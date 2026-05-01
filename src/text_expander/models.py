from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Snippet:
    trigger: str
    replacement: str
    tags: list[str] = field(default_factory=list)
    case_sensitive: bool = True
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Snippet":
        return cls(
            trigger=str(value["trigger"]),
            replacement=str(value["replacement"]),
            tags=list(value.get("tags", [])),
            case_sensitive=bool(value.get("case_sensitive", True)),
            created_at=str(value.get("created_at") or now_iso()),
            updated_at=str(value.get("updated_at") or now_iso()),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "trigger": self.trigger,
            "replacement": self.replacement,
            "tags": self.tags,
            "case_sensitive": self.case_sensitive,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

