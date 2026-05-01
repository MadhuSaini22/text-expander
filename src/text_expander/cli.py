from __future__ import annotations

import argparse
import importlib.util
import os
import platform
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

from . import __version__
from .daemon import is_running, read_pid, run_forever, start_background, stop_background
from .paths import data_path, log_path
from .startup import install_startup, uninstall_startup
from .store import SnippetStore


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("Interrupted")
        return 130
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="text-expander", description="Terminal-only global text expander")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="Add a shortcut")
    add.add_argument("trigger", nargs="?")
    add.add_argument("replacement", nargs="?")
    add.add_argument("--tag", action="append", default=[])
    add.add_argument("--case-insensitive", action="store_true")
    add.set_defaults(func=cmd_add)

    list_cmd = subparsers.add_parser("list", help="View all shortcuts")
    list_cmd.set_defaults(func=cmd_list)

    edit = subparsers.add_parser("edit", help="Edit an existing shortcut")
    edit.add_argument("trigger")
    edit.set_defaults(func=cmd_edit)

    delete = subparsers.add_parser("delete", help="Delete a shortcut")
    delete.add_argument("trigger")
    delete.set_defaults(func=cmd_delete)

    search = subparsers.add_parser("search", help="Search shortcuts")
    search.add_argument("query")
    search.set_defaults(func=cmd_search)

    install = subparsers.add_parser("install", help="Install startup entry and start the daemon")
    install.set_defaults(func=cmd_install)

    uninstall = subparsers.add_parser("uninstall", help="Stop the daemon and remove startup entry")
    uninstall.set_defaults(func=cmd_uninstall)

    start = subparsers.add_parser("start", help="Start the background daemon")
    start.set_defaults(func=lambda _args: start_background())

    stop = subparsers.add_parser("stop", help="Stop the background daemon")
    stop.set_defaults(func=lambda _args: stop_background())

    status = subparsers.add_parser("status", help="Show daemon status")
    status.set_defaults(func=cmd_status)

    doctor = subparsers.add_parser("doctor", help="Check dependencies and host permissions")
    doctor.set_defaults(func=cmd_doctor)

    run = subparsers.add_parser("run", help="Run the daemon in the foreground")
    run.set_defaults(func=lambda _args: run_forever())

    startup = subparsers.add_parser("startup", help="Manage login startup")
    startup_sub = startup.add_subparsers(dest="startup_command", required=True)
    startup_install = startup_sub.add_parser("install", help="Install login startup entry")
    startup_install.set_defaults(func=cmd_startup_install)
    startup_uninstall = startup_sub.add_parser("uninstall", help="Remove login startup entry")
    startup_uninstall.set_defaults(func=cmd_startup_uninstall)

    export = subparsers.add_parser("export", help="Export shortcuts to JSON")
    export.add_argument("path")
    export.set_defaults(func=cmd_export)

    import_cmd = subparsers.add_parser("import", help="Import shortcuts from JSON")
    import_cmd.add_argument("path")
    import_cmd.add_argument("--overwrite", action="store_true")
    import_cmd.set_defaults(func=cmd_import)

    backup = subparsers.add_parser("backup", help="Create a timestamped local backup")
    backup.set_defaults(func=cmd_backup)

    return parser


def cmd_add(args: argparse.Namespace) -> int:
    trigger = args.trigger or input("Trigger: ").strip()
    replacement = args.replacement or input("Replacement: ")
    validate_trigger(trigger)
    SnippetStore().add(trigger, replacement, args.tag, not args.case_insensitive)
    print(f"Added {trigger}")
    return 0


def cmd_list(_args: argparse.Namespace) -> int:
    print_snippets(SnippetStore().list())
    return 0


def cmd_edit(args: argparse.Namespace) -> int:
    store = SnippetStore()
    snippet = store.get(args.trigger)
    if snippet is None:
        print(f"No snippet found for {args.trigger}", file=sys.stderr)
        return 1
    edited = open_editor(snippet.replacement)
    if edited is None:
        print("Edit cancelled")
        return 1
    store.update(args.trigger, replacement=edited)
    print(f"Updated {args.trigger}")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    if SnippetStore().delete(args.trigger):
        print(f"Deleted {args.trigger}")
        return 0
    print(f"No snippet found for {args.trigger}", file=sys.stderr)
    return 1


