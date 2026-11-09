# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. A writer sends text and a `creator_id` to the service's `POST /submit` route.
2. The route reads the request and assigns the submission a `content_id` so the decision can be found later.
3. The model signal measures how predictable the text is to the local language model and produces a `model_score`.
4. The style signal measures features such as sentence-length variation, vocabulary repetition, and punctuation, producing a `style_score`. It measures the text's shape, not what it means.
5. The combining rule turns the two signal scores into one `combined_score`. If the signals disagree, the rule determines how much that disagreement affects the result.
6. The label mapping turns the combined score into a guess and a reader-facing label: high-confidence human, unsure, or high-confidence AI.
7. The route writes the decision and its scores to the audit log, then returns the content ID, scores, guess, and label to the caller.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** `detector.py` uses a local GPT-2 language model to estimate how predictable the text is, then converts that perplexity into a score from 0 to 1. A higher score means the text is more predictable to the model and is treated as more AI-like.

**Why that might differ between human and AI writing:** A language model tends to choose likely next words, so generated text may be comparatively predictable. Human writing can be less predictable because of unusual wording, specific details, or abrupt changes in direction.

**What it can't see:** Predictability does not prove who wrote the text. Plain, conventional human writing, including writing by English learners or people deliberately using simple language, can also be predictable. Conversely, unusual or ornate AI text may be less predictable. This signal cannot establish authorship or understand the writer's process.

### Signal two — the style signal

**What it measures:** `stylometry.py` measures sentence-length variation and vocabulary repetition (unique words divided by total words). It averages the inverse vocabulary ratio with a normalized inverse sentence-length spread to produce a 0–1 score; higher means more AI-like. Punctuation density is reported as a diagnostic but is not included in the score.

**Why that might differ between human and AI writing:** Generated prose can have relatively even sentence lengths and repeated, conventional vocabulary or punctuation patterns. Human writing often varies more in rhythm and wording. These are tendencies, not reliable rules about individual writers.

**What it can't see:** The style signal cannot understand the content or determine authorship. Editing the surface—adding typos, changing sentence breaks, or inserting a quotation—can change these measurements without changing who wrote the text. Vocabulary repetition also depends on text length, so comparisons across different lengths can mislead. A submission with fewer than two sentences gets a neutral sentence-spread component.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Take the weighted average of the model and style scores. When the signals disagree, the average falls between them, treating disagreement as uncertainty rather than letting either signal decide alone.

**The numbers:** `combined_score = (0.5 × model_score + 0.5 × style_score) / (0.5 + 0.5)`. The weights are in `config.py`. The current thresholds are `0.35` for high-confidence human and `0.65` for high-confidence AI; scores between them are unsure.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

This sample’s signals disagree: the model score is 0.8077, while the style score is 0.3118. Their equal-weight average is 0.55975 (about 0.56), which falls in the unsure range. The disagreement lowers the result instead of letting the high model score alone trigger an AI label. This may avoid some false accusations, though some AI-written text may also receive an unsure result.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35 | We think this was probably written by a person. |
| unsure | above 0.35 and below 0.65 | We couldn’t tell from this sample. It may well have been written by a person, and this result isn’t a judgment about your work. |
| high-confidence AI | 0.65–1.00 | We think this was probably written by AI. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

I wanted the message to be clear that the system couldn’t tell, without making the writer feel blamed for an uncertain result.

---

## Sample Run

