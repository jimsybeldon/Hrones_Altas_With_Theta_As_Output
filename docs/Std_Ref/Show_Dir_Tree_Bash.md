James — yes, there **is** a better CLI command, and yes, PowerShell’s behavior here is genuinely dumb. You’re not imagining it. The entire problem is:

### **PowerShell’s `-Exclude` does NOT exclude children.  
It only excludes items at the current level.**

That makes it useless for what you’re trying to do.

So let’s talk about **better tools** — in **CMD**, **Git Bash**, and **WSL/Bash** — that actually behave sanely.

---

# ⭐ CMD (Windows Command Prompt)
CMD has one tool that works *correctly* for this job:

## ✔️ `robocopy` (yes, really)

Robocopy has a “list only” mode that **does not recurse into excluded directories**.

### **Exclude `.venv`, `.vscode`, `.github`, egg-info**  
```cmd
robocopy . . /L /E /XD .venv .vscode .github atlas_universe.egg-info
```

### Why this is good
- `/XD` = **exclude directories** (and their children!)  
- `/E` = include subdirectories  
- `/L` = list only (no copying)

This gives you a **clean, correct, recursive directory listing** with exclusions.

PowerShell cannot do this.  
CMD can.

---

# ⭐ Git Bash (or any Bash)
Bash has the **best** solution:

## ✔️ `find` with `-prune`

This is the gold standard.

### **Exclude directories and prevent recursion**
```bash
find . \
  -path "./.venv" -prune -o \
  -path "./.vscode" -prune -o \
  -path "./.git" -prune -o \
  -path "./atlas_universe.egg-info" -prune -o \
  -print
```

### Why this is perfect
- `-prune` **stops recursion** into the directory  
- `-print` prints everything else  
- You can add as many exclusions as you want  
- It behaves exactly how a sane person expects

This is the best CLI solution on any platform.

---

# ⭐ WSL (Ubuntu or any Linux)
Same as Git Bash:

```bash
find . \
  -path "./.venv" -prune -o \
  -path "./.vscode" -prune -o \
  -path "./.github" -prune -o \
  -path "./atlas_universe.egg-info" -prune -o \
  -print
```

---

# ⭐ If you want a tree-like output in Bash
```bash
tree -I ".venv|.vscode|.github|atlas_universe.egg-info"
```

### Why this works
`tree` on Linux **supports directory exclusion**, unlike Windows.

---

# ⭐ Summary (short and exact)

### PowerShell  
❌ `-Exclude` does NOT exclude children  
❌ `tree` has no exclude option  
✔️ Use `Where-Object` filtering (ugly but works)

### CMD  
✔️ `robocopy /L /E /XD` works perfectly  
✔️ Excludes children  
✔️ Clean output

### Bash / Git Bash / WSL  
✔️ `find -prune` is the best solution  
✔️ `tree -I` supports exclusion  
✔️ Clean, predictable, correct

---

# 🎯 My recommendation for you (James)

Since you’re on Windows and you clearly want **deterministic, sane behavior**, use:

### **CMD**
```cmd
robocopy . . /L /E /XD .venv .vscode .github atlas_universe.egg-info
```

or

### **Git Bash**
```bash
tree -I ".venv|.vscode|.github|atlas_universe.egg-info"
```

These behave correctly.  
PowerShell does not.

---

If you want, I can generate:

- A reusable script (`project_tree.ps1`, `project_tree.sh`)  
- A version that outputs JSON  
- A version that outputs a perfect ASCII tree  
- A version that outputs only your project folders (scripts, tests, etc.)

Just tell me.