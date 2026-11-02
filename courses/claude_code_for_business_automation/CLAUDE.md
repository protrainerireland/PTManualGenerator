# CLAUDE.md — Claude Code For Business Automation

Guidance for this course in particular. The machinery that builds it — the
settings file, the cover, the stylesheet, the validator — is described in the
`CLAUDE.md` at the project root and is shared with every other course. Keep
this file to what is true of this course alone.

## What it is

Claude Code For Business Automation: using Claude Code to automate ordinary
business work — file and document handling, reporting, data tidying, routine
multi-step jobs — rather than as a software-engineering tool.

- **Audience**: business users and analysts, not developers. Assume comfort
  with files, folders and a spreadsheet; assume nothing about the terminal,
  git or programming languages. Every command is shown in full.
- **Client**: TechIA Skillnet. The cover carries Professional Training's logo
  only until they send theirs — then drop the file into `images/` and
  uncomment `client_logo` in `document_settings.toml`.
- **Length and delivery**: six days, delivered online over Zoom, run in pairs
  of consecutive days a few weeks apart. Days 1–2 were 7–8 October 2026, days
  3–4 were booked for 2–3 November 2026. Each day runs 09:30–16:05 with a
  mid-morning break, an hour for lunch from 12:30, and a mid-afternoon break.
  The length is deliberately kept off the cover.
- **Hand-out files**: none at present. If the course gains workbooks, scripts
  or prompt files, make a `files/` folder and restore the `files` /
  `zip_name` settings — the commented block in `document_settings.toml` says
  how.

## The documents and how they interlock

| Document | Source file | What it is |
|---|---|---|
| Participant notes | `notes.md` | the reference manual, kept after the day; carries a generated contents page |
| Running order | `running_order.md` | the timed session plan the trainer works from |

The running order refers to the notes by section number. Renumber a `##`
section in `notes.md` and every reference to it in the running order has to
move with it — the contents page regenerates itself, the cross-references do
not. A trainer manual can be added later with a `[[documents]]` block and
nothing else.

## Where it came from

`source/` holds the Zoom transcripts of days 1 and 2 (7 and 8 October 2026),
timestamped to the second. Days 3–6 are not there yet. The project folders
worked in live — the `pyclock` script and the Flask course website with its
JSON-backed REST API — are not in `source/` either, and the notes will need
them before any code can be written up.

`source/` is never built and never shipped — it exists so the documents can
be written from what was actually said and typed.

The rule that matters most here: **commands,
prompts and file paths are copied from the transcripts or the session's
repo, never composed.** A command that was never run does not go in the
manual. Anything that cannot be sourced is flagged, not invented.

## Voice

- Irish/UK spelling throughout ("organise", "colour", "behaviour").
- Second person, present tense: "you ask Claude to…", not "the user may".
- Terminal commands, file paths and anything typed verbatim go in `code`
  spans; a prompt given to Claude goes in a fenced block so it survives
  copying and is never split across a page.
- Screenshots live in `images/` and are referred to as `images/...`. Each one
  is introduced by the sentence before it.

## Editing rules that matter

- Claude Code moves quickly. Anything version-dependent — a flag, a slash
  command, a settings key — is dated in the text or checked against the
  transcripts before it is changed.
- Nothing demonstrated live is "improved" in the manual without re-running
  it; a tidier command that was not the one on screen confuses anyone
  rewatching the recording.
