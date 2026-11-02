---
description: Draft a course's running order from the transcripts in source/
argument-hint: [course folder name] [optional: finish time, e.g. 13:30]
---

Draft the running order for the course in `courses/$1` from its transcripts.

**Which course.** If `$1` names one, use it. If `$1` is empty and there is
only one course, use that. Otherwise **ask which** — never pick for the user,
and never do more than one course in a run. Say which course you are working
on before you start writing, even when there was only one to choose from.

**Never overwrite work.** Before writing anything, read the course's running
order document. If it already has segments in it — anything beyond a title
line — **stop and say so**, with its segment count and the span of its
timings, and ask whether to replace it, revise it in place, or leave it. This
document is written by hand and agreed with clients; a draft built from a
transcript is not worth losing it over. The same applies if the course's
`source/` folder holds no transcripts: say so and stop, rather than inventing
a timetable.

**Read first, in this order:** `courses/$1/CLAUDE.md`, then
`courses/$1/document_settings.toml` to see which document is the running
order, then everything in `courses/$1/source/`. The transcripts are the
record of what was actually taught — the running order describes that, not an
idealised syllabus.

**Work out the shape of the day from the transcripts themselves:** where the
session started and finished, where the break fell and how long it ran, and
how long each topic actually took. Timings come from the transcript's own
clock wherever it has one. Where it does not, say so rather than inventing a
figure, and offer an estimate for the user to correct.

**Write the running order** in this form, which `validate_course.py` and the
build both expect:

```markdown
## Session 1 — Foundations (09:30–11:15)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 1 | 09:30 | 5 | Welcome & Trainer Introduction | 1 | short, concrete list of what is covered |
| — | 11:15 | 20 | Coffee break | — | |
```

- A session heading carries its own start and end: `## Session N — Name (HH:MM–HH:MM)`.
- Each row's **Time** is the previous row's time plus its **Mins**, without
  exception. The last row must end at the declared finish time ($2 if given).
- Segments are numbered 1, 2, 3 … without a gap. Breaks take `—` in the
  number and the Notes § columns.
- **Notes §** points at the participant notes' numbered sections. Leave it `—`
  for anything the notes do not cover, and come back to it after
  `/flesh-out` — a reference to a section that does not exist yet is an error.
- **What to cover** is a terse list of the concrete things done in that
  segment, not a sentence of description.

**Then:**

1. Run `python validate_docs.py --course $1` and fix what it reports. The
   arithmetic must pass before you show the result.
2. Tell the user, briefly: the shape you found in the transcripts, anything
   you had to estimate, and anything taught that you have *not* given a
   segment to. Do not build PDFs.
