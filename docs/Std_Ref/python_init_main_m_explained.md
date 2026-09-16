Here’s the clean, *mechanism‑first*, “inside baseball” explanation you want — the real rules behind `__init__.py`, `__main__.py`, and `python -m`, and how they interact to make subdirectories behave like importable or executable modules.

I’ll give you the **short deterministic takeaways first**, then the **deep reference‑grade breakdown** you can drop directly into your documentation.

---

## 🧩 **Concise Takeaway (the part to memorize)**

- **`__init__.py`**  
  Turns a directory into a **package**. Controls what happens on import. Defines package‑level namespace.

- **`__main__.py`**  
  Turns a directory into an **executable module**. Defines what happens when you run the package with `python -m package`.

- **`python -m`**  
  Runs a module or package **as a script**, using the import system instead of the filesystem.  
  If the target is a package, Python executes its `__main__.py`.

These three mechanisms are how Python decides whether a directory is:
- importable (`__init__.py`)
- executable (`__main__.py`)
- runnable via the module system (`python -m`)

---

# 📘 **Full Reference‑Grade Explanation (for your documentation)**

---

## 1. **What `__init__.py` Actually Does**

### **1.1. Marks a directory as a package**
Historically, Python only treated directories containing `__init__.py` as importable packages.

Modern Python *can* import namespace packages without it, but **real packages with code still use `__init__.py`** because it provides deterministic behavior.

### **1.2. Defines the package namespace**
When you write:

```python
import mypkg
```

Python executes:

```
mypkg/__init__.py
```

Everything defined or imported inside `__init__.py` becomes part of the package namespace:

```python
# mypkg/__init__.py
from .core import Engine
VERSION = "1.2.0"
```

Now users can do:

```python
from mypkg import Engine, VERSION
```

### **1.3. Controls what submodules are exposed**
You can explicitly define what `from mypkg import *` means:

```python
__all__ = ["Engine", "Solver"]
```

### **1.4. Can run initialization code**
This is rare but allowed:

```python
print("mypkg imported")
```

---

## 2. **What `__main__.py` Actually Does**

### **2.1. Makes a package executable**
If a directory contains:

```
mypkg/
    __main__.py
```

Then you can run:

```
python -m mypkg
```

Python will execute:

```
mypkg/__main__.py
```

### **2.2. Equivalent to script entry point**
`__main__.py` is the package’s “if run as a script” behavior.

It is the directory‑level equivalent of:

```python
if __name__ == "__main__":
    ...
```

inside a single `.py` file.

### **2.3. Typical use cases**
- CLI tools
- “run the package” behavior
- dispatching to subcommands
- packaging tools (pip, setuptools)

Example:

```python
# mypkg/__main__.py
from .cli import main
main()
```

---

## 3. **What `python -m` Actually Does**

### **3.1. Runs a module using the import system**
When you run:

```
python -m something
```

Python does **not** look for `something.py` in the current directory.

Instead it:
1. Uses the import system (`sys.path`)
2. Locates the module or package
3. Executes it as a script

This avoids the “current working directory” pitfalls of running raw scripts.

### **3.2. Behavior depends on what `something` is**

#### **Case A: `something` is a module**
Example:

```
python -m http.server
```

Python loads the module and executes its `if __name__ == "__main__"` block.

#### **Case B: `something` is a package**
Example:

```
python -m mypkg
```

Python executes:

```
mypkg/__main__.py
```

If `__main__.py` is missing, you get:

```
No module named mypkg.__main__
```

---

# 🧱 **How These Three Pieces Work Together for Subdirectories**

Let’s say you have:

```
mypkg/
    __init__.py
    __main__.py
    core/
        __init__.py
        engine.py
    cli/
        __init__.py
        main.py
```

### **Importing**
```python
import mypkg
```
→ runs `mypkg/__init__.py`

### **Running**
```
python -m mypkg
```
→ runs `mypkg/__main__.py`

### **Importing subpackages**
```python
from mypkg.core import engine
```
→ runs `mypkg/core/__init__.py`

### **Running subpackages**
```
python -m mypkg.core
```
→ runs `mypkg/core/__main__.py` (if present)

---

# 🧠 **Mental Model (the deterministic one)**

Think of a directory as having two optional “interfaces”:

| File | Meaning | When it runs |
|------|---------|--------------|
| `__init__.py` | *Import interface* | `import package` |
| `__main__.py` | *Execution interface* | `python -m package` |

And `python -m` is simply:

> “Run this module/package using the import system instead of the filesystem.”

---

# 🛠 **Rules of Thumb for Your Own Projects**

### **Use `__init__.py` when:**
- You want the directory to be importable.
- You want to expose a clean API.
- You want deterministic import behavior.

### **Use `__main__.py` when:**
- You want `python -m package` to do something.
- You want a CLI entry point.
- You want a runnable tool inside a package.

### **Use `python -m` when:**
- You want imports to work correctly.
- You want to avoid script path issues.
- You want to run a package, not a file.

---

# 📦 **Minimal Example for Your Reference Docs**

```
mypkg/
    __init__.py      # import behavior
    __main__.py      # run behavior
    tools/
        __init__.py
        build.py
```

`__init__.py`:

```python
from .tools.build import build_project
```

`__main__.py`:

```python
from .tools.build import build_project

if __name__ == "__main__":
    build_project()
```

Now:

- `import mypkg` gives you `build_project`
- `python -m mypkg` runs the build

---

If you want, I can also produce:

- a **canonical reference diagram**  
- a **“rules for structuring Python packages”** section  
- a **ready‑to‑paste documentation page**  
- a **minimal working example repo layout**  

Just tell me what format you want.