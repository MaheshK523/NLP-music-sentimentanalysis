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
