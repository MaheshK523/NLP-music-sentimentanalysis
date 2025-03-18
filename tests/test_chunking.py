import unittest

from music_emotion.chunking import tokenizer_chunks, tokenize_words, word_chunks


class FakeTokenizer:
    def num_special_tokens_to_add(self, pair=False):
        return 2

    def encode(self, text, add_special_tokens=False):
        return list(range(1, len(text.split()) + 1))

    def decode(self, token_ids, skip_special_tokens=True):
        return " ".join(f"token-{token_id}" for token_id in token_ids)


class ChunkingTest(unittest.TestCase):
    def test_word_tokenization_is_unicode_and_contraction_aware(self):
        self.assertEqual(tokenize_words("Café, DON'T stop 42 times."), ["café", "don't", "stop", "times"])

