---
description: Draft a trainer manual from the running order and the participant notes
argument-hint: [course folder name]
---

Draft the trainer manual for the course in `courses/$1` — how to *deliver* the
course, not what it contains.

**Which course.** If `$1` names one, use it. If `$1` is empty and there is
only one course, use that. Otherwise **ask which** — never pick for the user,
and never do more than one course in a run. Say which course you are working
on before you start writing.

**Never overwrite work.** Before writing anything, read the course's trainer
manual if it has one. If it already has content, **stop and say so**, and ask
whether to replace it, revise it in place, or leave it. A delivery guide
accumulates a trainer's hard-won experience; a draft from a transcript is not
worth losing it over. If the course has no trainer manual listed in its
settings, say what needs adding there — a `[[documents]]` block and a
Markdown file — and stop.

**Read first:** the course's `CLAUDE.md`, its running order (the spine of this
document), its participant notes (what each segment teaches), and the
transcripts in `source/` for how the material actually landed — what people
asked, what took longer than expected, what needed saying twice.

**The trainer manual is the running order with delivery advice attached.** A
sensible shape, adapted to the course:

- Who the audience is and what they already know
- What to have open and ready before the first slide
- Ground rules: how to handle questions, chat, screen sharing, exercises
- A segment-by-segment guide: for each, what to do, what to say, what
  typically goes wrong, and what to cut if time is short
- Managing time: checkpoints, and what to drop first
- Frequently asked questions, with answers

**Conventions that the validator checks** (match the course's existing ones —
read `validate_course.py` if it has one):

- Cite the running order as *Segment N* and the notes as *Notes §N*. Every
  such citation must resolve: segments that exist, sections that exist.
- Checkpoint times must be real segment start times from the running order,
  not approximations:

```markdown
### Checkpoints

| By | You should be starting |
|---|---|
| 09:58 | Parts of a prompt |
```

- `- [ ]` checklists render as checkboxes in the PDF; use them for what the
  trainer has to do, not for content.

**Draw the delivery advice from the transcripts, not from imagination.** What
confused people, what the trainer repeated, which exercise ran long — that is
the value of this document, and it is all in the recordings. Where you have
nothing to go on for a segment, give the mechanics and say the advice needs
the trainer's own experience, rather than padding it.

**Finish by** running `python validate_docs.py --course $1`, fixing what it
reports, and saying which segments you had little transcript evidence for. Do
not build PDFs.
