# CLAUDE.md — AI in Excel Using ChatGPT & Copilot

Guidance for this course in particular. The machinery that builds it — the
settings file, the cover, the stylesheet, the validator — is described in the
`CLAUDE.md` at the project root, and is shared with every other course.

**"AI in Excel Using ChatGPT & Copilot"** is a half-day (09:30–13:30) live online course delivered to members of the Institute of Chartered Accountants, whose logo is the `client_logo` on its covers. It currently builds to 42 pages (notes, including the contents page), 7 (running order) and 20 (trainer manual).

## The three documents and how they interlock

Edits to one almost always require edits to the others. Keep them consistent.

| File | Role | Cross-reference convention |
|---|---|---|
| `AI_in_Excel_Course_Notes_updated_October2026.md` | Participant Reference Manual — every prompt, formula and step, numbered **§1–§14** | The source of truth for content |
| `AI_in_Excel_running_order_updated_October2026.md` | Minute-by-minute timeline, **segments 1–29**, two sessions split by a 20-min break at 11:15 | Has a "Notes §" column pointing into the course notes |
| `AI_in_Excel_Trainer_Manual_October2026.md` | How to deliver it — audience, ground rules, segment-by-segment guide | Cites *Segment N* (running order) and *Notes §N* (course notes) |

So: changing a section number in the notes breaks the running order's "Notes §" column and the trainer manual's §-citations. Changing a segment's duration shifts every later start time in the running order *and* the checkpoint times in the trainer manual's §8 "Managing time". Adding or cutting a segment renumbers the running order and the trainer manual's §6. `validate_course.py` checks all of this; a timing error is reported at the first row that disagrees with its predecessor — that row is the edit to fix, not the dozen consistent rows after it.

`AI_in_Excel_Course_Notes.md` (no date suffix) is the **superseded original**, kept for reference. It follows the older delivery order and has 12 sections, not 14. It is not listed in the settings, so it is neither built nor checked. Do not edit it unless asked; new work goes in the `_updated_October2026` file.

## Document conventions

- **Images** live in `images/` and are referenced relatively (`images/01_compound_interest.png`). The numeric prefix tracks the *original* delivery order, not the current section order, so image numbering looks out of sequence in the updated notes — that is expected, don't renumber.
- **Voice**: Hiberno-English/British spelling, second person, plain English for a senior non-technical-about-AI audience that is already expert in Excel and finance. Prompts the trainer types are in *italics* or fenced blocks; Excel functions, cell refs, keystrokes and UI labels in **bold**.
- **Workbook names**: the documents refer to the files as *AI in Excel data.xlsx* and *AI in Excel errors.xlsx*, but the files on disk in `files/` are `AiAndExcelData.xlsx` and `AiAndExcel_Errors.xlsx`, and the distributed zip keeps those on-disk names. So the prose names and the filenames participants receive genuinely differ. Leave both as they are unless asked — but it is worth flagging to the user if it ever causes confusion in class.

## The course workbooks

`files/AiAndExcelData.xlsx` — one tab per exercise, in roughly course order:
`Compound Interest`, `ToDo`, `Progress`, `XLOOKUP`, `SalesCommission`, `ProjectTasks`, `Q1Sales`, `Invoices`, `Bank Transactions`, `MonthlySales`, `sales_records`, `Calculations`.

`files/AiAndExcel_Errors.xlsx` — tabs `Error1`–`Error5`, deliberately broken, used in the final "can AI audit a spreadsheet?" demo (Notes §12). Error 5 (an unanchored VAT reference) is the one the notes screenshot.

Tab names, cell addresses and table names (`Invoices`, `BankTransactions`, `ProjectTasks`) are quoted literally throughout the documents. If a workbook changes, grep the three `.md` files for the old name.

## Editing rules that matter here

- Every formula, prompt and keystroke in the notes was demonstrated live. Don't invent or "improve" a formula without being asked — if a change is needed, flag that it needs re-testing in Excel.
- Timings in the running order must sum correctly: each segment's start = previous start + previous duration, across the break at 11:15–11:35, finishing at 13:30.
- The trainer manual states the content is "scrutinised and agreed between Professional Training and the Institute". Treat topic, exercise and order changes as needing the user's explicit sign-off rather than editorial judgement.
