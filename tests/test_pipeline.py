import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from music_emotion.analysis import select_dominant_emotions
from music_emotion.cli import main
from music_emotion.errors import DataValidationError


REPO_ROOT = Path(__file__).resolve().parents[1]


class PipelineTest(unittest.TestCase):
    def test_threshold_falls_back_deterministically(self):
        scores = {"sadness": 0.4, "joy": 0.4, "neutral": 0.2}
        self.assertEqual(select_dominant_emotions(scores, 0.9), ("joy",))
        with self.assertRaises(DataValidationError):
