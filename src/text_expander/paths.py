from __future__ import annotations

import os
import platform
from pathlib import Path


APP_NAME = "text-expander"


def app_dir() -> Path:
    override = os.environ.get("TEXT_EXPANDER_HOME")
    if override:
        path = Path(override).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        return path

    system = platform.system()
    if system == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    elif system == "Windows":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    path = base / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def data_path() -> Path:
    return app_dir() / "snippets.json"


def pid_path() -> Path:
    return app_dir() / "daemon.pid"


def lock_path() -> Path:
    return app_dir() / "daemon.lock"


def log_path() -> Path:
    return app_dir() / "daemon.log"


def backup_dir() -> Path:
    path = app_dir() / "backups"
    path.mkdir(parents=True, exist_ok=True)
    return path
