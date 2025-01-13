from __future__ import annotations

import html
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .errors import DataValidationError
from .io import load_songs
from .models import AnalysisResult


@dataclass(frozen=True, slots=True)
class ReportArtifacts:
    html: Path
    markdown: Path
    summary_json: Path


def _parse_json_value(value: Any, expected: type, field: str, row: int | None) -> Any:
    parsed = value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise DataValidationError(f"row {row}: {field} must contain valid JSON") from exc
    if not isinstance(parsed, expected):
        raise DataValidationError(f"row {row}: {field} must be a JSON {expected.__name__}")
    return parsed


def load_analysis_results(path: str | Path, *, input_format: str = "auto") -> list[AnalysisResult]:
    songs = load_songs(path, input_format=input_format)
    results: list[AnalysisResult] = []
    for song in songs:
        missing = [field for field in ("dominant_emotions", "emotion_scores") if field not in song.extra]
        if missing:
            raise DataValidationError(f"row {song.source_row}: missing analysis field(s): {', '.join(missing)}")
        dominant = _parse_json_value(song.extra["dominant_emotions"], list, "dominant_emotions", song.source_row)
        scores = _parse_json_value(song.extra["emotion_scores"], dict, "emotion_scores", song.source_row)
        if not dominant or not all(isinstance(label, str) and label.strip() for label in dominant):
            raise DataValidationError(f"row {song.source_row}: dominant_emotions must contain labels")
        clean_scores: dict[str, float] = {}
        for label, value in scores.items():
            try:
                score = float(value)
            except (TypeError, ValueError) as exc:
                raise DataValidationError(f"row {song.source_row}: invalid score for {label!r}") from exc
            if not math.isfinite(score) or not 0 <= score <= 1:
                raise DataValidationError(f"row {song.source_row}: scores must be finite values from 0 to 1")
            clean_scores[str(label)] = score
        if not clean_scores:
            raise DataValidationError(f"row {song.source_row}: emotion_scores cannot be empty")
        try:
            chunk_count = int(song.extra.get("chunk_count", 1))
        except (TypeError, ValueError) as exc:
            raise DataValidationError(f"row {song.source_row}: chunk_count must be an integer") from exc
        results.append(
            AnalysisResult(
                song=song,
                dominant_emotions=tuple(dominant),
                emotion_scores=clean_scores,
                backend=str(song.extra.get("analysis_backend", "unknown")),
                model=str(song.extra.get("analysis_model", "unknown")),
                chunk_count=chunk_count,
            )
        )
