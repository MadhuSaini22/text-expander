# Terminal Text Expander

A terminal-only, local-first text expander for macOS, Windows, and Linux.

Define snippets from the command line, run the daemon in the background, and type triggers anywhere on your system. When a trigger is followed by Space, Enter, or Tab, it is replaced with the saved text.

```bash
pipx install text-expander
text-expander install
text-expander add
```

Example:

```txt
;l<space>
```

expands to:

```txt
https://linkedin.com/in/yourprofile
```

## Install

Recommended:

```bash
pipx install text-expander
text-expander install
```

With pip:

```bash
python -m pip install text-expander
text-expander install
```

From this repository:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e .
```

On Linux, global keyboard capture may require additional system permissions depending on your desktop session. On macOS, grant Accessibility permissions to the terminal app that starts the daemon.

## Commands

```bash
text-expander add
text-expander list
text-expander edit ;l
text-expander delete ;l
text-expander search linkedin
text-expander install
text-expander uninstall
text-expander start
text-expander stop
text-expander status
text-expander doctor
text-expander run
text-expander startup install
text-expander startup uninstall
text-expander export snippets.json
text-expander import snippets.json
text-expander backup
```

## Storage

Snippets and runtime files are stored locally:

- macOS: `~/Library/Application Support/text-expander`
- Windows: `%APPDATA%\text-expander`
- Linux: `~/.config/text-expander`

Set `TEXT_EXPANDER_HOME=/path/to/dir` to use a custom data directory.

No cloud services are used.

## Notes

- Expansions are suppressed while the app is simulating replacement text to prevent recursive triggering.
- The daemon uses clipboard paste as the primary expansion path because it is faster and more reliable for long replacements. It restores the previous clipboard contents when possible.
- Startup registration uses LaunchAgents on macOS, the user Startup folder on Windows, and systemd user services on Linux.
- `pip install` only installs the CLI. Run `text-expander install` explicitly to register and start the background daemon.
