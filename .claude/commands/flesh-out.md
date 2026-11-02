---
description: Write up one section of the participant notes from the transcripts and code
argument-hint: [section number or topic] [optional: course folder name]
---

Write up section **$1** of the participant notes, from the transcripts and
source code of that course.

**Which course.** If `$2` names one, use it. If `$2` is empty and there is
only one course, use that. Otherwise **ask which** — never pick for the user,
and never write into more than one course in a run. Say which course and
which section you are writing before you start.

**Never overwrite work.** Before writing, read the section as it stands. If
it already has content, **stop and say so** — summarise what is there in a
line — and ask whether to replace it, extend it, or leave it alone. Adding a
new section, or filling one that is only a heading, needs no such question.
Equally, if the course's `source/` holds nothing covering this topic, say so
and stop rather than writing the section from general knowledge: these notes
are a record of what was taught.

**Read first:** the course's `CLAUDE.md` (voice and conventions), the running
order's row for this section (what was actually covered, and how long it
took), the notes' existing sections either side of it (so this one matches
them in depth and tone), and the parts of `source/` that deal with this
topic — transcript passages and any code or workbook the session used.

**Then write it**, as a numbered section of the notes:

```markdown
## 7. Section title

Short lead-in: what this is for and when you would use it.

### 7.1 A step with a name

Numbered steps, each one something the reader does.

The prompt the trainer typed, in italics or a fenced block, exactly as typed.

The formula or code, exactly as it appeared.

A sentence on what the result was, and what to watch out for.
```

**The rules that matter here:**

- **Every formula, prompt, keystroke and file name comes from the transcript
  or the repo. Copy them; do not compose them.** If something is needed and
  the sources do not have it, write the prose around it and say plainly what
  is missing — never invent a formula that has not been run. Anything you do
  reconstruct must be flagged for re-testing.
- Screenshots: refer to `images/<file>.png` only where that file exists. Where
  one is needed and missing, say which screenshot to take rather than
  referencing a file that is not there.
- Keep the section numbered consistently with its neighbours, and its
  subsections `N.1`, `N.2` in the order the work was done.
- Follow the course's own voice as its `CLAUDE.md` describes it.
- The notes are the source of truth for content, so anything taught that the
  running order summarises in a phrase belongs here in full.

**Finish by:**

1. Updating the running order's **Notes §** column for the segments this
   section covers.
2. Running `python validate_docs.py --course <course>`, and fixing what it
   reports.
3. Saying in a line or two what you took from where, and listing anything you
   could not source from the transcripts — that list is the point of this
   step. Do not build PDFs.
