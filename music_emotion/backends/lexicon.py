from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Mapping

from ..chunking import tokenize_words, word_chunks
from ..models import BackendPrediction


EMOTIONS = ("anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise")

LEXICON: dict[str, tuple[tuple[str, float], ...]] = {
    "afraid": (("fear", 1.5),),
    "amazed": (("surprise", 1.4), ("joy", 0.4)),
    "angry": (("anger", 1.6),),
    "bright": (("joy", 1.0),),
    "broken": (("sadness", 1.4),),
    "burn": (("anger", 1.0),),
    "calm": (("neutral", 1.0), ("joy", 0.3)),
    "celebrate": (("joy", 1.5),),
    "cry": (("sadness", 1.5),),
    "dance": (("joy", 1.2),),
    "danger": (("fear", 1.3),),
    "dark": (("fear", 0.8), ("sadness", 0.5)),
    "disgust": (("disgust", 1.8),),
    "empty": (("sadness", 1.1),),
    "fear": (("fear", 1.6),),
    "fight": (("anger", 1.1),),
    "filthy": (("disgust", 1.3),),
    "free": (("joy", 1.0),),
    "fury": (("anger", 1.7),),
    "glad": (("joy", 1.4),),
    "gone": (("sadness", 0.9),),
    "grief": (("sadness", 1.8),),
    "happy": (("joy", 1.6),),
    "hate": (("anger", 1.4), ("disgust", 0.5)),
    "haunted": (("fear", 1.4),),
    "hope": (("joy", 1.2),),
    "joy": (("joy", 1.7),),
    "lightning": (("surprise", 1.0), ("fear", 0.3)),
    "lonely": (("sadness", 1.5),),
    "love": (("joy", 1.5),),
    "nightmare": (("fear", 1.8),),
    "ordinary": (("neutral", 1.0),),
    "panic": (("fear", 1.8),),
    "poison": (("disgust", 1.0), ("fear", 0.5)),
    "quiet": (("neutral", 0.9),),
    "rage": (("anger", 1.8),),
    "rotten": (("disgust", 1.5),),
    "sad": (("sadness", 1.6),),
    "scared": (("fear", 1.6),),
    "shame": (("disgust", 0.7), ("sadness", 0.7)),
    "sick": (("disgust", 1.1),),
    "simple": (("neutral", 0.8),),
    "smile": (("joy", 1.4),),
    "sorrow": (("sadness", 1.7),),
    "steady": (("neutral", 1.0),),
    "sudden": (("surprise", 1.2),),
    "sunrise": (("joy", 1.2),),
    "surprise": (("surprise", 1.7),),
    "tears": (("sadness", 1.5),),
    "tremble": (("fear", 1.3),),
    "unexpected": (("surprise", 1.5),),
    "vile": (("disgust", 1.6),),
    "warm": (("joy", 0.9),),
    "wonder": (("surprise", 1.0), ("joy", 0.5)),
    "wow": (("surprise", 1.6),),
}

NEGATIONS = {"aren't", "can't", "didn't", "doesn't", "don't", "never", "no", "not", "wasn't", "won't"}
INTENSIFIERS = {"deeply": 1.35, "extremely": 1.65, "really": 1.25, "so": 1.2, "very": 1.4}
NEGATION_TARGETS = {
    "anger": "fear",
    "disgust": "neutral",
    "fear": "neutral",
    "joy": "sadness",
    "neutral": "surprise",
    "sadness": "joy",
    "surprise": "neutral",
}


def _normalize(raw: Mapping[str, float]) -> dict[str, float]:
    total = sum(max(float(raw.get(emotion, 0.0)), 0.0) for emotion in EMOTIONS)
    if total <= 0:
        return {emotion: (1.0 if emotion == "neutral" else 0.0) for emotion in EMOTIONS}
    return {emotion: max(float(raw.get(emotion, 0.0)), 0.0) / total for emotion in EMOTIONS}


def _score_chunk(text: str) -> dict[str, float]:
    words = tokenize_words(text)
    raw = {emotion: 0.04 for emotion in EMOTIONS}
    raw["neutral"] = 0.20

    for index, word in enumerate(words):
        entries = LEXICON.get(word, ())
        if not entries:
            continue
        multiplier = INTENSIFIERS.get(words[index - 1], 1.0) if index else 1.0
        context = words[max(0, index - 2) : index]
        negated = any(token in NEGATIONS for token in context)
        for emotion, weight in entries:
            target = NEGATION_TARGETS[emotion] if negated else emotion
            raw[target] += weight * multiplier

    raw["surprise"] += min(text.count("!") * 0.10 + text.count("?") * 0.05, 0.4)
    return _normalize(raw)


def _weighted_average(items: Iterable[tuple[Mapping[str, float], int]]) -> dict[str, float]:
