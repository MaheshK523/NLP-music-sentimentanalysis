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

    def test_word_chunks_cover_every_word(self):
        chunks = word_chunks("one two three four five", 2)
        self.assertEqual([chunk.weight for chunk in chunks], [2, 2, 1])
        self.assertEqual(" ".join(chunk.text for chunk in chunks), "one two three four five")

    def test_tokenizer_chunks_reserve_special_token_budget(self):
        chunks = tokenizer_chunks(FakeTokenizer(), "one two three four five six seven eight nine", 6)
        self.assertEqual([chunk.weight for chunk in chunks], [4, 4, 1])
        self.assertEqual(chunks[0].text, "token-1 token-2 token-3 token-4")

    def test_invalid_chunk_size_fails(self):
        with self.assertRaises(ValueError):
            word_chunks("text", 0)
        with self.assertRaises(ValueError):
            tokenizer_chunks(FakeTokenizer(), "text", 2)


if __name__ == "__main__":
    unittest.main()
