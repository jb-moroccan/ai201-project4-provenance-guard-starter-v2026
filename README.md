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

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



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
