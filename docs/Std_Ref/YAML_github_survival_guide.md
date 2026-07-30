James — here’s the **YAML Survival Guide**, written for a science‑minded user who wants clarity, stability, and zero nonsense. This is the version you can safely drop into your reference markdowns.

I’m keeping it crisp, deterministic, and focused on the failure modes that *actually* matter in GitHub Actions.

---

# 🧭 YAML Survival Guide (GitHub Actions Edition)

## 1. YAML Is Whitespace‑Sensitive  
YAML uses indentation to define structure.  
That means:

- **spaces matter**
- **tabs break things**
- **non‑breaking spaces (`\u00A0`) silently break workflows**
- **mixed indentation breaks workflows**

### How to protect yourself  
Turn on whitespace rendering in VS Code:

- `Ctrl+Shift+P` → “Toggle Render Whitespace”

You’ll see:

- real spaces → dots  
- tabs → arrows  
- non‑breaking spaces → weird symbols  

If you see anything except dots, fix it.

---

## 2. GitHub Actions YAML Is Not Pure YAML  
GitHub interprets YAML as a workflow graph.

This means:

- wrong indentation → job ignored  
- wrong key → step ignored  
- wrong trigger → workflow never runs  
- wrong field → silent failure  

YAML won’t warn you.  
GitHub won’t warn you.  
It just… doesn’t run.

### How to protect yourself  
Validate your YAML structure here:

[https://yamlchecker.com/](https://yamlchecker.com/)

This catches indentation errors before GitHub does.

---

## 3. Invisible Unicode Characters Are a Real Threat  
Copy/pasting from:

- chat  
- markdown  
- websites  
- formatted text  

…can introduce invisible characters that look like spaces but aren’t.

These break GitHub Actions.

### How to protect yourself  
Add this to `.editorconfig`:

```ini
[*]
indent_style = space
indent_size = 2
```

VS Code will enforce ASCII spaces.

---

## 4. GitHub Actions Deprecations Break Dormant Workflows  
GitHub Actions evolves.  
Your YAML does not.

A workflow that worked 4 years ago may fail today because:

- Node.js 16/18/20 was removed  
- Ubuntu 18.04/20.04 was removed  
- old action versions were deprecated  

### How GitHub handles deprecations  
1. **Soft warning**  
2. **Hard warning**  
3. **Removal** → workflow breaks

### How to protect yourself  
Use the latest actions:

- `actions/checkout@v5`  
- `actions/setup-python@v6`  

These are Node.js 24‑native.

---

## 5. GitHub Actions Does Not Validate YAML Locally  
VS Code cannot tell you:

- if your workflow is valid  
- if your triggers are correct  
- if your jobs are recognized  
- if your steps are structured correctly  

GitHub only validates after you push.

### How to protect yourself  
Use GitHub’s built‑in workflow linter:

```
gh workflow lint
```

(If you use GitHub CLI)

---

## 6. Silent Failures Are Normal  
GitHub Actions will silently ignore:

- invalid jobs  
- invalid steps  
- invalid triggers  
- invalid indentation  
- invalid fields  

You will see:

- no red X  
- no yellow warning  
- no workflow run  
- nothing at all

### How to protect yourself  
Check the “Actions” tab after every push.

If your workflow doesn’t appear:

- your YAML is malformed  
- your trigger didn’t fire  
- your indentation is wrong  
- your file is in the wrong folder  
- your file contains invisible characters  

---

## 7. The `.github/workflows` Folder Must Be Exact  
GitHub will ignore your workflow if:

- the folder name is wrong  
- the file extension is wrong  
- the file name contains hidden characters  
- the file is nested incorrectly  

Correct structure:

```
.github/
  workflows/
    your-workflow.yml
```

---

## 8. Python Projects Should Not pip‑install Themselves From GitHub  
If your repo contains your package, do **not** put this in `requirements.txt`:

```
git+https://github.com/you/yourrepo.git
```

This forces pip to clone your private repo, which fails in CI.

### Correct pattern

```
-e .
```

This installs your package locally.

---

## 9. YAML Is Not a Programming Language  
YAML was designed for configuration, not logic.

GitHub Actions uses YAML as a DSL, which creates fragility.

### How to protect yourself  
Keep workflows simple:

- one job per file  
- minimal steps  
- minimal conditionals  
- avoid complex matrix logic unless needed  

---

## 10. Always Pin Versions  
GitHub Actions changes defaults over time.

Pin versions explicitly:

```yaml
uses: actions/checkout@v5
uses: actions/setup-python@v6
```

This prevents surprise breakage.

---

# 🧪 Quick Checklist (copy this into your repo)

- [ ] Use `.editorconfig` to enforce ASCII spaces  
- [ ] Turn on whitespace rendering in VS Code  
- [ ] Validate YAML indentation  
- [ ] Keep workflows in `.github/workflows`  
- [ ] Remove git+https self‑dependencies  
- [ ] Pin action versions (`checkout@v5`, `setup-python@v6`)  
- [ ] Watch for deprecation warnings  
- [ ] Keep workflows simple  
- [ ] Test workflows after every push  

---

If you want, I can also write:

- a **GitHub Actions troubleshooting guide**  
- a **Python CI best practices guide**  
- a **workflow modernization checklist**  

Just tell me which one you want next.