import unittest

from text_expander.engine import ExpansionEngine
from text_expander.models import Snippet


class ExpansionEngineTests(unittest.TestCase):
    def test_expands_trigger_on_space(self):
        engine = ExpansionEngine()
        for char in ";l":
            engine.ingest_char(char)

        expansion = engine.ingest_key("space", [Snippet(trigger=";l", replacement="https://example.com")])

        self.assertIsNotNone(expansion)
        self.assertEqual(expansion.replacement, "https://example.com ")
        self.assertEqual(expansion.backspaces, 3)

    def test_case_insensitive_snippet_matches_lowered_buffer(self):
        engine = ExpansionEngine()
        for char in ";LI":
            engine.ingest_char(char)

        expansion = engine.ingest_key("tab", [Snippet(trigger=";li", replacement="LinkedIn", case_sensitive=False)])

        self.assertIsNotNone(expansion)
        self.assertEqual(expansion.replacement, "LinkedIn\t")

    def test_non_matching_delimiter_stays_in_buffer(self):
        engine = ExpansionEngine()
        engine.ingest_char("x")

        expansion = engine.ingest_key("space", [Snippet(trigger=";l", replacement="link")])

        self.assertIsNone(expansion)
        self.assertEqual(engine.buffer, "x ")


if __name__ == "__main__":
    unittest.main()
