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
    total = sum(normalized.values())
    if total <= 0:
        raise DataValidationError("backend score total must be positive")
    return {label: value / total for label, value in sorted(normalized.items())}


def select_dominant_emotions(scores: Mapping[str, float], threshold: float) -> tuple[str, ...]:
    if not 0.0 <= threshold <= 1.0:
        raise DataValidationError("threshold must be between 0 and 1")
    validated = _validated_scores(scores)
    selected = [label for label, score in validated.items() if score >= threshold]
    if not selected:
        selected = [min(validated, key=lambda label: (-validated[label], label))]
    return tuple(sorted(selected, key=lambda label: (-validated[label], label)))


def analyze_records(
    records: Iterable[SongRecord],
    backend: EmotionBackend,
    *,
    threshold: float = 0.25,
    chunk_size: int = 256,
) -> Iterator[AnalysisResult]:
    if chunk_size < 2:
        raise DataValidationError("chunk size must be at least 2")
    for song in records:
        prediction = backend.predict(song.lyrics, chunk_size=chunk_size)
        scores = _validated_scores(prediction.scores)
        yield AnalysisResult(
            song=song,
            dominant_emotions=select_dominant_emotions(scores, threshold),
            emotion_scores=scores,
            backend=backend.name,
            model=backend.model_name,
            chunk_count=prediction.chunk_count,
        )
