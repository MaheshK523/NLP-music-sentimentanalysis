from __future__ import annotations

import csv
import json
import os
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, TextIO

from .errors import DataValidationError
from .models import AnalysisResult, SongRecord


INPUT_FIELDS = ("title", "artist", "lyrics")
RESULT_FIELDS = (
    "dominant_emotions",
    "emotion_scores",
    "analysis_backend",
    "analysis_model",
    "chunk_count",
)
RESERVED_FIELDS = set(INPUT_FIELDS + RESULT_FIELDS)


def infer_format(path: str | Path, selected: str = "auto") -> str:
    if selected != "auto":
        return selected
    suffix = Path(path).suffix.casefold()
    if suffix == ".csv":
        return "csv"
    if suffix in {".jsonl", ".ndjson"}:
        return "jsonl"
    raise DataValidationError("could not infer format; use a .csv/.jsonl path or pass an explicit format")


def _validate_song(row: Mapping[str, Any], source_row: int) -> SongRecord:
    missing = [field for field in INPUT_FIELDS if field not in row]
    if missing:
        raise DataValidationError(f"row {source_row}: missing required field(s): {', '.join(missing)}")

