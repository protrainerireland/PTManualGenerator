# AI-Driven Data Automation — Running Order

Full-day live online course, **09:30–16:15**, with a morning coffee break, lunch, and an afternoon coffee break.
Times are taken from the transcript of the delivered session, rounded to the minute.
The **Notes §** column refers to the sections of the participant notes, and is filled in as those sections are written.
Tools: **ChatGPT** and **Microsoft Copilot** in the browser, **Microsoft Excel** with Power Query, and a web browser for the course data site.
Files: the 26 annual sales workbooks (`SampleSalesData_2000.xlsx` … `2025.xlsx`), plus the images, receipts and invoices used in the morning.

## Session 1 — Working with AI, and getting data out of documents (09:30–10:55)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 1 | 09:30 | 5 | Arrivals | — | Wait for the room to fill; start proper at 09:35 |
| 2 | 09:35 | 5 | Welcome and trainer introduction | — | Trainer background, 30 years in programming and data; who the course is for — anyone producing periodic reports; the arc of the day: AI technique → Power Query → data from anywhere → APIs |
| 3 | 09:40 | 8 | Round the room | — | Each participant: role, organisation, what they use AI for today, what they want from the day. Most use Copilot; several want to automate weekly or monthly reports |
| 4 | 09:48 | 7 | Logistics and the tools | — | Zoom chat for long prompts and files; yes/no reactions as the check-in mechanism; ChatGPT and Copilot, free versus paid (and what the paid Office Copilot costs); Excel with Copilot integrated; the course download page |
| 5 | 09:55 | 16 | What to watch for with AI | 1 | It can be wrong — the countries of Europe demo, 50 vs 51; training data is the internet, roughly a quarter Wikipedia and a quarter Reddit; sources are rarely cited; out of date — Ireland's population, Bulgaria and Croatia on the euro; bias — Grok, DeepSeek; not deterministic; overloaded in the afternoon — shorter answers, truncated lists, hallucination (the Tesco stores that do not exist); start a new chat per topic |
| 6 | 10:11 | 16 | The parts of a prompt | — | Context (who you are — the NLP answer changes with it); persona; a clear, unambiguous, concise request; examples; constraints; method; the data itself; delimiters (and what prompt injection is); format; tone. Finish by having AI draw an infographic of the parts of a prompt |
| 7 | 10:27 | 16 | Getting data out of images and PDFs | — | OCR by AI: a photographed data table; two crumpled receipts in different layouts; three unrelated invoices (Microsoft, a training invoice, an ISP) — supplier, date, invoice number, total, VAT; formatting instructions that harmonise dates and numbers; a handwritten expenses list; what this means for accounts payable |
| 8 | 10:43 | 4 | Screenshots as input | — | Paste a screenshot instead of describing a spreadsheet; Greenshot, and Copilot's own freeform snip; include the column letters, row numbers and table name so formulas come back usable |
| 9 | 10:47 | 8 | What is Power Query? | — | Poll: roughly 8 in 10 have never used it. Ask AI what it is, then ask for a simpler answer; the problems it solves — import, clean, repeat; set the cleaning steps up once and press Refresh |
| — | 10:55 | 20 | Coffee break | — | |

