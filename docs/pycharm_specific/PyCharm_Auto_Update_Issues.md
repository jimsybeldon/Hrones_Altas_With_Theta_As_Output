PyCharm itself **does not automatically run `pip install --upgrade**` on your virtual environment packages in the background.

However, PyCharm *does* perform background indexing, package version scanning, and automatic IDE/plugin updates. Furthermore, clicking certain editor notification popups can inadvertently trigger background package synchronization.

To lock down PyCharm 2026 and prevent automatic scans, prompt installs, and IDE updates from touching your workflow:

---

### 1. Disable PyCharm Automatic IDE & Plugin Updates

Prevents JetBrains from automatically updating the IDE engine or internal Python plugins.

1. Press `Ctrl + Alt + S` (or `Cmd + ,` on macOS) to open **Settings**.
2. Navigate to **Appearance & Behavior** $\rightarrow$ **System Settings** $\rightarrow$ **Updates**.
3. Uncheck **Check IDE updates automatically**.
4. Uncheck **Update plugins automatically**.

---

### 2. Disable Automatic Package Sync / Requirements Prompting

Prevents PyCharm from prompting or auto-installing missing packages when it detects changes in `requirements.txt` or `pyproject.toml`.

1. In **Settings**, go to **Editor** $\rightarrow$ **Inspections**.
2. Expand **Python** in the center pane.
3. Locate **Package requirements** (or **Unsatisfied package requirements**).
4. Uncheck the box to disable the inspection completely.

---

### 3. Disable Automatic Background Indexing of Remote/Conda Environments

If you are using Conda, Docker, or WSL2 interpreters, PyCharm periodically syncs binaries in the background.

1. In **Settings**, navigate to **Tools** $\rightarrow$ **Python Integrated Tools**.
2. Look for **Packaging** / **Package Manager** settings and disable any background update checks or automatic version polling.

---

### 4. Lock Your Dependencies (The Ironclad Fix)

If a package updated and broke your code today, your virtual environment's dependencies were likely defined using loose version specifiers (or no versions at all) during an install or sync.

To guarantee no package ever updates implicitly again, explicitly pin exact versions in your environment definition:

```text
# requirements.txt
matplotlib==3.8.2
numpy==1.26.4
pandas==2.2.0

```

Or if you prefer `pyproject.toml`:

```toml
[project]
dependencies = [
    "matplotlib==3.8.2",
    "numpy==1.26.4",
]

```

When versions are hard-pinned with `==`, standard `pip install` commands will strictly refuse to pull newer breaking versions.