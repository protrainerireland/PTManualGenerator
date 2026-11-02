# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Not a software project. This is the authoring workspace for the course manuals of **Professional Training** (professional.ie): Markdown sources, screenshots and class files, built into branded PDFs. There is no git repository here.

One shared toolchain builds every course; each course is a folder under `courses/` holding its own documents, images, files and settings. Nothing about a particular course is written into the scripts or the stylesheet, and adding a course means adding a folder, not editing code.

```
build_deliverables.py          the build: Markdown -> branded PDF, plus a zip of the course files
validate_docs.py               the checks that apply to any course
cover_page.md                  the cover layout, shared, with {{TITLE}} and {{SUBTITLE}} placeholders
assets/professional_logo.jpg   files the shared cover itself refers to
tools/                         render_md.js, print_pdf.js, node_modules
tools/styles/                  the look of every manual
courses/
  ai_in_excel_2026/            the live course - see the last section
  _template/                   a starting point to copy; folders beginning with _ are never built
```

A course folder:

```
courses/<course>/
  CLAUDE.md                what is particular to this course - read it before editing its Markdown
  document_settings.toml   what to build and what goes on the covers - this is what makes it a course
  *.md                     the documents
  images/                  screenshots, written as images/... in the Markdown
  files/                   workbooks and hand-outs; the build zips them
  source/                  transcripts, repo, slides - what the documents were written from
  validate_course.py       optional checks of its own
  deliverables/            built output; never edited by hand
```

`source/` and `files/` are not interchangeable. `files/` is zipped **by file type**, so a `.docx` transcript or a `.pdf` of reference material left there goes to participants without a word; `source/` is never read by anything. Inputs there, hand-outs in `files/`.

Only documents listed in `[[documents]]` are built, so a half-written `section_9_draft.md` can sit in the folder without reaching anyone's PDF.

### Authoring commands

The workflow from recordings to PDFs is four slash commands in `.claude/commands/`:

| Command | What it does |
|---|---|
| `/new-course <folder>` | copies the template, asks what it cannot know, fills in the settings and the course's own `CLAUDE.md` |
| `/running-order <folder>` | drafts the running order from the transcripts in `source/`, with timings taken from the recordings rather than invented |
| `/flesh-out <section>` | writes up one numbered section of the notes from the transcripts and the session's code |
| `/trainer-manual <folder>` | drafts the delivery guide from the running order, the notes and how the material actually landed |

They are starting points, not a pipeline: each reads the course's own `CLAUDE.md` first, each ends by running `validate_docs.py`, and none of them builds a PDF. Two rules are written into all of them because they are the ones that matter — formulas, prompts and keystrokes are **copied from the transcripts or the repo, never composed**, and anything that cannot be sourced is reported rather than filled in. Edit the command files as your own habits settle; they are plain Markdown.

### Adding a course

Copy `courses/_template` to `courses/<name>`, fill in its `document_settings.toml` and its `CLAUDE.md`, and put the Markdown beside it. That is the whole procedure: the cover, the styling, the contents pages, the page-number footer and the zip all follow. Write course-specific checks, if it needs any, in a `validate_course.py` modelled on the one in `ai_in_excel_2026`.

Keep course folder names lowercase with underscores; the name is what `--course` takes.

## Building the deliverables

**Only build the PDFs when explicitly asked to.** After editing a document, make the edit, run the validator, and stop there — do not rebuild as a courtesy. The user decides when output is regenerated, so an unasked-for build is unwanted work. This means `deliverables/` is routinely older than the Markdown sources, and that is the expected state, not a problem to fix.

```
python build_deliverables.py                        ask which courses to build
python build_deliverables.py --all                  every course, no questions
python build_deliverables.py --course ai_in_excel_2026   (repeat for several)
python build_deliverables.py --only trainer         one document
python build_deliverables.py --no-zip               skip the file zip
python build_deliverables.py --skip-validate        build despite doc errors
```

With no course named, the build puts up a tick-list of the courses - each with its document and file counts and when it was last built - and builds the ones ticked. Space ticks, `a` ticks all, Enter builds. That list is `course_picker.py`, drawn with **questionary**; the build does not depend on it, falling back to a numbered prompt if it is not installed, and skipping the question entirely when there is nobody to ask - a pipe or a scheduled run - and building everything in that case. A lone course is shown ticked, so Enter builds it. So a script that ran `python build_deliverables.py` still works unattended.

Each course is validated first and errors stop the build. Output goes to that course's own `deliverables/`, so two courses can never overwrite each other.

Rendering is Markdown → HTML (`tools/render_md.js`, markdown-it plus markdown-it-checkbox for `- [ ]` lists) → PDF (`tools/print_pdf.js`, which drives headless Chrome over the DevTools protocol). The renderer and printer run with the course folder as their working directory, which is what makes `images/...` in a document resolve to that course's images.

