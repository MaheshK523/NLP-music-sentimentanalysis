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
