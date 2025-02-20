from __future__ import annotations

from .base import EmotionBackend
from .lexicon import LexiconEmotionBackend


def create_backend(
    name: str,
    *,
    model_name: str | None = None,