The printer is a script rather than `chrome --print-to-pdf` because that command line offers only Chrome's stock header/footer (title, date, URL) or none at all; a custom footer is reachable only through `Page.printToPDF`. `print_pdf.js` has no dependencies — it uses Node's built-in WebSocket — and it owns the page margins, so do not put a `margin` back into the `@page` rule: a CSS page margin overrides the one passed to Chrome and clips the footer off the paper. The intermediate `.build.html` is written beside the source document so relative image paths resolve, and is deleted afterwards. Set `CHROME` to override browser detection. **pypdf** is required: the build reads page numbers back out of the PDFs and adds the footer link with it. **questionary** is optional, for the course tick-list.

Exporting a single document from VS Code (**Ctrl+Shift+P** → *Markdown PDF: Export (pdf)*) still works, but produces no cover page — nothing fills the placeholders — and no contents page numbers.

## Checking your work

```
python validate_docs.py                        every course
python validate_docs.py --course ai_in_excel_2026
```

Run this after editing any document — it is the one thing to run unprompted, unlike the PDF build. There is no build or test step; this stands in for one. Exit status 1 means errors; warnings do not fail the run.

`validate_docs.py` itself checks only what is true of any course: that every image a document asks for exists, that the cover's own files exist beside the cover, and that the settings are sane. It then calls `check(course)` in the course's own `validate_course.py`, if it has one, handing it the documents keyed by the names the settings give them (`notes`, `trainer`, …) along with `error()`, `warn()` and `note()`. Anything particular to a course belongs there — `ai_in_excel_2026` checks its running order's arithmetic, its segment numbering and its cross-references, none of which means anything to a course built differently.

## A course's settings: document_settings.toml

The settings file is what makes a folder a course. It holds:

| Key | Meaning |
|---|---|
| `cover_title` | the course name, filling `{{TITLE}}` on every cover |
| `cover_page` | the cover layout; found in the course folder first, then the project root, so the shared one is the default |
| `client_logo` | optional, under Professional Training's own logo. A bare filename is looked for in the images folder |
| `footer_link_text` / `footer_link_url` | optional clickable web address at the left of the footer |
| `files` / `zip_name` | the folder of hand-outs and what to call the zip of them; omit `files` and nothing is zipped |
| `images` | only if the screenshots are kept somewhere other than `images/` |
| `[[documents]]` | one block each: `name` (what `--only` takes), `file`, `subtitle` (filling `{{SUBTITLE}}`; `""` leaves the line off), and optionally `output`, what the PDF is called |

`build_deliverables.py` reads it afresh on every run and holds no course knowledge of its own. The loader checks rather than trusts: a missing settings file, an empty document list, a repeated `name`, a `file`, `cover_page` or `client_logo` that does not exist, each stops the build with a sentence naming the entry at fault. It needs Python 3.11 or newer for `tomllib`, and says so if it does not have it.

`output` separates the file you edit from the file you hand over: without it a PDF is named after its Markdown file, so `notes.md` becomes `notes.pdf`. With it, a source file can be short and working while the deliverable carries a formal name. Two documents cannot write the same PDF, and `output` names a file in `deliverables/`, not a path - both are refused with a message saying which entry is at fault.

Styling deliberately does *not* live here — that is the stylesheet, below.

## The cover page

`cover_page.md` in the project root is shared by every course: the title, a `<hr>` rule, the document type, the Professional Training logo, the optional client logo, and the Cork/Dublin/Limerick contact lines. Three placeholders are filled per document: `{{TITLE}}` from `cover_title`, `{{SUBTITLE}}` from that document's own entry, and `{{PUBLISHED}}`, the day the PDF was built, as dd/mm/yyyy. A course that needs a different cover keeps its own `cover_page.md`, which is found first.

- A `\n` in either value becomes a `<br>`, so a long title turns where it reads best rather than wherever it runs out of room. `as_html_lines()` in the build does that before the value reaches the renderer, because the text travels as a command-line argument and a newline inside one is not safe through a Windows shell. The values are otherwise dropped into raw HTML untouched: write an ampersand as `&amp;`, and a hand-written `<br>` works as well. The title is centred.
- A subtitle is optional: `""` and `render_md.js` drops the line rather than leaving a gap. It removes a line only when that line's **own** placeholder came back empty — which is what stops it sweeping up the cover's other empty elements.
- `{{PUBLISHED}}` comes from the build rather than from any setting, so it is always the date on the file and never a date someone forgot to change. It is settled once per run, so a build straddling midnight cannot date one document a day after another. The words around it are ordinary text in `cover_page.md`, so "Published date:" can be reworded or the line removed; `--published-size` and `--published-colour` in the stylesheet set how loudly it speaks.
- The shared cover's own files live in `assets/`, and `render_md.js` rewrites its relative paths to point there from wherever the document is being rendered. That is what lets one cover serve every course without a copy of the logo in each.
- Both logos are raw `<img>` tags rather than Markdown images, so they can carry the classes the stylesheet sizes them by. `validate_docs.py` reads `<img src="...">` as well as `![](...)`, and takes `client_logo` from the settings, so neither logo is reported as unused.
- The client logo is drawn at `--client-logo-scale` (50%) of `--cover-logo-width`, with the height left to follow the file's own proportions — so a logo of any size or shape is never stretched or skewed, and a new one needs no measuring.
- A cover carrying a client logo is nearly a full page, which caught out the empty `<div style="page-break-after: always;"></div>` that used to follow it: with no room left, the div fell onto the next page and broke after *itself*, leaving a blank page between cover and document. The cover now breaks after itself, via `.cover` in the stylesheet.