## Session 2 — Power Query: importing and cleaning (11:15–12:30)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 10 | 11:15 | 3 | The course data site and JSON | — | `api.decodingtutor.com/customers`; reading JSON — square brackets are a list, curly brackets a record, each name/value pair a column |
| 11 | 11:18 | 9 | First Power Query: from the web | — | Ask AI for step-by-step instructions, with the URL delimited and a sample of the data; Data ▸ Get Data ▸ From Other Sources ▸ From Web; To Table; expand the column and untick "use original column name as prefix"; Close & Load; check 99 rows against the site |
| 12 | 11:27 | 7 | Queries, tables and refresh | — | The Queries & Connections panel; the query, sheet and table all take the same name; Table Design; add a customer on the site and Refresh All to see 100 rows |
| 13 | 11:34 | 9 | Removing duplicates | — | Delete a duplicate row by hand, refresh, watch it come back; describe the problem to AI; Query ▸ Edit; Home ▸ Remove Rows ▸ Remove Duplicates. (A participant's Copilot refused the same question twice — a worked example of an overloaded model) |
| 14 | 11:43 | 12 | Normalising the country names | — | Ireland / Republic of Ireland / Éire; Transform ▸ Replace Values, or right-click the value; Refresh Preview when the editor's snapshot is stale; ask AI to find the rest from a UNIQUE list — UK vs United Kingdom, USA vs U.S.A., España vs Spain |
| 15 | 11:55 | 4 | Structured references | — | `=UNIQUE(Customers[Country])` against `=UNIQUE(G2:G100)`; easier to read, and it does not need editing when the data grows; AI writes formulas this way, so it is worth being comfortable with them |
| 16 | 11:59 | 3 | Removing columns | — | Remove the internal ID; Remove Columns and Remove Other Columns when six of fifty columns matter |
| 17 | 12:02 | 4 | Applied Steps | — | The pipeline of steps as a recipe; rename a step; delete a step to undo a mistake; renaming a query renames the table and breaks formulas that used the old name |
| 18 | 12:06 | 9 | Data, Analysis, Dashboard | — | Three sheets: never touch the data; calculations on the analysis sheet; presentation on the dashboard. `=ROWS(Customers)` as a KPI; a shape holding a cell reference; turn off gridlines so it stops looking like Excel |
| 19 | 12:15 | 8 | A second source: sales records | — | The `sales_records` endpoint through the same steps; 1,671 rows; a transaction count on the analysis sheet and the dashboard; delete a record at source and refresh |
| 20 | 12:23 | 7 | Making dates real dates | — | "Sort A to Z" on a date column is the tell; change the column type in Power Query rather than formatting in Excel; whole numbers and decimals for quantity and price; what Power Query does with values that do not fit the type |
| — | 12:30 | 60 | Lunch | — | |

## Session 3 — Files, folders and calculated columns (13:30–14:55)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 21 | 13:30 | 13 | Importing a saved file | — | Save the JSON from the site, then Get Data ▸ From File (JSON, XML, CSV, Excel — and PDF); the steps after the source are identical; keep the export's file name the same and Refresh is all it takes; when the name changes, double-click the Source step and browse |
| 22 | 13:43 | 16 | Combining a folder of files | — | 26 annual sales workbooks; ask AI first — one dedicated folder, matching columns, same sheet or table name in each; Get Data ▸ From File ▸ From Folder; Combine & Transform; the sample file; 29,811 rows; sanity-check `Source.Name`; remove blanks; the helper queries it creates |
| 23 | 13:59 | 5 | Adding next year's file | — | Drop a 2026 file into the folder, refresh, and watch the new rows arrive with no change to the query |
| 24 | 14:04 | 14 | Analysis from a screenshot | — | Screenshot the table, table name included, and ask for a year-to-date total; check the figure by hand; what `TODAY()` means for a report run in January; last year's total; build a dashboard message by concatenating text and a rounded value on the analysis sheet |
| 25 | 14:18 | 4 | The refresh test | — | Add £40,000 of sales to the 2026 file, Refresh All, and watch data, analysis and dashboard update untouched |
| 26 | 14:22 | 11 | A calculated column | — | Sales records hold quantity, price and discount but no line value; resist adding an Excel formula — it is a manual step; Add Column ▸ Custom Column, `[Quantity] * [Price] * (1 - [Discount]/100)`; M is not Excel's formula language; ask for it again rounded, with `Number.Round` |
| 27 | 14:33 | 2 | Where the data has come from so far | — | A website, a second website, a single file, a folder of files |
| 28 | 14:35 | 20 | Getting data from an API | — | What an API is and why it changes reporting; exchangerate.host, its free tier and its API key; the documentation and the endpoint; building the URL from host, access key and symbols; the JSON record into a table; renaming a query that was named after a URL |
| — | 14:55 | 25 | Coffee break | — | |

## Session 4 — Data straight from a business system (15:20–16:15)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 29 | 15:20 | 7 | Finishing the exchange rate feed | — | What went wrong before the break — the key reset, and the query named after the URL; filter to the one rate that matters; look it up on the analysis sheet; dashboard shapes, euro and dollar icons, an arrow |
| 30 | 15:27 | 8 | CRM data the long way round | — | HubSpot as the stand-in for any CRM, ERP or accounts system; add a contact; export to CSV, wait for the email, download, import; drop the columns you do not need; a record ID forced to text so it stops being 8.98E+11; remove blanks |
| 31 | 15:35 | 13 | Asking for API access | — | Is it possible? Ask AI first; bearer tokens, authorization headers and scopes; creating a read-only service key in the system's own UI; who actually holds the key in your organisation, and why read-only answers most of IT's objections |
| 32 | 15:48 | 10 | The API into Excel | — | Three poor answers in a row from one assistant and the switch to the other — afternoon load is real; Get Data ▸ From Other Sources ▸ Blank Query ▸ Advanced Editor; paste the generated M, insert the key; it works first time; add a contact and refresh to prove it |
| 33 | 15:58 | 2 | Saving and sharing the workbook | — | Save with the date in the name; put the workbook and the query script in the chat before the meeting ends |
| 34 | 16:00 | 13 | Recap, and what it is worth | — | The whole day in order: OCR, Power Query, never edit the data, data/analysis/dashboard, the source step is the only one that changes, folders, APIs. Two credit union examples — a two-day monthly board report down to two hours, and 15 minutes a day across six branches down to five |
| 35 | 16:13 | 2 | Questions and close | — | |
