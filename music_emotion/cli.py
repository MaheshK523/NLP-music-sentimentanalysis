from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .analysis import analyze_records
from .backends import create_backend
from .errors import MusicEmotionError
from .io import load_songs, write_results
from .report import generate_report, load_analysis_results


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="music-emotion",
        description="Analyze lyric emotion with an offline baseline or an explicitly enabled Transformers model.",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
