from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


WORD_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?", re.UNICODE)


@dataclass(frozen=True, slots=True)
class TextChunk:
    text: str
    weight: int


def tokenize_words(text: str) -> list[str]:
    return [match.group(0).casefold().replace("’", "'") for match in WORD_RE.finditer(text)]


