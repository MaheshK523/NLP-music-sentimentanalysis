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
