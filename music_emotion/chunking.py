from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


WORD_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?", re.UNICODE)