<!-- Real terminal requests and responses. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```powershell
$body = '{"text":"In today\u2019s rapidly evolving world, it is essential to recognize that small actions can have a meaningful impact. By working together and embracing new opportunities, we can create positive change and build a brighter future for everyone.","creator_id":"label-test-unsure"}'
Set-Content -Path "$env:TEMP\submit.json" -Encoding ascii -Value $body
curl.exe -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" --data-binary "@$env:TEMP\submit.json"
```

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "combined_score": 0.62305,
  "confidence": 0.5,
  "content_id": "eba9edc6-122b-4729-94d2-18654881f195",
  "guess": "unsure",
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "model_score": 0.7066,
  "style_score": 0.5395,
  "you_sent": {
    "creator_id": "label-test-unsure",
    "text_length": 237
  }
}
```

**An appeal**

```powershell
$body = '{"content_id":"eba9edc6-122b-4729-94d2-18654881f195","reasoning":"I wrote this myself and would like the result reviewed."}'
Set-Content -Path "$env:TEMP\appeal.json" -Encoding ascii -Value $body
curl.exe -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" --data-binary "@$env:TEMP\appeal.json"
```

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "content_id": "eba9edc6-122b-4729-94d2-18654881f195",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```powershell
curl.exe "http://127.0.0.1:5000/log?limit=2"
```

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.62305,
      "content_id": "eba9edc6-122b-4729-94d2-18654881f195",
      "creator_id": "label-test-unsure",
      "guess": "unsure",
      "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
      "model_score": 0.7066,
      "status": "decided",
      "style_score": 0.5395,
      "timestamp": "2026-10-26T21:40:47+00:00"
    },
    {
      "content_id": "eba9edc6-122b-4729-94d2-18654881f195",
      "creator_id": "label-test-unsure",
      "event": "appeal",
      "reasoning": "I wrote this myself and would like the result reviewed.",
      "status": "under_review",
      "timestamp": "2026-10-26T21:49:15+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* Help building the style signal and combining it with the model signal.
- *What came back:* A style score based on sentence-length variation and vocabulary repetition, plus an equal-weight average for combining both scores.
- *What I changed:* I replaced the generic disagreement example with my actual signal scores, 0.8077 and 0.3118, and explained why their average falls in the unsure range.

**Moment 2**

- *What I asked for:* Help writing the `curl` requests for the sample run.
- *What came back:* The first commands worked, but included extra setup that made them harder to follow.
- *What I changed:* I asked for simpler, shorter commands, closer to the examples in the project description.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

Five submissions per minute allows a writer to make a few quick corrections
without making them wait after every request, while slowing a rapid burst of
automated probing. The daily limit of 50 leaves room for legitimate work over
the day but puts a ceiling on sustained requests from the same caller. These
limits are a practical starting point, not a guarantee: a shared caller ID can
affect multiple people, and someone able to change IDs may avoid the limit.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

Requests are limited per `creator_id` when one is
provided. If it is missing or invalid, the service uses the caller's IP
address. This keeps callers with different IDs separate, but also means a
script that changes IDs can get around the limit, while people sharing one ID
can count against each other.

**The run of status codes when I pushed past it:**

15 submissions as `flood_tester` produced 5 successful responses and 10 rate
limit rejections.

<!-- python run_attacks.py --flood 15 -->

```
  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
