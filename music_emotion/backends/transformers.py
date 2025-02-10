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
        for label, score in scores.items():
            totals[label.casefold()] += float(score) * safe_weight
    if not totals or total_weight < 1:
        raise BackendUnavailableError("the Transformers backend returned no emotion scores")
    averaged = {label: value / total_weight for label, value in totals.items()}
    total = sum(averaged.values())
    if not math.isfinite(total) or total <= 0:
        raise BackendUnavailableError("the Transformers backend returned invalid emotion scores")
    return {label: value / total for label, value in sorted(averaged.items())}


class TransformersEmotionBackend:
    name = "transformers"

    def __init__(self, model_name: str = DEFAULT_MODEL, *, allow_download: bool = False) -> None:
        try:
            from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
        except ImportError as exc:
            raise BackendUnavailableError(
                "Transformers support is optional. Install it with "
