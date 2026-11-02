# CLAUDE.md — AI-Driven Data Automation

Guidance for this course in particular. The machinery that builds it — the
settings file, the cover, the stylesheet, the validator — is described in the
`CLAUDE.md` at the project root and is shared with every other course. Keep
this file to what is true of this course alone; whoever is working on its
Markdown reads this one.

## What it is

**"AI-Driven Data Automation"** is a full-day live online course delivered by
Professional Training (professional.ie) to members of the Institute of
Chartered Accountants, whose logo is the `client_logo` on its covers.

The day runs **09:30–16:15**, in four sessions: 09:30–10:55, 11:15–12:30,
13:30–14:55 and 15:20–16:15, with coffee at 10:55 and 14:55 and lunch from
12:30 to 13:30. Those times come from the transcript of the delivered session
and are checked by `validate_course.py`, so a change to any segment's length
has to be carried through the rest of the running order.

> Still to fill in: who the audience is and what they already know, and what
> the course promises to leave them able to do.

## The documents

| File | Role | Cross-reference convention |
|---|---|---|
| `notes.md` | Participant Reference Manual — every prompt, step and piece of code, in numbered `##` sections with a generated contents page | The source of truth for content |
| `running_order.md` | The timetable: sessions, segments, minutes, and a **Notes §** column pointing into the notes | Drafted from the transcripts |

A trainer manual can be added later: write the Markdown, add a
`[[documents]]` block for it, and it gets the same cover and styling as the
others.

Renumbering a section in the notes breaks the running order's **Notes §**
column. Changing a segment's duration shifts every later start time in the
running order. Both are checked by `python validate_docs.py --course
ai_driven_data_automation`.

## Where it came from

`source/` holds the transcripts of the live sessions and the GitHub repo for
the code written in them. Everything in the notes should be traceable to one
or the other — code and prompts are copied from them, never composed. Nothing
in `source/` is built or shipped.

`source/CAI - AI driven Data Automation.txt` is the full transcript of the
delivered session, timestamped throughout, 09:29 to 16:13. The running order
was drafted from it.

`source/AI-Data-datafiles.zip` holds the 26 annual sales workbooks
(`SampleSalesData_2000.xlsx` … `2025.xlsx`) used for the folder-combining
exercise. These are hand-outs rather than source material: unzip them into
`files/` so the build ships them to participants.

> Still to fill in: the images, receipts and invoices used in the morning
> (the "extra materials" file), which are not in `source/` yet.

## Voice

Hiberno-English/British spelling, second person, plain English. Prompts typed
into an AI tool are in *italics* or fenced blocks; file names, UI labels and
keystrokes in **bold**; code in fenced blocks with a language.

**Level: follow-along steps throughout.** Spell out each click and keystroke,
including the Excel ones, so that the notes work for somebody who was not in
the room and is not strong in Excel. The attendees were finance people from
banking, pharma, a credit union and practice; most used Copilot daily, and 8
in 10 had never used Power Query.

## Editing rules that matter here

- Every prompt, command and piece of code in the notes was demonstrated live.
  Don't invent or "improve" one without being asked — if a change is needed,
  flag that it needs re-running.
- Timings in the running order must sum correctly: each segment's start =
  previous start + previous duration, across the break, finishing at the
  declared time.

> Still to fill in: anything agreed with the Institute that is not ours to
> change.
