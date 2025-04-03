import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from music_emotion.analysis import select_dominant_emotions
from music_emotion.cli import main
from music_emotion.errors import DataValidationError
