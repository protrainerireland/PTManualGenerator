#!/usr/bin/env node
/*
 * Render one Markdown document to a self-contained HTML file, styled to match
 * the VS Code "Markdown PDF" extension (yzane.markdown-pdf).
 *
 * The stylesheets in tools/styles/ are copies of that extension's own, so the
 * output matches the PDFs produced from the editor. Page geometry (A4
 * portrait and the margins) is no longer set here: it is passed to
 * Page.printToPDF by tools/print_pdf.js, which has to own the margins because
 * the page-number footer is drawn inside them. A CSS @page margin would
 * override those and clip the footer.
 *
 *   node render_md.js <input.md> <output.html>
 *
 * The output is written next to the source document so that relative image
 * paths (images/...) still resolve when Chrome loads it.
 */

"use strict";

const fs = require("fs");
const path = require("path");

const markdownIt = require("markdown-it");
const checkbox = require("markdown-it-checkbox");

const argv = process.argv.slice(2);
const options = {
  pages: null,
  sections: null,
  cover: null,
  title: null,
  subtitle: null,
  clientLogo: null,
  published: null,
};
const positional = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === "--pages") options.pages = argv[++i];
  else if (argv[i] === "--sections") options.sections = argv[++i];
  else if (argv[i] === "--cover") options.cover = argv[++i];
  else if (argv[i] === "--title") options.title = argv[++i];
  else if (argv[i] === "--subtitle") options.subtitle = argv[++i];
  else if (argv[i] === "--client-logo") options.clientLogo = argv[++i];
  else if (argv[i] === "--published") options.published = argv[++i];
  else positional.push(argv[i]);
}
const [input, output] = positional;
if (!input || !output) {
  console.error(
    "usage: node render_md.js <input.md> <output.html> " +
      "[--cover cover_page.md --title '...' [--subtitle '...'] " +
      "[--published dd/mm/yyyy]] " +
      "[--pages pages.json] [--sections sections.json]"
  );
  process.exit(2);
}

const STYLE_DIR = path.join(__dirname, "styles");

// The stylesheets, in cascade order: the two vendored ones first, then the
// house style, which loads last so its rules win. All of the styling worth
// changing lives in styles/professional_training_styles.css - nothing is
// written inline here.
// Pagination CSS (keeping table rows or headings together) was tried in that
// file and reverted: it repaginates the running order onto 5 pages where the
// extension produced 4.
const STYLESHEETS = [
  "markdown.css",
  "markdown-pdf.css",
  "professional_training_styles.css",
];

function readStyle(name) {
  const file = path.join(STYLE_DIR, name);
  if (!fs.existsSync(file)) {
    console.error(`missing stylesheet: ${file}`);
    process.exit(1);
  }
  return fs.readFileSync(file, "utf8");
}

const md = markdownIt({
  html: true, // the documents use raw HTML for the cover page and page breaks
  breaks: false, // markdown-pdf.breaks default
  linkify: true,
  typographer: false,
}).use(checkbox); // the trainer manual's "- [ ]" checklists

// Numbered top-level sections ("## 4. Formulas with AI") get an id, so the
// contents page can link to them and so the build can find where each one
// landed in the printed PDF. Collected as a side effect of rendering.
const sections = [];
md.core.ruler.push("number_sections", (state) => {
  const tokens = state.tokens;
  for (let i = 0; i < tokens.length; i++) {
    const open = tokens[i];
    if (open.type !== "heading_open" || open.tag !== "h2") continue;
    const text = (tokens[i + 1] && tokens[i + 1].content) || "";
    const match = text.match(/^(\d+)\.\s+(.*)$/);
    if (!match) continue;
    const id = `sec-${match[1]}`;
    open.attrSet("id", id);
    sections.push({ id, number: match[1], title: match[2].trim() });
  }
});

