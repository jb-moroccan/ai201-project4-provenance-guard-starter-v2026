"""
Turning two numbers into one, and one number into something a person can read.
← YOU BUILD THIS IN MILESTONES 4 AND 5

`combine_signals` takes the weighted average of the two signal scores, so
disagreement pulls the result toward the middle. `score_to_label` maps the
combined score to a guess and reader-facing message.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Return the weighted average of the two 0–1 signal scores.

    Both inputs point the same way: higher means more likely AI. Your output
    should too. When the signals disagree, averaging moves the result between
    them; an even split between high and low scores lands near unsure.

    Args:
        model_score: from `detector.model_signal` — how predictable the text is.
        style_score: from `stylometry.style_signal` — the shape of the text.

    Returns:
        A float from 0.0 (confidently human) to 1.0 (confidently AI).

    The weights live in config.py. Dividing by their sum keeps this a weighted
    average if the weights are changed, rather than assuming they sum to 1.
    """
    model_weight = config.WEIGHT_MODEL_SIGNAL
    style_weight = config.WEIGHT_STYLE_SIGNAL
    total_weight = model_weight + style_weight
    if total_weight <= 0:
        raise ValueError("Signal weights must sum to a positive value.")

    return (
        model_weight * model_score + style_weight * style_score
    ) / total_weight


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a combined score into a guess and reader-facing message.

    Returns:
        (guess, label_text) — where `guess` is a short machine-readable string
        like "ai" / "human" / "unsure", and `label_text` is the full sentence
        shown to a person.

    Scores at or below HUMAN_THRESHOLD are labeled human; scores at or above
    AI_THRESHOLD are labeled AI. Scores between those thresholds are unsure.
    """
    if score >= config.AI_THRESHOLD:
        return "ai", "We think this was probably written by AI."
    if score <= config.HUMAN_THRESHOLD:
        return "human", "We think this was probably written by a person."
    return (
        "unsure",
        "We couldn’t tell from this sample. It may well have been written by a "
        "person, and this result isn’t a judgment about your work.",
    )


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00–{config.HUMAN_THRESHOLD:.2f} (inclusive)"),
        (
            "unsure",
            f">{config.HUMAN_THRESHOLD:.2f} and <{config.AI_THRESHOLD:.2f}",
        ),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f}–1.00 (inclusive)"),
    ]
