# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

<!-- Your criterion. It must name a number. -->

Across each of the three evaluation trials, no more than 1 of 10 pieces of my own writing is labelled high-confidence AI.

**Why this target:**

One false accusation in ten is already serious, but allowing none may be unrealistic for a heuristic detector. I prioritize avoiding accusations against real writers over catching every AI-written submission. The ten test pieces must be writing I actually wrote.

---

## 2.

<!-- Your criterion. -->

In each evaluation trial, the median combined score for at least 5 clearly AI-written samples is at least 0.15 higher than the median combined score for at least 5 pieces of my own writing.

**Why this target:**

The detector does not need to classify every individual text correctly to be useful, but the two groups should show a measurable score difference. Comparing medians makes the target less dependent on one unusually high or low score.

---

## 3.

<!-- Your criterion. -->

In each evaluation trial, the calibration set produces at least one high-confidence human label, one unsure label, and one high-confidence AI label.

**Why this target:**

All three outcomes need to be reachable for the labels to communicate different levels of uncertainty. I use a calibration set with examples I judge clearly human, genuinely borderline, and clearly AI-written.

---

## 4.

<!-- Your criterion. -->

For 3 of 3 appeals submitted with a valid existing `content_id`, the service responds with HTTP 200 and `status: "under_review"`, and the audit log contains an appeal entry for that content.

**Why this target:**

An appeal is the writer's path to challenge a mistaken result. The response confirms that it was accepted, while the audit entry provides a record that can be checked later.

---

## 5.

<!-- Your criterion. -->

In each evaluation trial, requests with missing, empty, non-string, or more than 10,000 characters of `text` return HTTP 400 with a JSON error and do not create a scored decision in the audit log.

**Why this target:**

Malformed or oversized submissions should fail clearly rather than crash the service or receive a misleading authorship label. A 10,000-character limit gives the service a plainly testable boundary; rejected requests should not look like completed decisions.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