/** The contents page: one row per numbered section, then a page break. */
function renderToc(pages) {
  const rows = sections
    .map((s) => {
      const page = pages && pages[s.id] ? String(pages[s.id]) : "";
      return (
        `<li><a href="#${s.id}"><span class="toc-num">${s.number}.</span>` +
        `<span class="title">${md.utils.escapeHtml(s.title)}</span></a>` +
        `<span class="toc-dots"></span><span class="toc-page">${page}</span></li>`
      );
    })
    .join("\n");
  return (
    `<nav class="toc">
<h1>Contents</h1>
<ol>
${rows}
</ol>
</nav>
` +
    `<div style="page-break-after: always;"></div>`
  );
}

/* The shared cover page, with its placeholders filled in. One file gives all
 * three documents the same branding; only the subtitle differs.
 *
 * A subtitle is optional, and an empty one has to leave no trace: a <p> with
 * nothing in it still takes up a line and would push the rest of the cover
 * down. So any element left empty by a missing placeholder is dropped. Both
 * values go into raw HTML untouched, which is what lets a long title carry
 * its own <br>. */
function coverMarkdown() {
  if (!options.cover) return "";
  // The client's logo is sized by the stylesheet, not here, so the tag
  // carries no width of its own to be stretched by.
  const clientLogo = options.clientLogo
    ? `<img src="${options.clientLogo.split(path.sep).join("/")}" alt="Client logo">`
    : "";
  const fields = {
    TITLE: options.title || "",
    SUBTITLE: options.subtitle || "",
    CLIENT_LOGO: clientLogo,
    PUBLISHED: options.published || "",
  };
  // A shared cover lives beside the courses rather than inside one, so the
  // files it refers to - the Professional Training logo - are its
  // neighbours, not the course's. Its relative paths are rewritten to point
  // at the same files from wherever this document's HTML is being written,
  // which is what lets one cover serve every course without a copy of the
  // logo in each.
  const fromCover = path.dirname(path.resolve(options.cover));
  const toOutput = path.dirname(path.resolve(output));
  const reroot = (url) => {
    if (/^([a-z]+:|\/|#)/i.test(url)) return url; // absolute, data:, anchor
    const target = path.resolve(fromCover, url);
    return path.relative(toOutput, target).split(path.sep).join("/");
  };
  const rebase = (line) =>
    line
      .replace(/(<img[^>]+src=")([^"]+)(")/g, (_, a, url, b) => a + reroot(url) + b)
      .replace(/(!\[[^\]]*\]\()([^)]+)(\))/g, (_, a, url, b) => a + reroot(url) + b);

  const fill = (line) =>
    line.replace(/\{\{(\w+)\}\}/g, (whole, key) =>
      key in fields ? fields[key] : whole
    );
  const empty = /^\s*<(\w+)[^>]*>\s*<\/\1>\s*$/;
  const lines = [];
  for (const line of fs.readFileSync(options.cover, "utf8").split("\n")) {
    const held = /\{\{\w+\}\}/.test(line);
    // Rebased before the placeholders are filled: the client logo's path is
    // given relative to the course, not to the cover, so it must not be
    // rewritten with the cover's own.
    const filled = fill(rebase(line));
    // Only a line whose own placeholder came back empty is dropped. The
    // cover's own empty elements - the page break at the end above all -
    // have to survive.
    if (held && empty.test(filled)) continue;
    lines.push(filled);
  }
  return lines.join("\n") + "\n\n";
}

const source = coverMarkdown() + fs.readFileSync(input, "utf8");
let body = md.render(source);

// The page numbers are only known after a first print, so the build renders
// twice: once without them (same layout, blank numbers) to find out where the
// sections fell, then again with --pages to fill them in. See
// build_deliverables.py.
if (body.includes("<!-- toc -->")) {
  let pages = null;
  if (options.pages) {
    pages = JSON.parse(fs.readFileSync(options.pages, "utf8"));
  }
  body = body.replace("<!-- toc -->", renderToc(pages));
}

if (options.sections) {
  fs.writeFileSync(options.sections, JSON.stringify(sections, null, 2), "utf8");
}

const title = path.basename(input, path.extname(input));

const html = `<!DOCTYPE html>
<html lang="en-IE">
<head>
<meta charset="utf-8">
<title>${title}</title>
<style>
${STYLESHEETS.map(readStyle).join("\n")}
</style>
</head>
<body>
${body}
</body>
</html>
`;

fs.writeFileSync(output, html, "utf8");
