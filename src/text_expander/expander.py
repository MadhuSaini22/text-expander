from __future__ import annotations

import logging
import time
from contextlib import suppress

from .engine import Expansion

LOGGER = logging.getLogger(__name__)


class TextExpander:
    def __init__(self, paste_delay: float = 0.04) -> None:
        self.paste_delay = paste_delay
        self._load_dependencies()

    def _load_dependencies(self) -> None:
        try:
            import pyperclip
            from pynput.keyboard import Controller, Key
        except Exception as exc:  # pragma: no cover - depends on host desktop setup
            raise RuntimeError(
                "Expansion requires pynput and pyperclip. Install with: pip install -e ."
            ) from exc
        self.pyperclip = pyperclip
        self.keyboard = Controller()
        self.Key = Key

    def expand(self, expansion: Expansion) -> None:
        LOGGER.info("Expanding trigger %s", expansion.trigger)
        time.sleep(0.01)
        self._press_key(self.Key.backspace, presses=expansion.backspaces)
        self._paste_text(expansion.replacement)

    def _paste_text(self, text: str) -> None:
        previous = None
        with suppress(Exception):
            previous = self.pyperclip.paste()
        self.pyperclip.copy(text)
        time.sleep(self.paste_delay)
        if self._is_macos():
            self._hotkey(self.Key.cmd, "v")
        else:
            self._hotkey(self.Key.ctrl, "v")
        time.sleep(self.paste_delay)
        if previous is not None:
            with suppress(Exception):
                self.pyperclip.copy(previous)

    def _press_key(self, key, presses: int = 1) -> None:
        for _ in range(presses):
            self.keyboard.press(key)
            self.keyboard.release(key)

    def _hotkey(self, modifier, key: str) -> None:
        self.keyboard.press(modifier)
        try:
            self.keyboard.press(key)
            self.keyboard.release(key)
        finally:
            self.keyboard.release(modifier)

    def _is_macos(self) -> bool:
        import platform

        return platform.system() == "Darwin"