## Contents pages

Put `<!-- toc -->` at the top of a document and `render_md.js` replaces it with one row per numbered `##` section, each linked to its heading. It is generated, never written: adding, removing or renumbering a section updates it on the next build, and a contents page typed into the Markdown would go stale.

Page numbers are only known once a document has been printed, so such a document is printed twice — first with the numbers blank, to see where the sections fell, then again with them filled in, read back out of the PDF with pypdf. The rows are the same height either way, so the second print repaginates identically; the build prints a third time if it does not, and warns if the numbers never settle.

Give contents-page CSS classes a `toc-` prefix: `markdown-pdf.css` defines a bare `.page` as `page-break-after: always`, so a `class="page"` span puts every row on a page of its own.

## The page-number footer

`--footer-text` in the stylesheet takes `{page}` and `{pages}`; `""` turns the footer off. `footer_link_text` / `footer_link_url` in a course's settings add a web address at the left.

Chrome draws header and footer templates outside the page's own content and ignores any link in them, so the address takes two steps: `print_pdf.js` prints the words (`--footer-left`), and `add_footer_links()` lays a clickable rectangle over them with pypdf, measured from where the words actually landed so it follows the footer if the stylesheet moves it. Two traps live in that function, both already sprung: the footer's pieces are joined left to right until they spell out the address, because testing each piece for membership matched "of" out of "Page 3 of 7" inside "pr**of**essional" and stretched the clickable area across the page number; and since a PDF records no width for a run of text, the right-hand edge is estimated from the text's length and then held short of whatever is printed next.

Chrome prints a footer template in its own little document and reports nothing if it dislikes the markup — it falls back to its default style, about 1pt tall, present in the PDF's text but invisible on the page. That is what a `style="..."` attribute caused: the font stack's own double quotes closed the attribute early and took the font size with it, so the template is built from a `<style>` block instead. If page numbers ever go missing, measure the rendered size before assuming the footer is absent, and run `PRINT_PDF_DEBUG=1 node tools/print_pdf.js <chrome> <file.html> <out.pdf>` to see what the printer read from the stylesheet.

## Styling the PDFs

`tools/styles/professional_training_styles.css` is **the file to edit when something should look different**. It is loaded last, after the two vendored stylesheets, so its rules win, and it applies to every document of every course — which is how the manuals stay consistent and how a new course gets the house look for free. Nearly all of it is a `:root` block of named values (paper size and margins, the footer, body font and size, heading sizes and spacing, link colour, table borders and padding, quote and code blocks, the cover logos, the contents page), so changing the look normally means editing a value, not writing a rule.

`markdown.css` and `markdown-pdf.css` beside it are verbatim copies of the VS Code "Markdown PDF" extension's own stylesheets. Treat them as read-only and override in the house stylesheet instead.

Chrome, not the page, draws the paper margins and the footer, so `print_pdf.js` reads the `--page-*` and `--footer-*` custom properties back off the loaded page and passes them to the printer; lengths are measured rather than parsed, so cm, mm, in or px all work. Anything the stylesheet leaves out falls back to the defaults at the top of `print_pdf.js`.

**Watch for shrink-to-fit.** If anything on the page is wider than the text column, Chrome silently scales the whole document down until it fits, and says nothing. The AI in Excel notes printed at about two-thirds size for years because of a single table of long formulas — which is why changing the body font appeared to do nothing to them. The stylesheet sets `overflow-wrap: anywhere` on `code` inside table cells so long formulas wrap instead, while prose cells break at spaces like ordinary English. If a document ever ignores a font or margin change, measure the type in the PDF before believing the stylesheet is at fault: `tools/print_pdf.js` can be `require`d as a module, which is enough to load a rendered document in Chrome and ask which elements are wider than `document.body.clientWidth`.

Styling changes repaginate, so re-check the page counts after one. Pagination CSS was once banned here, because keeping table rows together repaginated a document onto an extra page; that caution stands — add such a rule only when asked for. Four are in force, all of them asked for:

| Value | Effect |
|---|---|
| `--section-page-break` | every `##` section starts a fresh page (suppressed for the first, so the title page is not left hanging) |
| `--keep-blocks-together` | a fenced prompt or formula block, and an image, is never split across pages |
| `--keep-headings-with-text` | no heading left stranded at the foot of a page |
| `--keep-images-with-text` | a screenshot stays with the sentence that introduces it |

All are preferences the browser drops when it cannot honour them — a block taller than a page is still split.

---

## The courses themselves

Each course folder carries its own `CLAUDE.md` with what is particular to it: its audience and client, the voice its documents are written in, how its documents cross-reference each other, and anything agreed with the client that is not mine to change. Read that before editing a course's Markdown — this file is only about the machinery.

- `courses/ai_in_excel_2026/CLAUDE.md` — AI in Excel Using ChatGPT & Copilot, delivered to the Institute of Chartered Accountants.
