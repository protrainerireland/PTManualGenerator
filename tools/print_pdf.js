#!/usr/bin/env node
/*
 * Print a local HTML file to PDF with a page-number footer.
 *
 *   node print_pdf.js <chrome.exe> <input.html> <output.pdf>
 *
 * Chrome's --print-to-pdf command line cannot set a custom footer: it offers
 * only the browser's default header/footer (document title, date, URL and
 * page number), which is why the build used --no-pdf-header-footer and got no
 * page numbers at all. The footer template is only reachable over the
 * DevTools protocol, so this script starts headless Chrome with a debugging
 * port, drives Page.printToPDF itself, and asks for "Page N of M" centred in
 * the bottom margin.
 *
 * No dependencies: the WebSocket client is Node's own (Node 22+).
 *
 * Chrome, not the page, draws the paper margins and the footer, so neither
 * can be set by ordinary CSS. They are still described in the house style
 * (styles/professional_training_styles.css) as the --page-* and --footer-*
 * custom properties: this
 * script reads them back off the loaded page and hands them to Chrome, so
 * everything about how a manual looks stays in the one stylesheet. The
 * defaults below are used for anything the stylesheet does not define.
 */

"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawn } = require("child_process");

const CM = 1 / 2.54; // inches per centimetre

// Used only where styles/professional_training_styles.css leaves a property out.
const DEFAULTS = {
  paperWidth: 21.0 * CM,
  paperHeight: 29.7 * CM,
  marginTop: 1.5 * CM,
  marginBottom: 1.3 * CM,
  marginLeft: 1.0 * CM,
  marginRight: 1.0 * CM,
  footerText: "Page {page} of {pages}",
  footerFont: "'Segoe UI', system-ui, sans-serif",
  footerSize: "8px",
  footerColour: "#666666",
  marginLeftCss: "2cm",
};

/* Read the --page-* and --footer-* custom properties off the loaded page.
 * Lengths are measured rather than parsed, so the stylesheet can use cm, mm,
 * in or px as it pleases: a hidden probe is given the value as its width and
 * its pixel width divided by 96 is the length in inches, which is the unit
 * Page.printToPDF takes. */
const READ_STYLE = `(() => {
  const root = getComputedStyle(document.documentElement);
  const probe = document.createElement("div");
  probe.style.cssText = "position:absolute;visibility:hidden;height:0";
  document.body.appendChild(probe);
  const inches = (name) => {
    const value = root.getPropertyValue(name).trim();
    if (!value) return null;
    probe.style.width = value;
    const px = probe.getBoundingClientRect().width;
    return px > 0 ? px / 96 : null;
  };
  const text = (name) => {
    const value = root.getPropertyValue(name).trim();
    if (!value) return null;
    // Strip the quotes around a CSS string, but only when they wrap the whole
    // value: a font stack like '"Segoe UI", system-ui' keeps its own.
    const quoted = value.match(/^"([^"]*)"$/) || value.match(/^'([^']*)'$/);
    return quoted ? quoted[1] : value;
  };
  const style = {
    paperWidth: inches("--page-width"),
    paperHeight: inches("--page-height"),
    marginTop: inches("--page-margin-top"),
    marginRight: inches("--page-margin-right"),
    marginBottom: inches("--page-margin-bottom"),
    marginLeft: inches("--page-margin-left"),
    footerText: text("--footer-text"),
    footerFont: text("--footer-font"),
    footerSize: text("--footer-font-size"),
    footerColour: text("--footer-colour"),
    // The left margin as written, not measured: the footer template needs
    // it as a CSS length so its text lines up with the text column.
    marginLeftCss: text("--page-margin-left"),
  };
  probe.remove();
  return JSON.stringify(style);
})()`;

function escapeHtml(text) {
  return text.replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])
  );
}

