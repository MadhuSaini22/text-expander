# Terminal Text Expander

A terminal-only, local-first text expander for macOS, Windows, and Linux.

Define shortcuts from your terminal, run the background daemon, and type triggers anywhere on your system: browsers, forms, editors, chat apps, terminals, job boards, and desktop apps.

When a trigger is followed by **Space**, **Enter**, or **Tab**, it expands into the saved text.

> In examples, `<space>` means: press the Space bar on your keyboard.  
> Example: `;l<space>` means type `;l`, then press Space.

## Why Use It?

Text Expander is useful when you repeatedly type the same links, messages, form answers, templates, or commands.

### For Developers

If you work on a few repositories every day, you probably open the same pages again and again:

```bash
text-expander add ';repo' 'https://github.com/yourname/your-repo'
text-expander add ';issues' 'https://github.com/yourname/your-repo/issues'
text-expander add ';prs' 'https://github.com/yourname/your-repo/pulls'
text-expander add ';local' 'http://localhost:3000'
```

Then type:

```txt
;issues<space>
```

and it expands to your issues page.

You can also save repeated snippets:

```bash
text-expander add ';bug' 'Steps to reproduce:\nExpected:\nActual:'
text-expander add ';api' 'http://localhost:3000/api'
text-expander add ';review' 'Thanks for the PR. I left a few comments.'
```

### For Job Seekers

If you apply on job boards regularly, save your common application details:

```bash
text-expander add ';l' 'https://www.linkedin.com/in/yourprofile/'
text-expander add ';g' 'https://github.com/yourname'
text-expander add ';w' 'https://yourportfolio.com'
text-expander add ';em' 'you@example.com'
text-expander add ';intro' 'Hi, I am a software engineer interested in this role.'
```

Use them on LinkedIn, Wellfound, Greenhouse, Lever, Workday, Google Forms, and other forms.

### For Email and Support Templates

If you type the same emails or replies often:

```bash
text-expander add ';hello' 'Hi, thanks for reaching out. I am happy to help.'
text-expander add ';follow' 'Thanks for your time today. Here are the next steps:'
text-expander add ';sig' 'Best,\nYour Name'
```

Then type:

```txt
;hello<space>
```

### For Everyday Forms

Save things like:

```bash
text-expander add ';addr' '123 Main Street, City, Country'
text-expander add ';phone' '+1 555 123 4567'
text-expander add ';cal' 'https://cal.com/yourname'
text-expander add ';bio' 'Short bio you use often.'
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

`pip install` only installs the CLI. Run `text-expander install` to register and start the background daemon.

## Quick Test

Add a shortcut:

```bash
text-expander add ';t' 'hello from text expander'
```

Start the daemon:

```bash
text-expander start
```

Open any text input and type:

```txt
;t<space>
```

Expected result:

```txt
hello from text expander
```

If the browser captures Tab, test with Space first.

## Commands

### Add a Shortcut

Interactive:

```bash
text-expander add
```

Direct:

```bash
text-expander add ';l' 'https://linkedin.com/in/yourprofile'
```

Adds a trigger and replacement.

### List Shortcuts

```bash
text-expander list
```

Shows all saved shortcuts.

### Edit a Shortcut

```bash
text-expander edit ';l'
```

Opens your terminal editor so you can update the replacement text.

### Delete a Shortcut

```bash
text-expander delete ';l'
```

Removes a saved shortcut.

### Search Shortcuts

```bash
text-expander search linkedin
```

Searches triggers, replacements, and tags.

### Start the Daemon

```bash
text-expander start
```

Starts the global keyboard listener in the background.

### Stop the Daemon

```bash
text-expander stop
```

Stops the background listener.

### Check Status

```bash
text-expander status
```

Shows whether the daemon is running and where data/log files are stored.

### Diagnose Problems

```bash
text-expander doctor
```

Checks dependencies, snippets, daemon status, and macOS Accessibility permission.

### Install Auto-Start

```bash
text-expander install
```

Registers Text Expander to run after login/restart and starts it immediately.

Uses:

- macOS: LaunchAgent
- Windows: Startup folder
- Linux: systemd user service

### Uninstall Auto-Start

```bash
text-expander uninstall
```

Stops the daemon and removes login/startup registration.

### Import, Export, and Backup

```bash
text-expander export snippets.json
text-expander import snippets.json
text-expander backup
```

Use these to move shortcuts between machines or create a backup.

## All Commands

```bash
text-expander add
text-expander list
text-expander edit ';l'
text-expander delete ';l'
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

## OS Permissions

### macOS

macOS requires Accessibility permission for global keyboard monitoring.

Open:

```txt
System Settings → Privacy & Security → Accessibility
```

Enable the terminal app that starts Text Expander, such as Terminal, iTerm, or VS Code.

You may also need:

```txt
System Settings → Privacy & Security → Input Monitoring
```

Then restart:

```bash
text-expander stop
text-expander start
```

### Windows

If `text-expander` is not found after install, your Python Scripts folder may not be on PATH.

You can still run:

```bat
python -m text_expander --version
python -m text_expander install
```

For detailed PATH fixes, see [USER_GUIDE.md](USER_GUIDE.md).

### Linux

Global keyboard capture depends on your desktop session.

X11 is more likely to work. Wayland may block global keyboard listeners by design.

## Storage

Snippets and runtime files are stored locally:

- macOS: `~/Library/Application Support/text-expander`
- Windows: `%APPDATA%\text-expander`
- Linux: `~/.config/text-expander`

Set a custom data directory:

```bash
TEXT_EXPANDER_HOME=/path/to/dir text-expander list
```

No cloud services are used.

## Privacy

- All snippets are stored locally.
- No account is required.
- No cloud sync is used.
- No telemetry is sent.

## Troubleshooting

Read the full guide:

[USER_GUIDE.md](USER_GUIDE.md)

It covers:

- `pip` not found
- `pipx` not found
- `text-expander` command not found
- Windows PATH issues
- macOS permissions
- Linux Wayland notes
- install/uninstall
- testing shortcuts
- duplicate expansion issues

## Development

Install from this repository:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e .
```

Run tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Build package:

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

