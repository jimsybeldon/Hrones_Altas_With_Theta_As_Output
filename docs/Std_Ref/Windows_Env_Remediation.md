**Here is a clean, mechanism‑first Markdown “method sheet” you can drop directly into VS Code.**  
It’s structured as a remediation protocol for Windows + VS Code + Python environment conflicts — exactly the subsystems you listed.

I open with the full artifact, then expand with reasoning and next‑step pathways.

---

# **Windows + VS Code Python Environment Remediation Protocol**

## [chat in copilot](https://copilot.microsoft.com/shares/L9tLZ6bmawaLJRshc9xcg)

## **1. Fix Windows PATH**  
### **Objective**  
Ensure Windows resolves the correct Python interpreter and its Scripts directory.

### **Procedure**  
1. Open **System Properties** → *Advanced* → *Environment Variables*.  
2. Under **User variables**, edit `Path`.  
3. Add the two canonical entries (adjust version if needed):  
   - `C:\Users\<you>\AppData\Local\Programs\Python\Python311\`  
   - `C:\Users\<you>\AppData\Local\Programs\Python\Python311\Scripts\`  
4. Move both entries **above** any older Python paths.  
5. Remove stale or broken Python paths (e.g., pointing to deleted installs).  
6. Close all terminals and restart VS Code.

### **Verification**  
```powershell
where python
python --version
```

---

## **2. Disable App Execution Aliases**  
### **Objective**  
Prevent Windows from hijacking `python.exe` and redirecting it to the Microsoft Store stub.

### **Procedure**  
1. Open **Settings** → *Apps* → *Advanced app settings*.  
2. Select **App execution aliases**.  
3. Turn **off**:  
   - `python.exe`  
   - `python3.exe`  
4. Restart VS Code.

### **Verification**  
```powershell
Get-Command python
```

---

## **3. Clean Python Registry Entries**  
### **Objective**  
Remove stale interpreter registrations that confuse VS Code’s discovery engine.

### **Procedure**  
1. Open **regedit**.  
2. Navigate to:  
   - `HKEY_CURRENT_USER\Software\Python`  
   - `HKEY_LOCAL_MACHINE\Software\Python`  
3. Delete keys referencing **nonexistent** Python installs.  
4. Keep only the keys matching your active interpreter (e.g., Python 3.11).  
5. Restart Windows.

### **Verification**  
VS Code should rebuild its interpreter cache on launch.

---

## **4. Rebuild VS Code Python Interpreter Cache**  
### **Objective**  
Force VS Code to forget stale interpreter metadata.

### **Procedure**  
1. Close **all** VS Code windows.  
2. Delete the Python extension’s global storage folder:  
   ```
   %APPDATA%\Code\User\globalStorage\ms-python.python
   ```  
3. Reopen VS Code.  
4. Add a workspace override to force the correct interpreter:

```jsonc
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "C:/Users/<you>/AppData/Local/Programs/Python/Python311/python.exe"
}
```

### **Verification**  
VS Code → Command Palette → *Python: Select Interpreter*  
Should show only valid interpreters.

---

## **5. Confirm Terminal vs VS Code Interpreter Independence**  
### **Objective**  
Understand why VS Code may show Python 3.11 while your terminal shows something else.

### **Key Points**  
- VS Code interpreter selection **does not** modify the terminal environment.  
- Terminal Python is determined by **PATH**, aliases, or explicit invocation.  
- VS Code uses its own discovery engine + workspace override.

### **Verification**  
```powershell
python --version
```

---

## **6. Optional: Create a Deterministic .venv**  
### **Objective**  
Guarantee reproducible interpreter behavior inside VS Code.

### **Procedure**  
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

VS Code should auto‑detect `.venv` and switch to it.

---

---

# **Expanded Reasoning (for your mechanism‑first preference)**

### **Why PATH matters**  
Windows resolves executables by scanning PATH in order. If an older Python path appears first, VS Code’s terminal will pick it up even if VS Code itself uses a different interpreter internally.

### **Why App Execution Aliases break Python**  
The Microsoft Store alias intercepts `python.exe` and returns a stub. This causes:  
- `python` not found  
- VS Code showing “Select Interpreter” endlessly  
- Terminal returning the wrong version

### **Why registry cleanup matters**  
VS Code’s Python extension enumerates interpreters from:  
- PATH  
- Registry  
- Known install locations  
Stale registry entries create phantom interpreters.

### **Why interpreter cache deletion matters**  
The Python extension stores discovery metadata. If corrupted, VS Code will:  
- Fail to show correct interpreters  
- Show deleted versions  
- Ignore workspace overrides

---

# **Next Step — pick the subsystem you want to execute first**

You can continue with:  
- Fix Windows PATH  
- Disable App Execution Aliases  
- Clean Python registry entries  
- Rebuild VS Code interpreter cache

Tell me which one you want to run, and I’ll walk you through it with precision.