/* The footer Chrome draws in the bottom margin, from the house style.
 *
 * Lengths are multiplied by --scale-factor, the variable Chrome sets in a
 * header/footer template when the print is scaled, so that the footer scales
 * with the page rather than staying put. At our scale of 1 it is 1:1, so
 * --footer-font-size: 10px prints as 10px.
 *
 * Get the markup wrong here and there is no error: Chrome silently prints
 * the footer in its own default style, about 1pt tall, which is in the PDF
 * but far too small to see. That is worth knowing, because it is exactly
 * what a style="..." attribute did - a font stack carries its own double
 * quotes, which closed the attribute early and took the font size with it. */
function footerTemplate(style, footerLeft) {
  const body = escapeHtml(style.footerText)
    .replace("{page}", '<span class="pageNumber"></span>')
    .replace("{pages}", '<span class="totalPages"></span>');
  const scaled = (length) => `calc(${length} * var(--scale-factor, 1))`;
  // The text at the left of the footer sits in the margin the page numbers
  // are centred in, so it is positioned rather than placed in the flow:
  // whatever its length, the page number stays in the middle of the page.
  const left = footerLeft
    ? `<span id="pt-footer-left">${escapeHtml(footerLeft)}</span>`
    : "";
  // A <style> block rather than a style attribute: a font stack carries its
  // own double quotes, which would close the attribute early and silently
  // drop everything after it.
  return `<style>
    #pt-footer {
      position: relative;
      width: 100%;
      box-sizing: border-box;
      text-align: center;
      padding: 0 ${scaled("1cm")};
      font-family: ${style.footerFont};
      font-size: ${scaled(style.footerSize)};
      color: ${style.footerColour};
    }
    #pt-footer-left {
      position: absolute;
      left: ${scaled(style.marginLeftCss || "2cm")};
    }
  </style>
  <div id="pt-footer">${left}${body}</div>`;
}

// Chrome insists on a header template when header/footer are shown; an empty
// one keeps the top of the page as it was.
const HEADER = `<span style="display:none"></span>`;

const [, , chrome, input, output, ...rest] = process.argv;
// Optional: text for the left of the footer, e.g. a website address.
let footerLeft = "";
for (let i = 0; i < rest.length; i++) {
  if (rest[i] === "--footer-left") footerLeft = rest[++i] || "";
}
// Only when run as a command. Required as a module, there are no arguments
// to check and complaining about them would be wrong.
if (require.main === module && (!chrome || !input || !output)) {
  console.error(
    "usage: node print_pdf.js <chrome> <input.html> <output.pdf> "
      + "[--footer-left 'text']"
  );
  process.exit(2);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitForPort(portFile, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const lines = fs.readFileSync(portFile, "utf8").split("\n");
      if (lines.length >= 2 && lines[0].trim()) {
        return { port: lines[0].trim(), wsPath: lines[1].trim() };
      }
    } catch {
      /* not written yet */
    }
    await sleep(100);
  }
  throw new Error("Chrome did not report a debugging port");
}

/** Minimal CDP client over Node's built-in WebSocket. */
class Devtools {
  constructor(ws) {
    this.ws = ws;
    this.nextId = 1;
    this.pending = new Map();
    this.listeners = [];
    ws.addEventListener("message", (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        msg.error ? reject(new Error(msg.error.message)) : resolve(msg.result);
      } else if (msg.method) {
        for (const listener of this.listeners) listener(msg);
      }
    });
  }

  static async connect(url) {
    const ws = new WebSocket(url);
    await new Promise((resolve, reject) => {
      ws.addEventListener("open", resolve, { once: true });
      ws.addEventListener("error", () => reject(new Error("cannot reach Chrome")), { once: true });
    });
    return new Devtools(ws);
  }

  send(method, params = {}, sessionId) {
    const id = this.nextId++;
    const message = { id, method, params };
    if (sessionId) message.sessionId = sessionId;
    this.ws.send(JSON.stringify(message));
    return new Promise((resolve, reject) => this.pending.set(id, { resolve, reject }));
  }

  once(method, sessionId, timeoutMs) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.listeners = this.listeners.filter((l) => l !== listener);
        reject(new Error(`timed out waiting for ${method}`));
      }, timeoutMs);
      const listener = (msg) => {
        if (msg.method !== method) return;
        if (sessionId && msg.sessionId !== sessionId) return;
        clearTimeout(timer);
        this.listeners = this.listeners.filter((l) => l !== listener);
        resolve(msg.params);
      };
      this.listeners.push(listener);
    });
  }
}

