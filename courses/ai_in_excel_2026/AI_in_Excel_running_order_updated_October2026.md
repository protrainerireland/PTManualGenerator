# AI in Excel Using ChatGPT & Copilot — Running Order (planned timeline)

Half-day live online course, **09:30–13:30**, with one 20-minute coffee break.
The **Notes §** column refers to the sections of *AI in Excel Course Notes (updated October 2026)*, which contain the full prompts, formulas and steps for each segment.
Files: **AI in Excel data.xlsx** (main workbook, one tab per exercise) and **AI in Excel errors.xlsx** (used in the final demo).
Tools: ChatGPT (browser) and Copilot (app). Everything except the Copilot in Excel segment works on free licences.

## Session 1 — Foundations (09:30–11:15)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 1 | 09:30 | 5 | Welcome & Trainer Introduction | 1 | Trainer Introduction; why AI took off in 2022 (anyone can talk to the computer like a human); no deep dive into the technology; training data mostly from the internet; course arc: formulas → intermediate → advanced (Power Query) |
| 2 | 09:35 | 5 | Delegate introductions | — | Name, role, AI use to date, which tools they have at work (ChatGPT is often blocked; Copilot is common) |
| 3 | 09:40 | 4 | Logistics & files | — | Cameras on; unmute to ask; chat for prompts and links; "Yes" reaction for polls; break ~11:15, finish 13:30; show participants how to download the course files from the webpage they used to enter the course, and unzip them; follow along, share screens if stuck |
| 4 | 09:44 | 4 | Tools tour | 1, 2 | ChatGPT and Copilot side by side; misspelt "Azerbaijan" question (AI infers meaning); side panel; **new chat per topic**; Excel data file |
| 5 | 09:48 | 10 | Limitations of AI | 1 | "May be incorrect" disclaimers; countries in Europe; non-determinism; unclear sources; out-of-date information (Ireland population, Bulgaria euro); bias; afternoon load and corner-cutting; hallucination (Cork Tesco stores); AI tells you what you want to hear. Assistant, not oracle |
| 6 | 09:58 | 15 | Parts of a prompt | 2 | Context (psychologist vs programmer NLP demo); NLP + corpus = LLM; persona; request (Europe ambiguity); examples; constraints; technique ("step-by-step instructions"); data; delimiter (Shift+Enter, one instruction per line); tone; format. Prompt engineering = human communication skills; birthday-cake mix-ups. Mention the infographic exercise as optional follow-up |
| 7 | 10:13 | 3 | Approach | 1 | Get AI to help *with* the analysis (a method you can check) rather than do the analysis |
| 8 | 10:16 | 5 | **Create a formula** | 4.1 | Compound interest (B2–E2, answer in G2); final value vs interest; sanity check |
| 9 | 10:21 | 6 | **Explain & debug a formula** | 4.2–4.3 | ExcelJet combine-ranges formula explained; VSTACK suggestion; paste into a sheet → #NAME?; replace placeholders with real ranges |
| 10 | 10:27 | 12 | **LET deep dive** | 4.4 | Poll (around 80% say no); rebuild step by step (Alt+Enter, ROWS, SEQUENCE, dynamic arrays, #SPILL!, IF, INDEX); rewrite without LET to show repetition; start a **new chat** afterwards so "no LET" doesn't stick |
| 11 | 10:39 | 10 | **To-do checklist** | 5 | Plain-English prompt → native checkboxes + conditional formatting strikethrough; Developer-tab answers are out of date; checkboxes are auditable (TRUE/FALSE); extension: formula listing items remaining |
| 12 | 10:49 | 8 | **Exercise: Progress tracker** | 7 | Delegates add checkboxes and a % complete formula; "make it visual" → data bars (fix the scale: Number 0–1) or REPT text bar |
| 13 | 10:57 | 10 | **XLOOKUP + dropdown** | 6 | Screenshot of data pasted into AI; XLOOKUP; XLOOKUP vs VLOOKUP; return name and price (CHOOSECOLS); data validation dropdown in F2 |
| 14 | 11:07 | 5 | **Keeping your data safe** | 3 | Follows on from the screenshot tip: don't share sensitive data with free tools; share structure, a header row or made-up sample data; paid Copilot + OneDrive "Add content"; check your organisation's AI policy |
| 15 | 11:12 | 3 | Recap | 1–7 | Limitations; parts of a prompt; describe the result, not the feature; screenshots; AI surfaces modern functions |
| — | 11:15 | 20 | **Coffee break** | | Back at 11:35 |

## Session 2 — Intermediate & Advanced (11:35–13:30)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 16 | 11:35 | 17 | **Excel Tables & structured references** | 8 | Switch to Copilot (new chat, context + persona); Ctrl+T; auto-expansion; contextual Table Design tab; styles; name the table; TRUE/FALSE → checkboxes; COUNTIF on a range vs structured reference; poll (roughly 40–50% say no); "what is this called?"; IntelliSense; cross-sheet comparison |
| 17 | 11:52 | 10 | **Extract invoice number** | 9.1 | Screenshot + "reliably"; expect early attempts to trip on the word "invoice"; feed back failing rows; nudge towards pattern matching → REGEXEXTRACT |
| 18 | 12:02 | 3 | **Validating a formula on large data** | 9.2 | Representative test set; sampling; grouping by pattern; deliberately trying to break it |
| 19 | 12:05 | 10 | **Unmatched invoices** | 9.3 | Show why tables matter: a fixed range misses a new invoice → convert to `Invoices` and `BankTransactions` tables → FILTER + COUNTIF; test by changing the data |
| 20 | 12:15 | 10 | **Full reconciliation** | 9.4 | Not paid / underpaid / overpaid / paid in full; amount paid, difference and status columns (SUMIFS + LET); names must match exactly |
| 21 | 12:25 | 5 | **Power Query intro** | 10 | Poll (around 80–90% say no); new chat; can AI take you from never having used a feature to using it?; what Power Query is; sources |
| 22 | 12:30 | 10 | **Web import** | 10.1 | Customers JSON endpoint; JSON explained; From Web → To Table → expand (untick prefix) → Close & Load; result is a named table |
| 23 | 12:40 | 10 | **Refresh & cleaning** | 10.1–10.2 | Add a record at source → Refresh; duplicate returns after manual delete → Remove Duplicates; Ireland / Republic of Ireland and USA / U.S.A. → Replace Values |
| 24 | 12:50 | 8 | **Data types, calculated columns & reports** | 10.3–10.4 | sales_records query: data types; custom LineValue column (M written by AI); Calculations tab updates on Refresh All |
| 25 | 12:58 | 2 | Power Query wrap-up | 10.4 | "Step-by-step instructions" is the phrase that pays; credit-union examples |
| 26 | 13:00 | 8 | **Copilot in Excel (paid)** | 11 | Cost; no need to describe cells; compound interest, checkboxes + strikethrough, XLOOKUP name and price + dropdown; be specific; keep checking |
| 27 | 13:08 | 8 | **Upload a file to find errors** | 12 | Check the file isn't sensitive; upload AI in Excel errors.xlsx; walk through what it finds; results vary between runs; a first pass, not a substitute for review |
| 28 | 13:16 | 7 | Wrap-up | 14 | Recap of limitations, prompting and everything AI did; habits to take away; "capable assistant, not infallible oracle"; share completed file in chat |
| 29 | 13:23 | 7 | Q&A | 13 | Common questions: free-tier limits, ChatGPT vs Copilot, uploading large documents |

## Notes for the trainer

**Before the course**
- **Start the session from the Zoom link on the course page participants use, never from the Zoom app**, and check the Course Name and Date on that page first — each run of the course has its own page. See the Trainer Manual, Section 4.
- Have ChatGPT, Copilot and Excel open side by side, and a completed copy of the data file ready to share in the chat at the end.
- Have the paid Copilot in Excel side panel available for segment 26. If you don't have a licence, show screenshots or skip it and extend the Q&A.
- Keep the longer prompts from the course notes to hand so you can paste them into the Zoom chat.

**Habits to model all day**
- Give context and a persona at the start of every new chat, and start a new chat for each topic.
- State exact cells, sheets, tables and column names, or use a screenshot.
- Describe the result you want rather than naming the Excel feature.
- Test every answer: sanity-check figures, change the data and watch the result.

**Things that commonly come up**
- **Out-of-date answers:** if AI suggests Developer > Form Control checkboxes, ask "Isn't there a more modern way?"
- **Data bars look wrong:** set Minimum and Maximum to type Number (0 and 1), not Percent.
- **Power Query instructions don't match the screen exactly:** e.g. the To Table dialog wording, or the prefix tick box not being mentioned. Use judgement and show delegates how to screenshot and ask.
- **Formulas need several attempts:** especially the invoice extraction and status formula. Iterating is part of the lesson; feed back what went wrong rather than fixing it yourself.
- **Name mismatches:** the AI may suggest its own column names (e.g. *Total Paid*). Either use them or tell it yours.
- **A slow or weak AI day:** switch tool, start a new chat, or come back to it later. Afternoons tend to be worse.

**Optional if time is short:** the LET rewrite (segment 10, last part), the To-do extension (segment 11), and data types/calculated columns (segment 24) can be shortened or referred to the notes without losing the thread of the course.
