# Python Virtual Environment Commands

This file provides the specific commands to create and activate a Python virtual environment named `.venv` across different command-line shells.

## 1. Create the Virtual Environment

This command is the same for Bash, CMD, and PowerShell. Run it from your project's root directory.

### Standard Python

> **Note:** On Windows, it is often more reliable to use the `py` launcher. On Linux/macOS, `python3` is standard.

```bash
# On Windows
python3 -m venv .venv

# On Linux/macOS
python3 -m venv .venv
```

### Using `uv`

If you have `uv` installed, you can use the following command, which is generally faster.

```bash
uv venv .venv
```

## 2. Activate the Virtual Environment

The activation command is different for each shell.

### PowerShell Prompt (PS)

```PS
.venv\scripts\activate
```

### Bash  (Git Bash on Windows)

```bash
source .venv/Scripts/activate
```

### Bash  (Bash on Linux/macOS)


```bash
source .venv/bin/activate
```



```bash
source marimo-env/Scripts/activate
```

### Windows Command Prompt (CMD)

```bat
.\.venv\Scripts\activate.bat
```

### Windows PowerShell (PWSH)

```powershell
# The '.' is the 'source' command in PowerShell, which runs the script in the current scope.
. .\.venv\Scripts\Activate.ps1
```

> **Note for PowerShell:** If you get a security error about the script not being digitally signed, you may need to adjust the execution policy for your current terminal session by running this command first, then trying the activation command again:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> ```

After successful activation, your terminal prompt should be prefixed with `(.venv)`.
