from __future__ import annotations

import math
from collections import defaultdict
from typing import Any, Iterable, Mapping

from ..chunking import tokenizer_chunks
from ..errors import BackendUnavailableError
from ..models import BackendPrediction

