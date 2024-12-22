from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .analysis import analyze_records
from .backends import create_backend
from .errors import MusicEmotionError