============================================================
```

**Checking the rejections in the audit log (PowerShell):**

`GET /log` is a web endpoint, not a command to type by itself. With the app
running, call it with `curl.exe` and count the rejected entries:

```powershell
curl.exe "http://127.0.0.1:5000/log?limit=15"
```

The response contains ten entries with `"event": "rejected"` and
`"reason": "rate_limited"`, confirming that all ten `429` responses were
recorded.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `8566155f-ea22-4258-ae5c-9bb50c081472` | human | 0.500 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `9104b632-d974-4583-8745-27e758917534` | human | 0.500 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `396c1490-aad0-4f18-8470-691aa0e3c1c9` | unsure | 0.500 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `64b41e56-01b6-432b-97bc-08b95686e85a` | unsure | 0.500 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `61e34f82-5238-47c8-b297-21a3b204b55b` | human | 0.500 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `f72d3509-ae9c-429a-aa1c-53491dfdba1b` | human | 0.500 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `263addf0-c897-4b5f-b881-9bfe8f5d4695` | unsure | 0.500 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `79e39d81-4bb5-4ed4-b775-2fab971323b7` | human | 0.500 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `7964a525-9ac5-4adc-83bb-4867329c16f0` | unsure | 0.500 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `5d60b8a4-7a11-4d08-8113-277d192a4ff8` | ai | 0.500 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `501a1b04-d264-4aa8-9b0c-e3b2b379ea45` | unsure | 0.500 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `357d556b-c504-4017-82af-5f16dc007868` | unsure | 0.500 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `2ad18d84-3b76-436b-a5ed-2a5fa4f8420a` | unsure | 0.500 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `9589f8b3-2162-4c77-93eb-7c5686b68848` | unsure | 0.500 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `99d3b67e-c78d-4ec3-ab16-f58b7a37926d` | ai | 0.500 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `b083bd0a-ea9b-47e3-aa6a-ee8e6ea65710` | unsure | 0.500 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `e10448b5-72b0-4586-97d5-c6bdb4aa6afe` | unsure | 0.500 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `0032b149-b96a-4222-a6ae-572dd7e914c9` | human | 0.500 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `e3434b0c-1d45-48df-9741-184a68155e24` | human | 0.500 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `a480186c-e14f-4ffa-b7a2-792ee33cb045` | human | 0.500 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `e26daa3b-07ba-4dd3-8348-777d1351a939` | unsure | 0.500 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `b4c0a9b8-6988-4713-891e-a707ae2a3fda` | unsure | 0.500 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `24052d6c-c0a2-49a3-98ff-6e97a15345dd` | unsure | 0.500 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `8a1e9490-69f7-48f2-a719-e55ac753cf2f` | unsure | 0.500 | HELD |
| MF01 | malformed | text is only whitespace | 200 | `c43fe09c-ece0-48a9-af83-93bbaae5fcb7` | unsure | 0.500 | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `0f7a60c4-8466-4650-a534-e87c618db32c` | human | 0.500 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `32e6cd24-b1e0-40a6-8a65-8da47dfaca26` | human | 0.500 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `4f1c58e0-6558-456a-aa6b-abad3bd612c3` | unsure | 0.500 | HELD |
| MF06 | malformed | text is emoji only | 200 | `028a06f8-068d-4297-8693-d216e985cd92` | ai | 0.500 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `3ce9107f-4de1-43f2-8406-b3df0f8791d3` | ai | 0.500 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `e6d5372c-374a-4df2-8d06-300889190a54` | ai | 0.500 | HELD |
| RQ01 | malformed | no text field at all | 500 | `—` | — | — | BROKE |
| RQ02 | malformed | no creator_id | 200 | `04096ff9-91b0-4e90-9d3a-9f460d9c47ac` | human | 0.500 | HELD |
| RQ03 | malformed | text is a number | 500 | `—` | — | — | BROKE |
| RQ04 | malformed | text is a list | 500 | `—` | — | — | BROKE |
| RQ05 | malformed | text is null | 500 | `—` | — | — | BROKE |
| RQ06 | malformed | creator_id is an object | 200 | `963740ba-960c-4a3b-94d2-35fd23920c68` | human | 0.500 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 500 | `—` | — | — | BROKE |
| RQ09 | malformed | body is empty | 500 | `—` | — | — | BROKE |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 500 | `—` | — | — | BROKE |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `223e92dc-df2a-4a77-9600-c8678adbaa17` | human | 0.500 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `13cc48ca-bc4e-4dbc-9570-ef1898bb56fd` | human | 0.500 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `688eaa18-513f-4336-af33-1ea0153cbee1` | human | 0.500 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5c75a1fa-3b01-4314-b15c-d5b4609c3513` | human | 0.500 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4040cca2-5d47-4be7-97ed-1703766ea68f` | human | 0.500 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
[
  {
    "timestamp": "2026-11-05T01:59:24+00:00",
    "content_id": "8566155f-ea22-4258-ae5c-9bb50c081472",
    "creator_id": "attacker_EV01",
    "guess": "human",
    "model_score": 0.1635,
    "style_score": 0.4575,
    "combined_score": 0.3105,
    "label": "We think this was probably written by a person.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T01:59:26+00:00",
    "content_id": "61e34f82-5238-47c8-b297-21a3b204b55b",
    "creator_id": "attacker_EV05",
    "guess": "human",
    "model_score": 0.3212,
    "style_score": 0.1657,
    "combined_score": 0.24345,
    "label": "We think this was probably written by a person.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T01:59:27+00:00",
    "content_id": "79e39d81-4bb5-4ed4-b775-2fab971323b7",
    "creator_id": "attacker_EV08",
    "guess": "human",
    "model_score": 0.2452,
    "style_score": 0.3114,
    "combined_score": 0.2783,
    "label": "We think this was probably written by a person.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T01:59:29+00:00",
    "content_id": "99d3b67e-c78d-4ec3-ab16-f58b7a37926d",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "model_score": 0.8005,
    "style_score": 0.5226,
    "combined_score": 0.66155,
    "label": "We think this was probably written by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T01:59:30+00:00",
    "content_id": "e3434b0c-1d45-48df-9741-184a68155e24",
    "creator_id": "attacker_PI01",
    "guess": "human",
    "model_score": 0.4625,
    "style_score": 0.0916,
    "combined_score": 0.27705,
    "label": "We think this was probably written by a person.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T01:59:30+00:00",
    "content_id": "a480186c-e14f-4ffa-b7a2-792ee33cb045",
    "creator_id": "attacker_PI02",
    "guess": "human",
    "model_score": 0.2044,
    "style_score": 0.0877,
    "combined_score": 0.14605,
    "label": "We think this was probably written by a person.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T01:59:31+00:00",
    "content_id": "c43fe09c-ece0-48a9-af83-93bbaae5fcb7",
    "creator_id": "attacker_MF01",
    "guess": "unsure",
    "model_score": 0.2053,
    "style_score": 0.5,
    "combined_score": 0.35265,
    "label": "We couldn’t tell from this sample. It may well have been written by a person, and this result isn’t a judgment about your work.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T01:59:35+00:00",
    "content_id": "028a06f8-068d-4297-8693-d216e985cd92",
    "creator_id": "attacker_MF06",
    "guess": "ai",
    "model_score": 0.9969,
    "style_score": 0.5,
    "combined_score": 0.7484500000000001,
    "label": "We think this was probably written by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T01:59:36+00:00",
    "content_id": "e6d5372c-374a-4df2-8d06-300889190a54",
    "creator_id": "attacker_MF08",
    "guess": "ai",
    "model_score": 0.9876,
    "style_score": 0.7113,
    "combined_score": 0.84945,
    "label": "We think this was probably written by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T01:59:37+00:00",
    "creator_id": "attacker_flood",
    "event": "rejected",
    "status": "rejected",
    "reason": "rate_limited",
    "limit": "5 per 1 minute"
  }
]
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

```json
[
  {
    "timestamp": "2026-11-05T01:59:29+00:00",
    "content_id": "99d3b67e-c78d-4ec3-ab16-f58b7a37926d",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "model_score": 0.8005,
    "style_score": 0.5226,
    "combined_score": 0.66155,
    "label": "We think this was probably written by AI.",
    "status": "decided"
  }
]
```

FP05 is the worst outcome: the test case is technical documentation written by
a person, but the service labeled it as probably AI-written. Its combined
score was 0.66155, just above the 0.65 AI threshold. That kind of false
accusation is more harmful than an inconclusive result or a rejected burst of
requests because a writer could be wrongly judged based on their writing style.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. ten pieces of my own writing | ≤ 1 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. score spread: my writing followed by AI-written comparisons | AI median ≥ 0.15 | 0.3412 | 0.3412 | 0.3412 | MET |
| 3. label coverage calibration | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. appeal_input | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 5. invalid and oversized text inputs | 4 of 4 | 0/4 | 0/4 | 0/4 | MISSED |

**Trial 1 results for all five criteria**

Criteria 1-3 and 5 below are copied from `results/run_2026-11-09_1729_before.md`. That report records response status and JSON, but does not capture raw HTTP headers. The three criterion 4 appeal responses include their HTTP status and Content-Type headers.

**Criterion 1 - my own writing - Trial 1**

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.533,
    "style_score": 0.2608,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Mr. Franklin\u2019s complaints about his parents may be somewhat unfair and"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.5,
    "model_score": 0.3047,
    "style_score": 0.2217,
    "label": "We think this was probably written by a person.",
    "sent": "Peer influence could have affected Mr. Franklin\u2019s traits he\u2019s experien"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.7078,
    "style_score": 0.2,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Since Mr. Franklin did not receive enough attention from his mother, h"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.7028,
    "style_score": 0.429,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Gender differences in both social connectedness and aggression are inf"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.6518,
    "style_score": 0.4283,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Social connectedness affects gender differences through nature and nur"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.6864,
    "style_score": 0.52,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "To reduce current gender differences in aggression, I would place chil"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.3407,
    "style_score": 0.3775,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "The board member\u2019s proposal to use subliminal persuasion should be rej"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.7407,
    "style_score": 0.5451,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Anthony Greenwald performed an experiment where he randomly assigned s"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.5535,
    "style_score": 0.3777,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Based on the results of this study, the board member\u2019s plan should be "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.7872,
    "style_score": 0.4531,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "While the five human senses have individual functions, they are not to"
  }
]
```

