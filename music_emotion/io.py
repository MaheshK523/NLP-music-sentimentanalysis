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
