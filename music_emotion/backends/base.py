from __future__ import annotations

from typing import Protocol

from ..models import BackendPrediction


class EmotionBackend(Protocol):
    name: str
    model_name: str

    def predict(self, text: str, *, chunk_size: int) -> BackendPrediction:
        """Return normalized emotion scores for one complete lyric."""
