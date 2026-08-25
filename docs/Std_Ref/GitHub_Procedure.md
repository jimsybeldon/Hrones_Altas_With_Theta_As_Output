# [Git CLI and More](https://git-scm.com/book/en/v2/Getting-Started-The-Command-Line)

Moving your SolidWorks BOM project from a local folder to a new GitHub repository is a great way to manage versions, especially as your Python scripts for ERP integration become more complex.

Since you are using **VS Code**, you can handle most of this through the integrated terminal or the Source Control GUI. Here is the workflow to get your "Solidworks Bom Print Project" live on GitHub.

---

## 1. Create the Repository on GitHub

Before running commands in VS Code, you need to create the "container" on GitHub.

1. Log in to your [GitHub account](https://github.com/).
2. Click the **+** icon in the top-right corner and select **New repository**.
3. **Repository name:** Enter `Solidworks-Bom-Print-Project` (GitHub usually replaces spaces with hyphens).
4. **Public/Private:** Choose based on whether you want to share this work or keep it internal.
5. **Initialize this repository:** **Leave these unchecked** (Add a README, .gitignore, or license). Since you already have local code, it is cleaner to start with a completely empty repository.
6. Click **Create repository**.

---

## 2. Initialize and Push from VS Code

Open your project folder in VS Code, then open the terminal (**Ctrl + `** or **Terminal > New Terminal**).

### A. Initialize Local Git

If you haven't initialized Git in this folder yet, run:

```bash
git init

```

### B. Add Your Files

Tell Git which files to track. For a BOM project, you’ll want to include your `.py` scripts and perhaps a sample CSV/Excel template, but **not** your actual ERP credentials or massive CAD binaries.

```bash
git add .

```

### C. Create the First Commit

```bash
git commit -m "Initial commit: Solidworks BOM Python processing scripts"

```

### D. Link to GitHub and Push

Copy the HTTPS URL from the empty GitHub page you just created (it will look like `https://github.com/YourUsername/Solidworks-Bom-Print-Project.git`).

```bash
# Set the main branch name
git branch -M main

# Add the remote link (replace the URL with yours)
git remote add origin https://github.com/jimsybeldon/Solidworks-Bom-Print-Project.git

# Push the code
git push -u origin main

```

---

## 3. Recommended: Create a `.gitignore`

In the root of your VS Code project, create a file named `.gitignore`. This prevents temporary or sensitive files from being uploaded. For your specific workflow, I suggest adding:

```text
# Python bytecode
__pycache__/
*.py[cod]

# Excel/CSV temporary files (if they contain sensitive ERP data)
~$*.xlsx
*.log

# Virtual environments
venv/
.venv/

```

---

### A Note on "Infected Doubt"

While this is the "proper" method, the friction point is usually the **GitHub Authentication**. VS Code will likely pop up a browser window asking you to sign in. If that fails, you might need to look into generating a **Personal Access Token (PAT)**, as GitHub no longer accepts standard passwords for command-line operations.

Would you like me to provide a `.py` template for a `README.md` file that explains how your BOM script handles the SolidWorks-to-ERP translation?