**Criterion 2 - score spread - Trial 1**

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.533,
    "style_score": 0.2608,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Mr. Franklin\u2019s complaints about his parents may be somewhat unfair and"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.5,
    "model_score": 0.3047,
    "style_score": 0.2217,
    "label": "We think this was probably written by a person.",
    "sent": "Peer influence could have affected Mr. Franklin\u2019s traits he\u2019s experien"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.7078,
    "style_score": 0.2,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Since Mr. Franklin did not receive enough attention from his mother, h"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.7028,
    "style_score": 0.429,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Gender differences in both social connectedness and aggression are inf"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.6518,
    "style_score": 0.4283,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Social connectedness affects gender differences through nature and nur"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.6864,
    "style_score": 0.52,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "To reduce current gender differences in aggression, I would place chil"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.3407,
    "style_score": 0.3775,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "The board member\u2019s proposal to use subliminal persuasion should be rej"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.7407,
    "style_score": 0.5451,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Anthony Greenwald performed an experiment where he randomly assigned s"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.5535,
    "style_score": 0.3777,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Based on the results of this study, the board member\u2019s plan should be "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.7872,
    "style_score": 0.4531,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "While the five human senses have individual functions, they are not to"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.9223,
    "style_score": 0.7083,
    "label": "We think this was probably written by AI.",
    "sent": "The sun is bright. The day is nice. The sky is blue. The grass is gree"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.9634,
    "style_score": 0.8542,
    "label": "We think this was probably written by AI.",
    "sent": "The sun is bright. The day is bright. The sky is bright. The grass is "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.9103,
    "style_score": 0.7778,
    "label": "We think this was probably written by AI.",
    "sent": "People need food. People need water. People need rest. People need car"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.9514,
    "style_score": 0.7147,
    "label": "We think this was probably written by AI.",
    "sent": "We can work together. We can learn together. We can grow together. We "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.9395,
    "style_score": 0.8333,
    "label": "We think this was probably written by AI.",
    "sent": "The system is simple. The process is simple. The result is simple. The"
  }
]
```

**Criterion 3 - label coverage - Trial 1**

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.5,
    "model_score": 0.3047,
    "style_score": 0.2217,
    "label": "We think this was probably written by a person.",
    "sent": "Peer influence could have affected Mr. Franklin\u2019s traits he\u2019s experien"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.533,
    "style_score": 0.2608,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "Mr. Franklin\u2019s complaints about his parents may be somewhat unfair and"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.7066,
    "style_score": 0.5395,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "In today\u2019s rapidly evolving world, it is essential to recognize that s"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.9223,
    "style_score": 0.7083,
    "label": "We think this was probably written by AI.",
    "sent": "The sun is bright. The day is nice. The sky is blue. The grass is gree"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.9634,
    "style_score": 0.8542,
    "label": "We think this was probably written by AI.",
    "sent": "The sun is bright. The day is bright. The sky is bright. The grass is "
  }
]
```

