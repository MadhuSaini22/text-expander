import unittest
from pathlib import Path

from text_expander.store import SnippetStore


class SnippetStoreTests(unittest.TestCase):
    def test_store_add_search_delete(self):
        with self._temp_dir() as tmp_path:
            tmp_path = Path(tmp_path)
            store = SnippetStore(tmp_path / "snippets.json")

            store.add(";l", "https://linkedin.com/in/yourprofile", ["social"])

            self.assertTrue(store.get(";l").replacement.startswith("https://linkedin"))
            self.assertEqual(store.search("social")[0].trigger, ";l")
            self.assertTrue(store.delete(";l"))
            self.assertEqual(store.list(), [])

    def test_import_export_roundtrip(self):
        with self._temp_dir() as tmp_path:
            tmp_path = Path(tmp_path)
            first = SnippetStore(tmp_path / "first.json")
            second = SnippetStore(tmp_path / "second.json")
            export_path = tmp_path / "export.json"

            first.add(";e", "hello@example.com")
            first.export(export_path)

            self.assertEqual(second.import_file(export_path), 1)
            self.assertEqual(second.get(";e").replacement, "hello@example.com")

    def _temp_dir(self):
        import tempfile

        return tempfile.TemporaryDirectory()


if __name__ == "__main__":
    unittest.main()
