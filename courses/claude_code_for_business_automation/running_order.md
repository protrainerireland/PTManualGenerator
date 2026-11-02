# Claude Code For Business Automation — Running Order

Drafted from the Zoom transcripts of the first two days, delivered online for
TechIA Skillnet on **Tuesday 7 and Wednesday 8 October 2026**. Both days ran
09:30–16:05 with three breaks. Every time below is taken from the transcript's
own clock; the breaks are the recorded gaps in it.

This is days 1 and 2 of a **six-day programme**. Days 3–6 are not yet in
`source/`, so they are not covered here. Day 2 closes by setting up day 3: the
provision-server skill, a subdomain and server for each participant, and an
automation each participant brings from their own work.

The **Notes §** column is `—` throughout because the participant notes have not
been written yet. Fill it in after `/flesh-out`.

## Session 1 — Day 1 Morning: Foundations and the Reality Check (09:30–11:07)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 1 | 09:30 | 7 | Welcome & Skillnet housekeeping | — | joining; greetings; Skillnet screen |
| 2 | 09:37 | 12 | Trainer introduction & course overview | — | Aidan's background; why AI is good at code (GitHub as training data); writing code was never the hard part; what the six days build — Python automations, a database, a live VPS website |
| 3 | 09:49 | 13 | Participant introductions | — | each participant's role and what they want to automate |
| 4 | 10:02 | 3 | Logistics & Zoom conventions | — | 09:30 start, 11ish break, 12:30–13:30 lunch, 3ish break, finish ~16:00; chat for prompts and links; yes/no reactions that stay up; cameras on |
| 5 | 10:05 | 15 | Reality check: wrong, out of date, non-deterministic | — | "can make mistakes" notice on both tools; countries-in-Europe count differs run to run; Ireland population out of date in Claude, current in ChatGPT; Bulgaria and the Euro as a currency check; vague questions invite drift |
| 6 | 10:20 | 6 | Grounding AI in your own data | — | upload the source rather than ask it to recall; the legislation example; per-project instructions beat one global profile |
| 7 | 10:26 | 9 | Bias, laziness and hallucination | — | training data from the internet; Grok, DeepSeek, Tibet and Tiananmen; the Tesco list — "I can't reliably extract all 160"; asking questions instead of doing the job; invented stores and fake codes; load in the afternoon |
| 8 | 10:35 | 21 | The parts of a prompt | — | context; persona (NLP: neuro-linguistic vs natural language processing); task; constraints; examples; tone; format; shift+return for new lines; keep it short; separate instruction from data — the "Happy Birthday Adam with blue flowers" cake |
| 9 | 10:56 | 6 | Prompts as JSON | — | labelled fields so nothing is forgotten; where web-form input lands; why this matters once prompts are sent programmatically |
| 10 | 11:02 | 5 | Screen check; Claude licence; browser extension | — | font and sound check; who has paid Claude; who has the Chrome extension; a car-hire research task set running over the break |
| — | 11:07 | 23 | Coffee break | — | |

## Session 2 — Day 1 Late Morning: Python and the Command Line (11:30–12:31)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 11 | 11:30 | 6 | The Claude browser extension, reviewed | — | five car-hire options gathered across several sites during the break; constraints (debit card, one week); installing it from the Chrome Web Store; Codex as the ChatGPT equivalent; exercise set for tomorrow |
| 12 | 11:36 | 11 | Python: what it is and installing it | — | general purpose, free, cross-platform, shallow learning curve; download and install; `python --version`; 3.10 or later is fine |
| 13 | 11:47 | 5 | Why automation lives at the command line | — | automating mouse clicks is hard, automating commands is not; the two old options — learn to code, or hire a coder — and why both failed; the third option as this course's hypothesis |
| 14 | 11:52 | 16 | First Python program | — | new chat, prompt for a starter script; paste into a file saved as `.py` in the course folder; watch for `.py.txt`; `cd` to the folder; `python helloworld.py`; tab completion |
| 15 | 12:08 | 17 | Visual Studio Code | — | free, open source, cross-platform, not tied to one technology; open a **folder**, not a file; install the Python extension; the play icon; syntax colouring |
| 16 | 12:25 | 3 | Recap: the roles that remain | — | requirements, specification, project management, testing, sign-off — only the coding is handed over |
| 17 | 12:28 | 3 | Set-up for lunch: Claude sits a Python exam | — | the shift from asking to doing; the extension driving a Udemy practice test unattended |
| — | 12:31 | 59 | Lunch | — | |

