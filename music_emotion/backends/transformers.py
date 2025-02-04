from __future__ import annotations

import math
from collections import defaultdict
from typing import Any, Iterable, Mapping

from ..chunking import tokenizer_chunks
from ..errors import BackendUnavailableError
from ..models import BackendPrediction


DEFAULT_MODEL = "j-hartmann/emotion-english-distilroberta-base"


def _average(items: Iterable[tuple[Mapping[str, float], int]]) -> dict[str, float]:
    totals: defaultdict[str, float] = defaultdict(float)
    total_weight = 0
    for scores, weight in items:
        safe_weight = max(int(weight), 1)
        total_weight += safe_weight
