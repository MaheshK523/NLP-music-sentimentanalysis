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
