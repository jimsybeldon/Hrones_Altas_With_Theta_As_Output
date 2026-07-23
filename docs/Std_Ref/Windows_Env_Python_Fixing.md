James, you’re absolutely right to push back here — and thank you for calling it out clearly.  
Let me reset the frame so we solve the *real* problem: **VS Code should create and use your `.venv` automatically**, and your terminals should follow that environment without you having to hack PATH or fight Windows.

Right now, your environment is behaving like this:

- VS Code *thinks* the `.venv` is active (the prompt shows `(.venv)`).
- But PowerShell’s PATH **does not include** `.venv\Scripts`.
- So VS Code’s integrated terminal is *lying* — it shows the venv name but is still using the system Python.
- That’s why `pytest` works (because VS Code runs the venv’s pytest.exe directly) but `python` does not.

This is a known VS Code + Windows + PowerShell interaction problem.

Let’s fix it **the VS Code way**, not the “hack PATH manually” way.

---

# ⭐ The correct fix: Let VS Code control the interpreter and terminals

VS Code has a very specific mechanism for Python environments:

### ✔ It chooses the interpreter  
### ✔ It rewrites the terminal PATH  
### ✔ It injects the correct activation script  
### ✔ It ensures `python` resolves to the venv Python  
### ✔ It ensures `pytest` resolves to the venv Python  

Right now, VS Code is **not** doing that correctly.

Let’s fix VS Code so it behaves the way you expect.

---

# 🔧 Step 1 — Tell VS Code which Python interpreter to use

In VS Code:

1. Press **Ctrl+Shift+P**
2. Type: **Python: Select Interpreter**
3. Choose:

```
.\.venv\Scripts\python.exe
```

This is the *only* interpreter VS Code should use.

VS Code will now:

- rewrite terminal PATH
- activate the venv correctly
- use the correct Python for debugging
- use the correct Python for scripts
- use the correct Python for pytest

This step alone fixes most issues.

---

# 🔧 Step 2 — Make VS Code terminals auto‑activate the venv

VS Code has a setting that controls this:

1. Open **Settings** (Ctrl+,)
2. Search for:

```
python terminal activate
```

3. Ensure this is **enabled**:

```
Python › Terminal: Activate Environment
```

This forces VS Code to run:

```
.\.venv\Scripts\activate
```

every time you open a terminal.

---

# 🔧 Step 3 — Ensure VS Code uses PowerShell correctly

VS Code sometimes uses a shell profile that blocks activation.

Check this setting:

1. Settings → search:

```
terminal.integrated.shellArgs.windows
```

Make sure it is **empty**.

If it contains something like:

```
-ExecutionPolicy Bypass
```

or

```
-NoProfile
```

it can break venv activation.

Clear it.

---

# 🔧 Step 4 — Restart VS Code completely

Close all VS Code windows.  
Reopen the project.

Open a new terminal:

```
(.venv) PS C:\Users\jimsy\github\Matlab\LInkage_Synth\Hrones_Nelson\Atlas_Universe>
```

Now run:

```
where python
```

You should finally see:

```
C:\Users\jimsy\github\Matlab\LInkage_Synth\Hrones_Nelson\Atlas_Universe\.venv\Scripts\python.exe
```

If you see that, everything is fixed.

---

# ⭐ Why this is the correct solution

Because:

- VS Code is designed to manage virtual environments automatically.
- You should **not** have to manually edit PATH.
- You should **not** have to fight Windows Store shims.
- You should **not** have to create PowerShell functions.
- You should **not** have to rebuild the venv repeatedly.

You want:

### ✔ VS Code creates the venv  
### ✔ VS Code activates the venv  
### ✔ VS Code terminals use the venv  
### ✔ VS Code debugging uses the venv  
### ✔ VS Code pytest uses the venv  

And that’s exactly what the steps above restore.

---

# ⭐ If you want, I can walk you through verifying VS Code’s interpreter and terminal activation live.

Just tell me:

```
Ctrl+Shift+P → Python: Select Interpreter → what options do you see?
```

That will tell me exactly where VS Code is pointing.