"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

The measures below describe surface features, not authorship. The style score
combines sentence-length spread and vocabulary repetition. Punctuation density
is reported as a diagnostic, but is not included in the score because density
alone has no reliable human-versus-AI direction.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── Surface measures ─────────────────────────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    Sentence-length coefficient of variation (sample stdev / mean).

    Returns:
    A non-negative float. Zero means the sentences have equal lengths or
    there is not enough text to measure a spread.
    """
    lengths = []
    for sentence in sentences(text):
        sentence_length = len(words(sentence))
        if sentence_length:
            lengths.append(sentence_length)
    if len(lengths) < 2:
        return 0.0

    mean_length = statistics.mean(lengths)
    if mean_length == 0:
        return 0.0
    return statistics.stdev(lengths) / mean_length


def type_token_ratio(text: str) -> float:
    """
    Unique words divided by total words.

    Returns:
    A float between 0 and 1. Higher means more varied vocabulary. This
    simple ratio tends to fall as text gets longer.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def punctuation_density(text: str) -> float:
    """
    Punctuation characters per word.

    Returns:
    A non-negative float. This is reported for inspection, but not used in
    the style score because punctuation density alone has no reliable
    direction as an authorship signal.
    """
    import unicodedata

    tokens = words(text)
    if not tokens:
        return 0.0
    punctuation_count = sum(
        1 for character in text
        if unicodedata.category(character).startswith("P")
    )
    return punctuation_count / len(tokens)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    Combine normalized style features into a 0–1 score; higher means more AI-like.

    Sentence-length variation is scaled so a coefficient of variation of 0.75
    or more maps to the most human-like end. Low variation is more AI-like.
    Vocabulary repetition is represented by 1 - type-token ratio. If the text
    has fewer than two sentences, sentence variation contributes a neutral
    0.5 rather than treating missing evidence as an AI-like pattern.
    """
    tokens = words(text)
    if not tokens:
        return 0.5

    sentence_parts = sentences(text)
    nonempty_sentence_count = sum(bool(words(sentence)) for sentence in sentence_parts)
    if nonempty_sentence_count < 2:
        spread_score = 0.5
    else:
        spread_score = 1.0 - min(sentence_length_spread(text) / 0.75, 1.0)

    repetition_score = 1.0 - type_token_ratio(text)
    return round((spread_score + repetition_score) / 2.0, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
