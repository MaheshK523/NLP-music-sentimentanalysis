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
