import unittest

from music_emotion.backends.lexicon import EMOTIONS, LexiconEmotionBackend


class LexiconBackendTest(unittest.TestCase):
    def setUp(self):
        self.backend = LexiconEmotionBackend()

    def test_joyful_text_is_scored_deterministically(self):