## Session 3 — Day 1 Afternoon: Cowork, Files and Images (13:30–14:54)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 18 | 13:30 | 5 | The exam result | — | 100% on the higher-level Python paper; the screenshot-click-screenshot loop; exercise set — bring one use of the extension tomorrow |
| 19 | 13:35 | 3 | Chat versus Cowork | — | the chat sidebar and history; what Cowork adds — reading, writing and copying files on your own machine |
| 20 | 13:38 | 2 | Creating a Cowork project and folder | — | naming it; the permission prompt; allow vs always allow; private to yourself |
| 21 | 13:40 | 11 | Tokens, usage limits, models and effort | — | Cowork costs far more than chat; Settings → usage; the five-hour session window and the weekly limit; Fable 5.1 / Sonnet 5.5 / Haiku 4.5; effort low to max; reasoning versus lookup; cheap models for cheap steps |
| 22 | 13:51 | 4 | Cowork writes a file | — | asking for a PDF; the folder access request; editing the file yourself rather than paying Claude to do it; collaborative ownership of the document |
| 23 | 13:55 | 10 | Slash commands; linking a local folder | — | `/` in the prompt bar; the UI differs between Personal, Professional and Team — "link local folder" vs "add folder"; screen-share troubleshooting |
| 24 | 14:05 | 7 | Cowork reads a file | — | dragging the demo public-sector contract PDF into the folder; asking it to read and summarise; the cyber-security indemnity clause |
| 25 | 14:12 | 13 | Markdown, and why it is cheaper | — | the transcript-to-course-notes workflow; Markdown costs far fewer tokens than Word or PDF; hashes, rules, lists, tables; Ctrl+Shift+V to preview; Ctrl+K then V for side-by-side |
| 26 | 14:25 | 3 | One document at a time | — | asking for notes, trainer manual and outline at once burned the day's tokens; build one, then derive the next from it |
| 27 | 14:28 | 13 | Extracting data from images | — | three invoices of completely different layouts; date format, no currency symbol, output as a table; a real VAT-number error found; two receipts and three VAT rates; the folder-of-invoices job this is heading towards |
| 28 | 14:41 | 5 | Screenshots as input | — | pasting a screenshot instead of describing a problem; "what has gone wrong?" when a set-up step fails |
| 29 | 14:46 | 6 | Fetching live data | — | Wikipedia refuses AI fetches; `api.codingtutor.com` does not; 106 customers saved to `customers.md`, with duplicates and incomplete rows flagged |
| 30 | 14:52 | 2 | Afternoon recap | — | asking versus doing; why image extraction opens automations that always failed before |
| — | 14:54 | 26 | Coffee break | — | |

## Session 4 — Day 1 Late Afternoon: Claude Writing Real Code (15:20–16:05)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 31 | 15:20 | 8 | Claude running commands on your machine | — | asking for the date and time; it runs in a Linux VM, not Windows itself; the hour's difference from daylight saving |
| 32 | 15:28 | 9 | When the settings differ | — | one participant unable to run commands; asking Claude which setting to change; the desktop app must be open and linked; asking AI to guide a set-up even when you know the product |
| 33 | 15:37 | 2 | Command prompt versus PowerShell | — | same job, different everything; stick to `cmd` |
| 34 | 15:39 | 17 | Building a desktop clock | — | an analog clock in Python from one prompt; iteration and the MVP; adding themes — Midnight, Classic, Ocean, Retro; frameless round mode; interrupting and adding to a running request |
| 35 | 15:56 | 4 | A desktop launcher | — | asking it to add a shortcut; the permission box before it touches the desktop; the `.vbs` launcher, with reservations |
| 36 | 16:00 | 5 | Day 1 recap and exercise | — | the change from asking to doing; JSON and Markdown; Python and VS Code; an application now running on the desktop; exercise — bring one real use of the Claude browser extension |

