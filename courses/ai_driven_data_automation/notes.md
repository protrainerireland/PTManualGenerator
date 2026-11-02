<!-- toc -->

# AI-Driven Data Automation — Participant Reference Manual

## 1. What to watch for when you use AI

The whole of this course leans on an AI assistant. It guides us through Power Query, it writes our formulas, and in the last session it writes a small program for us. So it is worth a few minutes at the start on what these tools get wrong, and how you would notice.

None of what follows is a reason not to use them. They are extraordinarily good, and they have access to more information than any of us. But the raw material behind every answer is material from the internet, and the internet has no editor. **Nothing that comes out of an AI assistant should be used without checking it.**

You can follow all of this yourself. Open **ChatGPT** (chatgpt.com) in one browser tab and **Microsoft Copilot** (copilot.microsoft.com) in another, side by side. Everything in this section works on the free version of either.

<!-- screenshot needed: ChatGPT and Copilot side by side, each showing its numbered list of European countries with the two different totals. -->

### 1.1 It can be wrong, and you can prove it in a minute

1. In **ChatGPT**, type:

   *Can you give me a numbered list of the countries in Europe.*

2. Type the same thing into **Copilot**.
3. Count what each one gives you.

On the day, one assistant returned 51 countries and the other said it was giving 50 — and then listed 51. Neither is obviously right, because "Europe" is open to interpretation: some people mean the EU, some include Britain, Iceland and Switzerland, some count Monaco and the Vatican, and then there are the transcontinental countries. The assistants do not ask which you meant; they simply decide.

Both tools say so themselves, in small print under the box: **"ChatGPT can make mistakes"** and **"AI-generated content may be incorrect."**

Asking the same question of two different assistants and comparing the answers is the cheapest check you have. Use it any time an answer matters.

### 1.2 Where the answers come from

Every AI assistant is built by pushing an enormous body of text through it — its *corpus* of training data — after which it is ready to answer questions. The vast majority of that text comes from the internet.

Roughly a quarter of what these tools answer with traces back to Wikipedia, which is a resource most of us would trust. Roughly another quarter traces back to Reddit, which is not. You do not need to know how the technology works — we do not need to know how a power station works to turn on a light — but you do need to remember where the raw material came from: a public resource with no master editor.

### 1.3 You often cannot see where an answer came from

Ask either tool where it got something and you may or may not get an answer. Copilot is a little better than ChatGPT at citing the websites it used; some days it lists them, other days it lists nothing at all.

So the information might be wrong, and you frequently cannot check *how* it was arrived at — only whether the result itself stands up.

### 1.4 It may be out of date

Carry on in the same chat:

*Can you give me the list again and include the currency and population of each country.*

Three things to look at in what comes back:

- **Ireland's population.** One assistant gave 5.5 million, the other 5.4 million. The CSO figure, updated for the budget, is 5.56 million. If you are a student doing a geography project, 5.4 million is fine. If you are the Minister for Finance, you should try harder.
- **Bulgaria's currency.** Bulgaria adopted the euro at the start of this year, and until roughly June or July both tools were still reporting the Bulgarian lev. Croatia joined the euro in January 2023, and it was 2025 before either tool would reliably say so.
- **France's population.** One gave 68.7 million and the other 66.7 million — two million apart. A delegate on an earlier course chased this down: one figure includes the overseas territories and the other is mainland France only. There is usually a reason for a discrepancy, but you have to go and find it.

### 1.5 It may be biased

The material these tools were trained on carries the views of whoever wrote it, and the tools treat all of it as equal.

Americans will tell you ChatGPT and Copilot lean a little Democrat. **Grok**, which is owned by Elon Musk, leans Republican. **DeepSeek**, the Chinese assistant, follows the Chinese Communist Party line on geopolitical and historical questions and will say nothing bad about China — including on the status of Taiwan and Tibet.

Little of today's work is exposed to that, but if you use AI for anything with a political or historical dimension, fact-check it properly.

### 1.6 The same question does not give the same answer twice

A *deterministic* system is one where the output follows from the input: the same figures on Monday and on Friday produce the same accounts, assuming the rules have not changed. Accountants rely on that, and so do programmers.

AI assistants are not deterministic. Ask for the countries of Europe on consecutive days and the count moves: 47, 48, 49, 50, 51 — as high as 53 and as low as 41. Type the same question as the person beside you and you will not necessarily get the same answer.

This matters for everything that follows. **If you repeat an exercise from these notes, the formula or the step-by-step instructions you get back may differ from the ones printed here.** That is normal. Test whatever you are given.

### 1.7 Busy days are bad days

In October 2022 ChatGPT had no users at all. It now serves more than 150 million a day. OpenAI publishes its own status page, which shows about 99.7% uptime — impressive, and not the same as always.

When the system is under load, four things happen:

1. It is slower to answer.
2. It cuts corners — the same question that produced a long, careful answer in the morning produces a short, sloppy one in the afternoon.
3. It leaves things out — ask for a list of 50 and get 47, with no indication anything is missing.
4. It hallucinates: it invents an answer.

Here is the hallucination the course uses, which you can try yourself:

*Can you give me a list of all of the Tesco stores in Ireland.*

The answer came back confident and well organised: 160 stores, too many to list at once, grouped by county. It is also partly fiction. There is no Tesco in Kinsale. There is no Tesco in Glanmire. The one listed for Blackpool is a Dunnes.

Afternoons are worse than mornings, because that is when the United States comes online. You will see this again in Session 4 of this course, where three poor answers in a row from one assistant were enough to switch to the other.

### 1.8 It is not trying to give you the right answer

This is the sentence worth taking away: an AI assistant is not trying to give you the correct answer. It is trying to give you **the answer it thinks you want to hear**, based on what it has picked up about you.

That is why a confident, well-formatted, completely wrong answer is so easy to produce — and why "it sounded right" is not a check.

### 1.9 Start a new chat for each new topic

Everything you type in a chat becomes *context*, and colours every answer after it. The longer a chat runs, the more it is answering the version of you it has assembled.

A real example: ask it once to rewrite a formula for an older version of Excel, say Excel 2016, and from that point on every formula in that chat comes back written for Excel 2016 — without the newer functions you were expecting, and without saying so.

So:

1. Finish a piece of work, change topic, or start something unrelated — **start a new chat**.
2. Do not leave one chat running all week. It happens; it is visible from across an office; and the answers drift.

The paid versions also have a **memory** feature that carries facts between chats. It is useful in day-to-day work — it can learn your defaults — but keep an eye on what it has remembered. One stray fact about Excel 2016 in there colours answers for good. (The version used in class has memory switched off, otherwise none of the examples above would misbehave on cue.)

### 1.10 What this means for the rest of the day

For every answer that matters:

- Check it. Due diligence is not optional, and it is the part of the job that has not been automated.
- Compare two assistants when you are unsure.
- Sanity-check a few rows by hand rather than trusting a total.
- Expect different wording, and sometimes a different formula, from the ones in these notes.
- Treat it as a capable assistant, not an infallible oracle. Most of the trouble people get into with these tools comes from pasting an answer onward without reading it.
