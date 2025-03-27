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
        self.assertEqual(records[0].extra["collection"], "demo")

    def test_jsonl_requires_string_fields(self):
        with tempfile.TemporaryDirectory() as raw_tmp:
            path = Path(raw_tmp) / "songs.jsonl"
            path.write_text(json.dumps({"title": "A", "artist": 7, "lyrics": "text"}) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(DataValidationError, "artist.*string"):
                load_songs(path)

    def test_csv_rejects_duplicate_headers(self):
        with tempfile.TemporaryDirectory() as raw_tmp:
            path = Path(raw_tmp) / "songs.csv"
            path.write_text("title,title,artist,lyrics\nA,A,B,text\n", encoding="utf-8")
            with self.assertRaisesRegex(DataValidationError, "duplicate"):
                load_songs(path)

    def test_csv_round_trip_uses_json_encoded_scores(self):
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            source = root / "songs.csv"