async function main() {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "mdpdf-"));
  const child = spawn(
    chrome,
    [
      "--headless=new",
      "--disable-gpu",
      "--no-sandbox",
      "--no-first-run",
      "--no-default-browser-check",
      "--disable-extensions",
      "--run-all-compositor-stages-before-draw",
      "--remote-debugging-port=0",
      `--user-data-dir=${profile}`,
      "about:blank",
    ],
    { stdio: "ignore" }
  );

  let client;
  try {
    const { port, wsPath } = await waitForPort(path.join(profile, "DevToolsActivePort"), 30000);
    client = await Devtools.connect(`ws://127.0.0.1:${port}${wsPath}`);

    const { targetId } = await client.send("Target.createTarget", { url: "about:blank" });
    const { sessionId } = await client.send("Target.attachToTarget", { targetId, flatten: true });

    await client.send("Page.enable", {}, sessionId);
    const loaded = client.once("Page.loadEventFired", sessionId, 60000);
    await client.send("Page.navigate", { url: pathToFileUrl(input) }, sessionId);
    await loaded;

    // Images and fonts can still be in flight when the load event fires.
    await client.send(
      "Runtime.evaluate",
      {
        awaitPromise: true,
        expression: `Promise.all([
          document.fonts.ready,
          ...[...document.images].filter(i => !i.complete).map(i =>
            new Promise(r => { i.addEventListener('load', r); i.addEventListener('error', r); }))
        ])`,
      },
      sessionId
    );

    // The page geometry and the footer come from the house style.
    const read = await client.send(
      "Runtime.evaluate",
      { expression: READ_STYLE, returnByValue: true },
      sessionId
    );
    const declared = JSON.parse(read.result.value);
    if (process.env.PRINT_PDF_DEBUG) console.error('declared', declared);
    const style = { ...DEFAULTS };
    for (const [key, value] of Object.entries(declared)) {
      if (value !== null && value !== "") style[key] = value;
    }
    const wantsFooter = declared.footerText !== "";

    const { paperWidth, paperHeight, marginTop, marginRight, marginBottom, marginLeft } = style;
    const { data } = await client.send(
      "Page.printToPDF",
      {
        paperWidth,
        paperHeight,
        marginTop,
        marginRight,
        marginBottom,
        marginLeft,
        displayHeaderFooter: wantsFooter,
        headerTemplate: HEADER,
        footerTemplate: wantsFooter
          ? footerTemplate(style, footerLeft)
          : HEADER,
        preferCSSPageSize: false,
      },
      sessionId
    );
    fs.writeFileSync(output, Buffer.from(data, "base64"));

    await client.send("Target.closeTarget", { targetId });
    await client.send("Browser.close").catch(() => {});
  } finally {
    if (client) client.ws.close();
    child.kill();
    await sleep(200);
    fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5 });
  }
}

function pathToFileUrl(p) {
  return require("url").pathToFileURL(path.resolve(p)).href;
}

// Also usable as a module, so that a throwaway script can borrow the Chrome
// plumbing to ask a question of a rendered document - how wide its widest
// element is, say - without a second copy of all this.
if (require.main === module) {
  main().catch((err) => {
    console.error(`  ERROR: ${err.message}`);
    process.exit(1);
  });
} else {
  module.exports = { Devtools, waitForPort, sleep, pathToFileUrl };
}