## Session 5 — Day 2 Morning: JSON, REST, CRUD and APIs (09:30–11:03)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 37 | 09:30 | 16 | Homework share-back | — | each participant's use of the browser extension; one logs into a password-protected system with the user's own credentials; the wholesaler who checked resellers' prices every morning — hours down to half an hour; man-weeks of collation across the group |
| 38 | 09:46 | 8 | Command prompt basics | — | `cd` and tab completion; `dir`; directory means folder; running a `.py` file; `cls`; `code .` to open the folder in VS Code |
| 39 | 09:54 | 3 | JSON, seen in the wild | — | `pyclock_settings.json` — mode, width, height, x, y; why the format matters once you talk to AI programmatically |
| 40 | 09:57 | 7 | RESTful web services and APIs | — | the customers endpoint returning JSON; one record by id; 404 for one that is not there; what API stands for and the question to ask of every system you use |
| 41 | 10:04 | 9 | Creating a record | — | POST; asking Claude to prompt you field by field; the `curl` command it hands back; "how will I know if this worked?" before running anything |
| 42 | 10:13 | 9 | Exercise: create your own record | — | write your own, don't copy the trainer's; PowerShell's execution-policy warning; one participant's reusable batch file — the same prompt, a different answer |
| 43 | 10:22 | 11 | CRUD, and updating a record | — | create, retrieve, update, delete; the JSON going up matches the JSON coming back; verifying the change in the browser |
| 44 | 10:33 | 3 | Deleting a record | — | the delete call; 200 means it worked |
| 45 | 10:36 | 10 | Does your CRM have an API? | — | HubSpot with three dummy contacts; asking Claude whether it is possible and how; the two questions to ask an administrator; creating a service key and choosing scopes; copy it now, you will not see it again |
| 46 | 10:46 | 5 | Calling HubSpot with the key | — | the authorization header; the contacts coming back; read-only access is usually enough to ask for; fifteen minutes start to finish with AI guidance |
| 47 | 10:51 | 8 | Environment variables | — | what they are; PATH as the familiar one; setting a token variable so the key is not pasted around; restart the command prompt afterwards; the same technique recurs for AI keys |
| 48 | 10:59 | 4 | Morning recap | — | JSON as the protocol; REST and CRUD; API access as a goldmine — one request against logging in, two-factor, navigating, exporting, opening in Excel |
| — | 11:03 | 26 | Coffee break | — | |

## Session 6 — Day 2 Late Morning: Claude Code and a First Website (11:29–12:31)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 49 | 11:29 | 6 | A project folder and the VS Code terminal | — | a fresh folder opened with `code .`; setting the default terminal profile to Command Prompt rather than PowerShell |
| 50 | 11:35 | 14 | Starting Claude Code | — | running `claude` in the terminal; the trust prompt; when it is not on the PATH — the install command and the `setx PATH` command, pasted into the chat for the group |
| 51 | 11:49 | 8 | Finishing the install and logging in | — | restarting VS Code so the PATH takes; `claude --version`; the browser login |
| 52 | 11:57 | 4 | First commands: /help, /model, /status, /usage | — | slash commands; choosing a model and an effort level; status, usage and stats; 7% of the session used |
| 53 | 12:01 | 2 | The context window | — | roughly a million characters; it is resent with every request; one job per context, then clear it |
| 54 | 12:03 | 4 | Permission modes | — | shift+tab to cycle; auto, manual, accept edits, plan; why plan mode matters once a project has working code to break |
| 55 | 12:07 | 3 | Two windows, two budgets | — | Claude Code for changes to this code; a cheaper Claude chat (or ChatGPT) for how-do-I questions |
| 56 | 12:10 | 11 | Asking Claude to write the prompt | — | "give me a prompt I can use to get started"; the first draft is over-engineered — FastAPI, a database, HTMX, pytest, a git repo; trimming it back to something a beginner can follow; editing beats a blank page |
| 57 | 12:21 | 10 | Claude builds the site | — | reading the plan before approving; Flask, `app.py`, `content.py`, `index.html`, a README; the files appearing; non-determinism means nobody's site matches |
| — | 12:31 | 60 | Lunch | — | |

