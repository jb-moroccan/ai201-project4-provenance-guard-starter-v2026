# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-09 18:13
- Auto-marked BROKE (5xx, crash, no response): **1**
- Left for you to judge: **55**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

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

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 1 | 19 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "d9940965-62ea-4d2d-9a74-678ca4660e89",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.1635,
  "style_score": 0.4575,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "a8fd0356-2598-48e3-bab3-bdd71ea2befc",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.5943,
  "style_score": 0.0879,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "aa9eb21c-9879-4b21-9fd1-d40d3a6e5729",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6662,
  "style_score": 0.2846,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "fc17034c-3340-41a3-954a-ffa85f2cbcfa",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6114,
  "style_score": 0.4479,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "cf77a947-98f7-4cdf-9a81-933cd2b2b8e3",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.3212,
  "style_score": 0.1657,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "2646bc98-8312-4dc6-b5bb-42e9bfa1b648",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.5727,
  "style_score": 0.125,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "a83f35d3-aff1-44b2-a0ad-ea87e580ff71",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5862,
  "style_score": 0.3634,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "5a780dee-d3e9-4256-a5a2-2f1633a7a0a0",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.2452,
  "style_score": 0.3114,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "220da3ff-8fd0-415a-ba6e-904b9d21c80f",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.7042,
  "style_score": 0.2649,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "605b979f-08af-4771-8d44-83aec6d9dfcb",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9792,
  "style_score": 0.5771,
  "label": "We think this was probably written by AI.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "7e580a41-351b-4c81-b594-56c7a0c34b99",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6175,
  "style_score": 0.3406,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "b94cdc47-7773-4fe8-9138-1807165198aa",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.7387,
  "style_score": 0.4845,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "daf43b52-46a4-48be-b949-0b4a8695ff21",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8051,
  "style_score": 0.4198,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "2daf6f8f-9116-4e63-b74b-64a3d20e8239",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8329,
  "style_score": 0.3511,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "847435c7-ee4e-422a-b3e2-18909675a929",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.8005,
  "style_score": 0.5226,
  "label": "We think this was probably written by AI.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "2f82a0d2-5d7d-4aca-bb5c-b369050e66d4",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8814,
  "style_score": 0.2867,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "3987c95f-664c-4f13-8237-e2c130ef089d",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8816,
  "style_score": 0.2839,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "37f8cb28-ff69-40f7-9430-606595088c9b",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.3223,
  "style_score": 0.2113,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "62f6c178-53cc-40d1-8572-bdefc9104e2e",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.4625,
  "style_score": 0.0916,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "46c8a367-7a3c-47b1-93e5-4a3e970e8215",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.2044,
  "style_score": 0.0877,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "a0aeb000-97d5-47dc-b4be-2e7ebbf3b972",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5943,
  "style_score": 0.3168,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "d03bdddd-1fa9-45c4-a599-c18ffd5f662f",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.4998,
  "style_score": 0.3042,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "62dd8aa0-6973-40d3-9890-78805e750d8a",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6401,
  "style_score": 0.2024,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "de277add-ebf0-4d93-a923-530c9a65d2a7",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5583,
  "style_score": 0.3491,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "53c2e33a-5ea3-477a-ba94-04414325ba40",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.25,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "492c130d-1a05-4e57-8d8f-6d850e4240f3",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "20fc3caa-8cb3-45b0-8f3e-8c1bfd2fc7ea",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.9976,
  "style_score": 0.25,
  "label": "We couldn\u2019t tell from this sample. It may well have been written by a person, and this result isn\u2019t a judgment about your work.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "f6654b52-0fd8-4ab4-a592-353be3da986b",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We think this was probably written by AI.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "abf9586f-59a7-496b-9d32-740142092bdd",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We think this was probably written by AI.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "2e958db0-e883-4bd6-ae3a-2affefff44aa",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9876,
  "style_score": 0.7113,
  "label": "We think this was probably written by AI.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "d7c80e69-fa09-4db7-a17a-815aa608b168",
  "creator_id": null,
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.2395,
  "style_score": 0.25,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "4d7aba7a-f6e0-4e9e-98af-ff56f63a3757",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0492,
  "style_score": 0.25,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "614b7a96-2788-4f6e-8579-b81f886a67c1",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c8d04541-2434-4a69-b4a6-1853675a55b7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "10d3f007-f44d-4ed4-8615-38066556a31e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "b7081683-d486-4a53-986e-38d3334dc78b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "17a041c8-2490-48a9-a739-bd5c5068ac41",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
