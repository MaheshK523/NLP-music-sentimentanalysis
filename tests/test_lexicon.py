import unittest

from music_emotion.backends.lexicon import EMOTIONS, LexiconEmotionBackend


class LexiconBackendTest(unittest.TestCase):
    def setUp(self):
        self.backend = LexiconEmotionBackend()

    def test_joyful_text_is_scored_deterministically(self):
        text = "We love the bright sunrise and dance with a happy smile"
        first = self.backend.predict(text, chunk_size=100)
        second = self.backend.predict(text, chunk_size=100)
        self.assertEqual(first, second)
        self.assertEqual(tuple(first.scores), EMOTIONS)
        self.assertAlmostEqual(sum(first.scores.values()), 1.0)
        self.assertEqual(max(first.scores, key=first.scores.get), "joy")

    def test_negation_redirects_a_positive_match(self):
        prediction = self.backend.predict("I am not happy", chunk_size=100)
