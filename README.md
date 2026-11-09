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

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
