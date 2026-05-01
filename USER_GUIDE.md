# Text Expander User Guide

This guide helps you install, test, troubleshoot, and uninstall `text-expander` on macOS, Windows, and Linux.

`text-expander` is a terminal-only global text expander. You add shortcuts from the command line, start the background daemon, and then type triggers anywhere.

Example:

```txt
;l<space>
```

expands to:

```txt
https://www.linkedin.com/in/yourprofile/
```

## Quick Start

Install:

```bash
pip install text-expander
```

Check version:

```bash
text-expander --version
```

Install/start background service:

```bash
text-expander install
```

Add a shortcut:

```bash
text-expander add ';t' 'hello from text expander'
```

Test in Notepad, TextEdit, browser input, VS Code, or any text field:

```txt
;t<space>
```

## If `pip` Is Not Found

Use Python's pip module instead:

```bash
python3 -m pip install text-expander
```

On Windows:

```bat
python -m pip install text-expander
```

If Python itself is not found, install Python from:

```txt
https://www.python.org/downloads/
```

On Windows, during Python install, enable:

```txt
Add python.exe to PATH
```

## If `text-expander` Is Not Found After Install

This means the package installed successfully, but your shell cannot find Python's script directory.

You can still run the app with:

```bash
python3 -m text_expander --version
python3 -m text_expander install
```

On Windows:

```bat
python -m text_expander --version
python -m text_expander install
```

### macOS PATH Fix

If install showed a warning like:

```txt
text-expander is installed in '/Users/you/Library/Python/3.9/bin' which is not on PATH
```

Add that folder to PATH:

