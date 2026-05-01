from __future__ import annotations

import os
import platform
import stat
import sys
from pathlib import Path

from .paths import app_dir


LABEL = "com.terminal-text-expander.daemon"


def install_startup() -> Path:
    system = platform.system()
    if system == "Darwin":
        return _install_macos()
    if system == "Windows":
        return _install_windows()
    return _install_linux()


def uninstall_startup() -> Path:
    system = platform.system()
    if system == "Darwin":
        path = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
    elif system == "Windows":
        path = _windows_startup_dir() / "text-expander.cmd"
    else:
        path = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "systemd" / "user" / "text-expander.service"
    path.unlink(missing_ok=True)
    return path


def _command() -> str:
    return f'"{sys.executable}" -m text_expander run'


def _install_macos() -> Path:
    path = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>{sys.executable}</string>
    <string>-m</string>
    <string>text_expander</string>
    <string>run</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>ProcessType</key>
  <string>Background</string>
  <key>StandardOutPath</key>
  <string>{app_dir() / "daemon.log"}</string>
  <key>StandardErrorPath</key>
  <string>{app_dir() / "daemon.log"}</string>
</dict>
</plist>
"""
    path.write_text(content, encoding="utf-8")
    return path


def _install_windows() -> Path:
    path = _windows_startup_dir() / "text-expander.cmd"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"@echo off\r\nstart \"\" /min {_command()}\r\n", encoding="utf-8")
    return path


def _install_linux() -> Path:
    path = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "systemd" / "user" / "text-expander.service"
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"""[Unit]
Description=Terminal Text Expander

[Service]
ExecStart={sys.executable} -m text_expander run
Restart=on-failure
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
"""
    path.write_text(content, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IRUSR | stat.S_IWUSR)
    return path


def _windows_startup_dir() -> Path:
    appdata = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    return appdata / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
