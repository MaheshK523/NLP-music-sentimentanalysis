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
        self.assertGreater(prediction.scores["sadness"], prediction.scores["joy"])

    def test_long_text_uses_multiple_chunks(self):
        prediction = self.backend.predict("love bright calm dark lonely surprise", chunk_size=2)
        self.assertEqual(prediction.chunk_count, 3)
        self.assertAlmostEqual(sum(prediction.scores.values()), 1.0)

    def test_unknown_text_has_a_neutral_fallback_distribution(self):
        prediction = self.backend.predict("quasar zephyr", chunk_size=50)
        self.assertEqual(max(prediction.scores, key=prediction.scores.get), "neutral")
