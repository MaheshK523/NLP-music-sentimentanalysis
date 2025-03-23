import csv
import json
import tempfile
import unittest
from pathlib import Path

from music_emotion.analysis import analyze_records
from music_emotion.backends.lexicon import LexiconEmotionBackend
from music_emotion.errors import DataValidationError
from music_emotion.io import load_songs, write_results