def cmd_search(args: argparse.Namespace) -> int:
    print_snippets(SnippetStore().search(args.query))
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    if is_running():
        print(f"text-expander is running (pid {read_pid()})")
    else:
        print("text-expander is stopped")
    print(f"Data: {data_path()}")
    print(f"Log: {log_path()}")
    return 0


def cmd_install(_args: argparse.Namespace) -> int:
    path = install_startup()
    print(f"Installed startup entry: {path}")
    return start_background()


def cmd_uninstall(_args: argparse.Namespace) -> int:
    stop_code = stop_background()
    path = uninstall_startup()
    print(f"Removed startup entry: {path}")
    return stop_code


def cmd_doctor(_args: argparse.Namespace) -> int:
    ok = True
    for module in ("pynput", "pyautogui", "pyperclip"):
        found = importlib.util.find_spec(module) is not None
        print(f"{module}: {'ok' if found else 'missing'}")
        ok = ok and found

    snippets = SnippetStore().list()
    print(f"snippets: {len(snippets)}")
    print(f"daemon: {'running' if is_running() else 'stopped'}")
    print(f"data: {data_path()}")
    print(f"log: {log_path()}")

    if platform.system() == "Darwin":
        trusted = macos_accessibility_trusted()
        print(f"macOS Accessibility: {'trusted' if trusted else 'not trusted'}")
        if not trusted:
            ok = False
            print("Grant Accessibility to the app that starts text-expander, then restart the daemon.")
    return 0 if ok else 1


def macos_accessibility_trusted() -> bool:
    try:
        from ApplicationServices import AXIsProcessTrusted
    except Exception:
        return False
    return bool(AXIsProcessTrusted())


def cmd_startup_install(_args: argparse.Namespace) -> int:
    path = install_startup()
    print(f"Installed startup entry: {path}")
    if sys.platform.startswith("linux"):
        print("Enable it with: systemctl --user enable --now text-expander.service")
    elif sys.platform == "darwin":
        print("Load it now with: launchctl load ~/Library/LaunchAgents/com.terminal-text-expander.daemon.plist")
    return 0


def cmd_startup_uninstall(_args: argparse.Namespace) -> int:
    path = uninstall_startup()
    print(f"Removed startup entry: {path}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    path = SnippetStore().export(Path(args.path))
    print(f"Exported snippets to {path}")
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    count = SnippetStore().import_file(Path(args.path), overwrite=args.overwrite)
    print(f"Imported {count} snippet(s)")
    return 0


def cmd_backup(_args: argparse.Namespace) -> int:
    path = SnippetStore().backup()
    print(f"Created backup: {path}")
    return 0


def validate_trigger(trigger: str) -> None:
    if not trigger:
        raise ValueError("Trigger cannot be empty")
    if any(char.isspace() for char in trigger):
        raise ValueError("Trigger cannot contain whitespace")


def print_snippets(snippets) -> None:
    if not snippets:
        print("No shortcuts found")
        return
    trigger_width = min(max(len(item.trigger) for item in snippets), 32)
    for snippet in snippets:
        tags = f" [{', '.join(snippet.tags)}]" if snippet.tags else ""
        print(f"{snippet.trigger:<{trigger_width}}  {snippet.replacement}{tags}")


def open_editor(initial: str) -> str | None:
    editor = os.environ.get("EDITOR") or ("notepad" if sys.platform == "win32" else "vi")
    with tempfile.NamedTemporaryFile("w+", suffix=".txt", encoding="utf-8", delete=False) as handle:
        handle.write(initial)
        handle.flush()
        temp_name = handle.name
    try:
        result = subprocess.run([*shlex.split(editor), temp_name], check=False)
        if result.returncode != 0:
            return None
        return Path(temp_name).read_text(encoding="utf-8")
    finally:
        Path(temp_name).unlink(missing_ok=True)
