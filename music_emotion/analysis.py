from __future__ import annotations

import math
from collections.abc import Iterable, Iterator, Mapping

from .backends.base import EmotionBackend
from .errors import DataValidationError
from .models import AnalysisResult, SongRecord


def _validated_scores(scores: Mapping[str, float]) -> dict[str, float]:
    if not scores:
        raise DataValidationError("backend returned no scores")
    normalized: dict[str, float] = {}
    for raw_label, raw_score in scores.items():
        label = str(raw_label).strip().casefold()
        score = float(raw_score)
        if not label or not math.isfinite(score) or score < 0:
            raise DataValidationError("backend returned an invalid label or score")
        normalized[label] = normalized.get(label, 0.0) + score
