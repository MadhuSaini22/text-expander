from __future__ import annotations

import errno
import logging
import os
import platform
import signal
import subprocess
import sys
import time
from contextlib import suppress
from pathlib import Path

from .engine import ExpansionEngine
from .expander import TextExpander
from .paths import lock_path, log_path, pid_path
from .store import SnippetStore

LOGGER = logging.getLogger(__name__)
LOCK_HANDLE = None


def configure_logging() -> None:
    logging.basicConfig(
        filename=str(log_path()),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def run_forever() -> int:
    configure_logging()
    if not acquire_single_instance_lock():
        LOGGER.info("Another text-expander daemon is already running; exiting")
        return 0
    LOGGER.info("Starting text-expander daemon")
    pid_path().write_text(str(os.getpid()), encoding="utf-8")
    try:
        return _run_listener()
    finally:
        with suppress(FileNotFoundError):
            pid_path().unlink()
        LOGGER.info("Stopped text-expander daemon")


def acquire_single_instance_lock() -> bool:
    global LOCK_HANDLE
    path = lock_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+")
    try:
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        handle.close()
        return False
    handle.seek(0)
    handle.truncate()
    handle.write(str(os.getpid()))
    handle.flush()
    LOCK_HANDLE = handle
    return True


def _run_listener() -> int:
    hide_macos_app_icon()
    try:
        from pynput import keyboard
    except Exception as exc:  # pragma: no cover - depends on host desktop setup
        LOGGER.exception("pynput is required for the global listener")
        raise RuntimeError("Global listener requires pynput. Install with: pip install -e .") from exc

    store = SnippetStore()
    engine = ExpansionEngine()
    expander = TextExpander()

    def current_snippets():
        try:
            return store.list()
        except Exception:
            LOGGER.exception("Could not load snippets")
            return []

    def on_press(key):
        if engine.suppressed:
            return
        try:
            if hasattr(key, "char") and key.char:
                engine.ingest_char(key.char)
                return
            key_name = getattr(key, "name", None)
            if key_name is None:
                key_name = str(key).replace("Key.", "")
            expansion = engine.ingest_key(key_name, current_snippets())
            if expansion is None:
                return
            engine.suppressed = True
            try:
                expander.expand(expansion)
            finally:
                engine.suppressed = False
        except Exception:
            LOGGER.exception("Listener error")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    return 0


def hide_macos_app_icon() -> None:
    if platform.system() != "Darwin":
        return
    try:
        from Foundation import NSBundle

        info = NSBundle.mainBundle().infoDictionary()
        info["LSBackgroundOnly"] = "1"
        info["LSUIElement"] = "1"
        LOGGER.info("macOS process marked as background-only UIElement")
    except Exception:
        LOGGER.exception("Could not hide macOS app icon")


def is_running(pid_file: Path | None = None) -> bool:
    path = pid_file or pid_path()
    pid = read_pid(path)
    if pid is None:
        return False
    return process_exists(pid)


def read_pid(path: Path | None = None) -> int | None:
    path = path or pid_path()
    try:
        return int(path.read_text(encoding="utf-8").strip())
    except (FileNotFoundError, ValueError):
        return None


def process_exists(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError as exc:
        if exc.errno == errno.EPERM:
            return True
        return False
    return True


def start_background() -> int:
    if is_running():
        pid = read_pid()
        print(f"text-expander is already running (pid {pid})")
        return 0

    command = [sys.executable, "-m", "text_expander", "run"]
    log_file = log_path().open("a", encoding="utf-8")
    kwargs: dict[str, object] = {
        "stdin": subprocess.DEVNULL,
        "stdout": log_file,
        "stderr": log_file,
        "cwd": str(Path.home()),
    }
    if sys.platform == "win32":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    else:
        kwargs["start_new_session"] = True
    process = subprocess.Popen(command, **kwargs)
    time.sleep(0.6)
    if process.poll() is not None:
        if is_running():
            print(f"text-expander is already running (pid {read_pid()})")
            return 0
        print(f"Failed to start text-expander. See log: {log_path()}")
        return process.returncode or 1
    print(f"text-expander started (pid {process.pid})")
    return 0


def stop_background() -> int:
    pid = read_pid()
    if pid is None:
        print("text-expander is not running")
        return 0
    try:
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.kill(pid, signal.SIGTERM)
    except OSError:
        pass
    for _ in range(20):
        if not process_exists(pid):
            with suppress(FileNotFoundError):
                pid_path().unlink()
            print("text-expander stopped")
            return 0
        time.sleep(0.1)
    print(f"Could not stop text-expander (pid {pid})")
    return 1
