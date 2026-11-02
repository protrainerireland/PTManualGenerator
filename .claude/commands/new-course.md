---
description: Start a new course folder from the template, ready for transcripts
argument-hint: [course folder name, e.g. power_bi_2027]
---

Set up a new course under `courses/`. The folder name is `$1` (lowercase with
underscores; ask for one if `$1` is empty).

1. **Check it is free.** If `courses/$1` exists, stop and say so rather than
   writing into it.

2. **Ask what you cannot know.** In one round of questions, not several:
   - the course title as it should read on the cover, and where a long one
     should break
   - the client, if any, and whether their logo goes on the covers
   - how long the course runs, and whether it is live, online or both
   - which documents it will have — participant notes, running order, trainer
     manual, something else — and what each should be called on its cover
   - what the file zip should be called, if the course hands out files

3. **Copy `courses/_template` to `courses/$1`**, then fill in:
   - `document_settings.toml`: `cover_title` (with `\n` where it should turn),
     `client_logo` if there is one, `files` / `zip_name`, and a
     `[[documents]]` block per document. Give each `name`, `file`, `subtitle`
     and, where the deliverable should be named more formally than the source,
     `output`.
   - `CLAUDE.md`: fill in the headings it prompts for from the answers above.
     Keep it to what is true of this course; the machinery is documented at
     the project root.
   - Delete any `[[documents]]` blocks or settings the course does not need
     rather than leaving them commented out.

4. **Create empty Markdown files** for each document listed, each with a
   one-line H1 title. Put `<!-- toc -->` at the top of any document that
   should have a contents page — normally the participant notes, not a short
   running order.

5. **Tell the user what to put where**: transcripts and the session's repo in
   `courses/$1/source/`, screenshots in `images/`, hand-out files in `files/`.
   Be explicit that `source/` is never built or shipped and `files/` is zipped
   by file type, so transcripts must not go there.

6. **Check it loads**: `python validate_docs.py --course $1`. It should report
   no errors. Do not build PDFs — there is nothing in the documents yet.

Report the folder created and the next command to run (`/running-order`).