```bash
echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Then:

```bash
text-expander --version
```

If your Python version is different, find the script folder with:

```bash
python3 -m site --user-base
```

The command usually lives in:

```txt
<user-base>/bin
```

### Windows PATH Fix

The command usually lives in:

```bat
C:\Python311\Scripts\text-expander.exe
```

or:

```bat
C:\Python312\Scripts\text-expander.exe
```

Test directly:

```bat
C:\Python311\Scripts\text-expander.exe --version
```

If that works, add the Scripts folder to PATH.

Find the correct Scripts folder:

```bat
python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
```

Then open:

```txt
Windows Search → Edit the system environment variables → Environment Variables
```

Under User variables:

```txt
Path → Edit → New
```

Add the folder printed by the command, for example:

```txt
C:\Python311\Scripts
```

Also add the Python folder if missing:

```txt
C:\Python311
```

Close Command Prompt and open a new one.

Test:

```bat
text-expander --version
```

## Recommended Install With pipx

`pipx` is a good way to install command-line apps globally but isolated from system Python.

Install pipx:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

On Windows:

```bat
python -m pip install --user pipx
python -m pipx ensurepath
```

Close and reopen the terminal.

Install:

```bash
pipx install text-expander
text-expander install
```

If `pipx` is not found, use:

```bash
python3 -m pipx install text-expander
```

On Windows:

```bat
python -m pipx install text-expander
```

## Basic Commands

Add:

```bash
text-expander add ';l' 'https://www.linkedin.com/in/yourprofile/'
```

Interactive add:

```bash
text-expander add
```

List:

```bash
text-expander list
```

Search:

```bash
text-expander search linkedin
```

Edit:

```bash
text-expander edit ';l'
```

Delete:

```bash
text-expander delete ';l'
```

Start:

```bash
text-expander start
```

Stop:

```bash
text-expander stop
```

Status:

```bash
text-expander status
```

Doctor:

```bash
text-expander doctor
```

Install startup service:

```bash
text-expander install
```

Remove startup service:

```bash
text-expander uninstall
```

If `text-expander` is not available, replace it with:

```bash
python3 -m text_expander
```

On Windows:

```bat
python -m text_expander
```

Example:

```bat
python -m text_expander add ;t "hello"
python -m text_expander start
```

## How To Test If It Works

Run:

```bash
text-expander --version
text-expander doctor
text-expander add ';t' 'hello from text expander'
text-expander list
text-expander start
text-expander status
```

Open any text input and type:

```txt
;t<space>
```

Expected result:

```txt
hello from text expander
```

Try testing in a simple app first:

- Windows: Notepad
- macOS: TextEdit
- Linux: a plain text editor

Browsers sometimes capture Tab, so test with Space first.

## macOS Permissions

macOS blocks global keyboard monitoring until you grant permission.

Open:

```txt
System Settings → Privacy & Security → Accessibility
```

Enable the app that starts `text-expander`:

- Terminal
- iTerm
- VS Code
- Python

Also check:

```txt
System Settings → Privacy & Security → Input Monitoring
```

After changing permissions:

```bash
text-expander stop
text-expander start
text-expander doctor
```

You want:

```txt
macOS Accessibility: trusted
```

## Windows Notes

If install fails with an error like:

```txt
Failed to write executable
WinError 2
C:\Python312\Scripts\text-expander.exe
```

Use user install:

```bat
python -m pip install --upgrade pip
python -m pip install --user --force-reinstall text-expander
```

Then test:

```bat
python -m text_expander --version
```

If the short command does not work, fix PATH using the Windows PATH section above.

If you installed into system Python and Windows blocks writing files, either:

```bat
python -m pip install --user text-expander
```

or open Command Prompt as Administrator and run:

```bat
python -m pip install --force-reinstall text-expander
```

The user install is safer.

## Linux Notes

Linux support depends on the desktop session.

X11 usually works better for global keyboard listening.

Wayland often blocks global keyboard listeners by design. If shortcuts do not expand on Wayland, try:

```bash
echo $XDG_SESSION_TYPE
```

If it prints:

```txt
wayland
```

you may need to log into an X11 session or use desktop-specific permission tools.

## Auto-Start After Restart

Run:

```bash
text-expander install
```

This registers startup:

- macOS: LaunchAgent
- Windows: Startup folder
- Linux: systemd user service

Check:

```bash
text-expander status
```

Remove auto-start:

```bash
text-expander uninstall
```

## Import, Export, and Backup

Export:

```bash
text-expander export snippets.json
```

Import:

```bash
text-expander import snippets.json
```

Backup:

```bash
text-expander backup
```

## Storage Location

Snippets are stored locally.

macOS:

```txt
~/Library/Application Support/text-expander
```

Windows:

```txt
%APPDATA%\text-expander
```

Linux:

```txt
~/.config/text-expander
```

Use a custom directory:

```bash
TEXT_EXPANDER_HOME=/path/to/dir text-expander list
```

Windows PowerShell:

```powershell
$env:TEXT_EXPANDER_HOME="C:\path\to\dir"
text-expander list
```

## Uninstall

First stop and remove startup integration:

```bash
text-expander uninstall
```

Then remove the package:

```bash
python3 -m pip uninstall text-expander
```

On Windows:

```bat
python -m pip uninstall text-expander
```

If you installed with pipx:

```bash
pipx uninstall text-expander
```

## Troubleshooting Checklist

### Package installed but command not found

Use:

```bash
python3 -m text_expander --version
```

Then fix PATH.

### Shortcut does not expand

Check:

```bash
text-expander status
text-expander doctor
text-expander list
```

Make sure:

- daemon is running
- shortcut exists
- permissions are granted
- you typed Space, Enter, or Tab after the trigger

### Browser does not expand with Tab

Try Space first:

```txt
;t<space>
```

Browsers often use Tab to move focus.

### It expands twice

Stop duplicate daemons:

```bash
text-expander stop
text-expander start
```

If it still expands twice, uninstall startup and reinstall:

```bash
text-expander uninstall
text-expander install
```

### macOS shows a Python icon in Dock

Restart the daemon:

```bash
text-expander stop
text-expander start
```

If using an old install, upgrade:

```bash
python3 -m pip install --upgrade text-expander
text-expander uninstall
text-expander install
```

### Check installed version

```bash
text-expander --version
```

Fallback:

```bash
python3 -m text_expander --version
```

Windows fallback:

```bat
python -m text_expander --version
```

