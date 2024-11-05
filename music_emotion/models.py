from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class SongRecord:
    title: str
    artist: str
    lyrics: str
    extra: Mapping[str, Any] = field(default_factory=dict)
    source_row: int | None = None


@dataclass(frozen=True, slots=True)
class BackendPrediction:
    scores: Mapping[str, float]
    chunk_count: int

