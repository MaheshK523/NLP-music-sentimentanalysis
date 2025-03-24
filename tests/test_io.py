import csv
import json
import tempfile
import unittest
from pathlib import Path

from music_emotion.analysis import analyze_records
from music_emotion.backends.lexicon import LexiconEmotionBackend
from music_emotion.errors import DataValidationError
from music_emotion.io import load_songs, write_results
from music_emotion.report import load_analysis_results


class InputOutputTest(unittest.TestCase):
    def test_csv_input_preserves_extra_columns(self):
        with tempfile.TemporaryDirectory() as raw_tmp:
            path = Path(raw_tmp) / "songs.csv"
            path.write_text("title,artist,lyrics,collection\nA,B,happy song,demo\n", encoding="utf-8")
            records = load_songs(path)
        self.assertEqual(len(records), 1)
