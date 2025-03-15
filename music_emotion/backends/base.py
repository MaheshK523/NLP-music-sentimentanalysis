from __future__ import annotations

from typing import Protocol

from ..models import BackendPrediction


class EmotionBackend(Protocol):
    name: str
    model_name: str
