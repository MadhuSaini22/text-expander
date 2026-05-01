from __future__ import annotations

import json
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

from .models import Snippet, now_iso
from .paths import backup_dir, data_path


class SnippetStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or data_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def list(self) -> list[Snippet]:
        return sorted(self._load().values(), key=lambda item: item.trigger.lower())

    def get(self, trigger: str) -> Snippet | None:
        return self._load().get(trigger)

    def add(self, trigger: str, replacement: str, tags: list[str] | None = None, case_sensitive: bool = True) -> Snippet:
        snippets = self._load()
        if trigger in snippets:
            raise ValueError(f"Snippet already exists: {trigger}")
        snippet = Snippet(trigger=trigger, replacement=replacement, tags=tags or [], case_sensitive=case_sensitive)
        snippets[trigger] = snippet
        self._save(snippets)
        return snippet

    def upsert(self, trigger: str, replacement: str, tags: list[str] | None = None, case_sensitive: bool = True) -> Snippet:
        snippets = self._load()
        existing = snippets.get(trigger)
        snippet = Snippet(
            trigger=trigger,
            replacement=replacement,
            tags=tags or (existing.tags if existing else []),
            case_sensitive=case_sensitive,
            created_at=existing.created_at if existing else now_iso(),
            updated_at=now_iso(),
        )
        snippets[trigger] = snippet
        self._save(snippets)
        return snippet

    def update(self, trigger: str, replacement: str | None = None, tags: list[str] | None = None, case_sensitive: bool | None = None) -> Snippet:
        snippets = self._load()
        snippet = snippets.get(trigger)
        if snippet is None:
            raise KeyError(trigger)
        if replacement is not None:
            snippet.replacement = replacement
        if tags is not None:
            snippet.tags = tags
        if case_sensitive is not None:
            snippet.case_sensitive = case_sensitive
        snippet.updated_at = now_iso()
        snippets[trigger] = snippet
        self._save(snippets)
        return snippet

    def delete(self, trigger: str) -> bool:
        snippets = self._load()
        existed = snippets.pop(trigger, None) is not None
        if existed:
            self._save(snippets)
        return existed

    def search(self, query: str) -> list[Snippet]:
        q = query.lower()
        return [
            snippet
            for snippet in self.list()
            if q in snippet.trigger.lower()
            or q in snippet.replacement.lower()
            or any(q in tag.lower() for tag in snippet.tags)
        ]

    def export(self, destination: Path) -> Path:
        destination = destination.expanduser()
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._save({})
        shutil.copy2(self.path, destination)
        return destination

    def import_file(self, source: Path, overwrite: bool = False) -> int:
        source = source.expanduser()
        payload = json.loads(source.read_text(encoding="utf-8"))
        incoming = self._parse_payload(payload)
        snippets = {} if overwrite else self._load()
        snippets.update(incoming)
        self._save(snippets)
        return len(incoming)

    def backup(self) -> Path:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        target = backup_dir() / f"snippets-{stamp}.json"
        return self.export(target)

    def _load(self) -> dict[str, Snippet]:
        if not self.path.exists():
            return {}
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid snippet database: {self.path}") from exc
        return self._parse_payload(payload)

    def _parse_payload(self, payload: object) -> dict[str, Snippet]:
        if isinstance(payload, dict) and "snippets" in payload:
            raw_snippets = payload["snippets"]
        else:
            raw_snippets = payload
        if not isinstance(raw_snippets, list):
            raise ValueError("Snippet file must contain a list or an object with a snippets list")
        snippets: dict[str, Snippet] = {}
        for raw in raw_snippets:
            if not isinstance(raw, dict):
                raise ValueError("Each snippet must be an object")
            snippet = Snippet.from_dict(raw)
            snippets[snippet.trigger] = snippet
        return snippets

    def _save(self, snippets: dict[str, Snippet]) -> None:
        payload = {
            "version": 1,
            "snippets": [snippet.to_dict() for snippet in sorted(snippets.values(), key=lambda item: item.trigger.lower())],
        }
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=str(self.path.parent), delete=False) as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            temp_name = handle.name
        Path(temp_name).replace(self.path)

