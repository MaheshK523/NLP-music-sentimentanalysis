from __future__ import annotations

import math
from collections.abc import Iterable, Iterator, Mapping

from .backends.base import EmotionBackend
from .errors import DataValidationError
from .models import AnalysisResult, SongRecord