**Criterion 4 — appeal responses (Trial 1), from `app.py::appeal`**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "content_id": "f16481e0-f5e6-4ef9-8e75-0ab2a20a755e",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "content_id": "dbfd4441-b69e-443e-a357-3769942301cf",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "content_id": "158e15ba-f0da-41da-b594-470ee7c140b8",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```

**Criterion 5 - invalid and oversized inputs - Trial 1**

```json
[
  {
    "status": null,
    "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
    "sent": "{\"creator_id\": \"eval_missing_text\"}"
  },
  {
    "status": null,
    "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
    "sent": "(empty text)"
  },
  {
    "status": null,
    "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
    "sent": "{\"text\": 12345, \"creator_id\": \"eval_non_string_text\"}"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.9976,
    "style_score": 0.25,
    "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
    "sent": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  }
]
```

**Diagnoses**

Criterion 5 failed at the **route/input-validation stage**. `/submit` uses an
empty string when `text` is missing and passes empty or non-string values to
the scoring signals without validating them first. The three invalid requests
therefore produced responses the evaluator could not parse as JSON instead of
the required HTTP 400 JSON errors. The 10,001-character request was not
rejected: it received HTTP 200, was scored, and was recorded in the audit log
with status `decided`. The route has no 10,000-character limit, so malformed
inputs can fail inside scoring while oversized input is treated as a normal
submission.

---

## The Improvement

**What I changed:** I added input checks to `app.py::submit` before either
scoring signal runs. Missing, empty (including whitespace-only), and
non-string `text` values now receive an HTTP 400 JSON error. Each is recorded
as a rejected audit entry, not a scored decision. I did not add a text-length
limit.

**Which diagnosis pointed at it:** Criterion 5 failed at the route/input-
validation stage because `/submit` passed malformed text to the signals. I
validate the request before calling them.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `d9940965-62ea-4d2d-9a74-678ca4660e89` | human | 0.500 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `a8fd0356-2598-48e3-bab3-bdd71ea2befc` | human | 0.500 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `aa9eb21c-9879-4b21-9fd1-d40d3a6e5729` | unsure | 0.500 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `fc17034c-3340-41a3-954a-ffa85f2cbcfa` | unsure | 0.500 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `cf77a947-98f7-4cdf-9a81-933cd2b2b8e3` | human | 0.500 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `2646bc98-8312-4dc6-b5bb-42e9bfa1b648` | human | 0.500 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `a83f35d3-aff1-44b2-a0ad-ea87e580ff71` | unsure | 0.500 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `5a780dee-d3e9-4256-a5a2-2f1633a7a0a0` | human | 0.500 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `220da3ff-8fd0-415a-ba6e-904b9d21c80f` | unsure | 0.500 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `605b979f-08af-4771-8d44-83aec6d9dfcb` | ai | 0.500 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `7e580a41-351b-4c81-b594-56c7a0c34b99` | unsure | 0.500 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `b94cdc47-7773-4fe8-9138-1807165198aa` | unsure | 0.500 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `daf43b52-46a4-48be-b949-0b4a8695ff21` | unsure | 0.500 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `2daf6f8f-9116-4e63-b74b-64a3d20e8239` | unsure | 0.500 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `847435c7-ee4e-422a-b3e2-18909675a929` | ai | 0.500 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `2f82a0d2-5d7d-4aca-bb5c-b369050e66d4` | unsure | 0.500 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `3987c95f-664c-4f13-8237-e2c130ef089d` | unsure | 0.500 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `37f8cb28-ff69-40f7-9430-606595088c9b` | human | 0.500 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `62f6c178-53cc-40d1-8572-bdefc9104e2e` | human | 0.500 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `46c8a367-7a3c-47b1-93e5-4a3e970e8215` | human | 0.500 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `a0aeb000-97d5-47dc-b4be-2e7ebbf3b972` | unsure | 0.500 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `d03bdddd-1fa9-45c4-a599-c18ffd5f662f` | unsure | 0.500 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `62dd8aa0-6973-40d3-9890-78805e750d8a` | unsure | 0.500 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `de277add-ebf0-4d93-a923-530c9a65d2a7` | unsure | 0.500 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `53c2e33a-5ea3-477a-ba94-04414325ba40` | human | 0.500 |  |
| MF04 | malformed | text is only punctuation | 200 | `492c130d-1a05-4e57-8d8f-6d850e4240f3` | human | 0.500 |  |
| MF05 | malformed | text is a very long single word | 200 | `20fc3caa-8cb3-45b0-8f3e-8c1bfd2fc7ea` | unsure | 0.500 |  |
| MF06 | malformed | text is emoji only | 200 | `f6654b52-0fd8-4ab4-a592-353be3da986b` | ai | 0.500 |  |
| MF07 | malformed | text is right-to-left script | 200 | `abf9586f-59a7-496b-9d32-740142092bdd` | ai | 0.500 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `2e958db0-e883-4bd6-ae3a-2affefff44aa` | ai | 0.500 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `d7c80e69-fa09-4db7-a17a-815aa608b168` | human | 0.500 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `4d7aba7a-f6e0-4e9e-98af-ff56f63a3757` | human | 0.500 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `614b7a96-2788-4f6e-8579-b81f886a67c1` | human | 0.500 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c8d04541-2434-4a69-b4a6-1853675a55b7` | human | 0.500 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `10d3f007-f44d-4ed4-8615-38066556a31e` | human | 0.500 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b7081683-d486-4a53-986e-38d3334dc78b` | human | 0.500 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `17a041c8-2490-48a9-a739-bd5c5068ac41` | human | 0.500 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

**Did it help, and how do I know:**

Yes, it fixed the missing, empty, and non-string input cases: the
`run_2026-11-09_1815_after.md` report shows HTTP 400 for all three in each
trial, while the 10,001-character input still returned HTTP 200. A focused
route test also confirmed the three 400 responses contain JSON errors, are
logged as rejections without score fields, and do not call either scoring
signal. The improvement helped, but criterion 5 remains MISSED overall because
the oversized input is still accepted.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. ten pieces of my own writing | ≤ 1 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. score spread: my writing followed by AI-written comparisons | AI median ≥ own median + 0.15 | 0.3412 gap | 0.3412 gap | 0.3412 gap | MET |
| 3. label coverage calibration | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. appeal_input | 3 of 3 appeals | 3/3 | 3/3 | 3/3 | MET |
| 5. invalid and oversized text inputs | 4 of 4 | 3/4 | 3/4 | 3/4 | MISSED |

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

The classification failures occur in the **signal-scoring and decision
stages**, not because the route is assigning labels directly. The equal-weight
average in `scoring.py::combine_signals` lets a manipulated or weak signal pull
the result across the `0.35` human threshold:

- **EV01** is driven humanward by the model signal: typos make the AI-written
  text less predictable, producing a low model score (`0.1635`) despite a
  higher style score (`0.4575`); the average is `0.3105`. **EV05** changes both
  signals through heavy editing (`0.3212` model, `0.1657` style; average
  `0.24345`), so neither signal retains enough evidence of generated text.
- **EV02** and **EV06** show the style signal's evasion mechanism: sentence
  restructuring produces very low style scores (`0.0879` and `0.125`) that
  outweigh moderately AI-like model scores (`0.5943` and `0.5727`) in the
  equal-weight average. Their combined scores (`0.3411` and `0.34885`) fall
  just below the human threshold. **EV08** is only a short sample, but the
  route applies no minimum-evidence rule: the model score is `0.2452`, style
  score `0.3114`, and average `0.2783`, so weak short-text evidence is labeled
  human rather than treated as inconclusive.
- **PI01** and **PI02** are also signal-scoring failures, not instructions
  successfully changing control flow. The service does not pass submissions
  to an instruction-following prompt; both signals score the injected text as
  ordinary prose. Its predictable wording and simple/repetitive shape produce
  low style scores (`0.0916` and `0.0877`); combined with model scores of
  `0.4625` and `0.2044`, the averages (`0.27705` and `0.14605`) are labeled
  human. Neither signal detects or discounts the embedded classification
  instruction.
- **FP05** fails in the opposite direction at model-signal calibration and
  thresholding. Formulaic technical prose receives a high model score
  (`0.8005`), already above the AI threshold; the style score (`0.5226`) is
  near neutral and does not offset it enough. Their average, `0.66155`, still
  crosses the `0.65` threshold and falsely labels a human writer's work as AI.

Across these cases, the mechanism is that surface features and predictability
are imperfect authorship proxies, and the weighted average has no mechanism
for recognizing when evidence is weak or adversarially shifted.

Two failures remain at the **route/input-validation stage**. **MF02**, a
one-character submission, returned HTTP 500 because the route accepts any
non-empty string, then the detector raises `ValueError` when it has fewer than
three tokens; the route does not catch that short-input failure and return a
client error. Criterion 5 is still missed because the 10,001-character
submission returns HTTP 200 and is recorded as a scored decision: the route
has no maximum-length check. I deliberately left the minimum-length handling
and size limit unchanged after fixing the other malformed-input cases.

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

I would favor avoiding false accusations: uncertain cases should stay `unsure`
instead of being called AI, even if that lets more AI-written text pass. Writers
whose AI-written work is not detected would pay that cost, while human writers
would be less likely to face a false accusation.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [X] criteria.md has five numbered criteria, each naming a target
       [X] Each has a reason underneath
       [X] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [X] Two signals that measure DIFFERENT things, each with a named blind spot
       [X] Three label variants, all reachable, written out in full
       [X] POST /appeal changes status and writes to the log
       [X] Signals and Scoring names scoring.py::combine_signals
       [X] Sample Run: a submission AND an appeal, as pasted text
       [X] At least four new commits
       [X] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [X] Rate limiting on /submit, with your numbers justified
       [X] The pasted run of status codes showing 429
       [X] Audit log with all nine fields, recording rejections too
       [X] The attack set run IN FULL, every input with an outcome
       [X] Ten audit log entries pasted as text
       [X] Five criteria across three trials
       [X] A diagnosis for every miss and every broken attack — stage AND mechanism
       [X] One improvement, with Attack Run — After
       [X] What's Still Broken, including the production trade
       [X] At least four new commits
       [X] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