## Session 7 — Day 2 Afternoon: Iterating, an API, and a Live Server (13:31–14:57)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 58 | 13:31 | 3 | Running the site | — | `python app.py` in a second terminal; 127.0.0.1 as your own machine; port numbers as the extension behind the phone number |
| 59 | 13:34 | 7 | Small changes, and which to make yourself | — | asking for a hero image; the licence check on the image it found; the result not being what was wanted; `content.py` holds the company name — change it by hand and keep the tokens |
| 60 | 13:41 | 12 | Plan mode: the hard-coded copyright year | — | hard-coded versus dynamic; Claude asking the one question that changes the output; reading the plan; the fix; Claude stopping the running server while it works |
| 61 | 13:53 | 10 | /clear and /init | — | clearing the context between features; what is always sent anyway; `/init` writing CLAUDE.md; editing it; project-level instructions instead of one global profile; asking it to update CLAUDE.md as work lands |
| 62 | 14:03 | 12 | Adding a REST API to the site | — | GET returning the course data from a JSON file; telling it the other methods are coming so it builds for that; reading the red and green diff lines |
| 63 | 14:15 | 8 | Testing it properly | — | "it says it ran tests — not good enough"; curl against the courses endpoint and a single course; POSTing a new course and listing again to confirm |
| 64 | 14:23 | 6 | Regrouping | — | hours of work in minutes; no more copy-paste; the job is still to specify and to verify; test-driven thinking — decide in advance how you will know |
| 65 | 14:29 | 6 | A VPS, and connecting with SSH | — | what a cloud VM is; `ssh` to the server; the first-connection fingerprint prompt; it is Linux, not Windows; everything is case-sensitive |
| 66 | 14:35 | 16 | Provisioning the server | — | update the software; the firewall; installing Python 3.12; getting the files up; starting the application; why people pay for hosting, and why that changed |
| 67 | 14:51 | 4 | nginx in front of the app | — | the web server forwarding requests to Python; the site reachable on its IP address |
| 68 | 14:55 | 2 | Cost, and what is coming | — | what the machine costs per month; next session this whole sequence becomes a shareable skill |
| — | 14:57 | 23 | Coffee break | — | |

## Session 8 — Day 2 Late Afternoon: Domains, HTTPS and Deployment (15:20–16:06)

| # | Time | Mins | Segment | Notes § | What to cover |
|---|------|------|---------|---------|---------------|
| 69 | 15:20 | 2 | Why this matters | — | how well Claude interacts with real machines; set it up once, then edit the site in English afterwards |
| 70 | 15:22 | 7 | Domain names and DNS | — | an IP address is marked not secure and nobody can remember it; what DNS does; `nslookup`; adding the record at the registrar; propagation delay |
| 71 | 15:29 | 7 | Subdomains and HTTPS | — | a subdomain lets you experiment without touching the main site; what the S means; running certbot; the email and terms prompts; HTTPS enabled |
| 72 | 15:36 | 6 | SSH keys | — | why an automation cannot type a password at midnight; `ssh-keygen`; the `.pub` key onto the server; logging in without disclosing the password |
| 73 | 15:42 | 8 | Deploying a change from Claude Code | — | asking whether it can reach the server over SSH; it inspects how the site is served; it refuses to overwrite the live data file because the server's copy can drift; confirming the file list before pushing; the change live on the domain |
| 74 | 15:50 | 3 | Does this replace a CMS? | — | thirty years of content management systems; English-language edits to a real site instead |
| 75 | 15:53 | 4 | Updating CLAUDE.md | — | capturing the deployment details; the next session starts informed instead of re-reading every file |
| 76 | 15:57 | 2 | What fills the context window | — | system prompt, tools, MCP instructions, memory files; a warning about installing fifty skills that are all loaded before you say hello |
| 77 | 15:59 | 7 | Next time, and the task to bring | — | the provision-server skill; a subdomain and server each; pick **one** automation, not fifty; email between sessions; the next two days are 2–3 November |
