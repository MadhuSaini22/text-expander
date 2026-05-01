from __future__ import annotations

from dataclasses import dataclass

from .models import Snippet


DELIMITER_KEYS = {"space", "enter", "tab"}
DELIMITER_TEXT = {"space": " ", "enter": "\n", "tab": "\t"}
RESET_KEYS = {"esc", "left", "right", "up", "down", "home", "end", "page_up", "page_down"}


@dataclass(frozen=True)
class Expansion:
    trigger: str
    replacement: str
    delimiter: str
    backspaces: int


class ExpansionEngine:
    def __init__(self, max_buffer: int = 128) -> None:
        self.max_buffer = max_buffer
        self.buffer = ""
        self.suppressed = False

    def reset(self) -> None:
        self.buffer = ""

    def ingest_char(self, char: str) -> None:
        if self.suppressed:
            return
        self.buffer = (self.buffer + char)[-self.max_buffer :]

    def ingest_key(self, key_name: str, snippets: list[Snippet]) -> Expansion | None:
        if self.suppressed:
            return None
        if key_name in DELIMITER_KEYS:
            return self._match(key_name, snippets)
        if key_name in RESET_KEYS:
            self.reset()
        return None

    def _match(self, delimiter: str, snippets: list[Snippet]) -> Expansion | None:
        for snippet in sorted(snippets, key=lambda item: len(item.trigger), reverse=True):
            haystack = self.buffer if snippet.case_sensitive else self.buffer.lower()
            needle = snippet.trigger if snippet.case_sensitive else snippet.trigger.lower()
            if haystack.endswith(needle):
                expansion = Expansion(
                    trigger=snippet.trigger,
                    replacement=snippet.replacement + DELIMITER_TEXT[delimiter],
                    delimiter=delimiter,
                    backspaces=len(snippet.trigger) + 1,
                )
                self.reset()
                return expansion
        self.ingest_char(DELIMITER_TEXT[delimiter])
        return None

