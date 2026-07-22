# Managing Python Project Requirements

This document outlines how to manage the `requirements.txt` file for your Python project.

## 1. Updating `requirements.txt` from the Environment

If you have installed new packages in your virtual environment and want to record all of them (including their dependencies) for exact replication, you can use the `pip freeze` command.

This command lists every installed package and its exact version.

**Command:**

```bash
pip freeze > requirements.txt
```

> **Use Case:** This is ideal for creating a snapshot of a working environment to ensure it can be perfectly recreated elsewhere. However, it can make the requirements file verbose as it includes packages that are dependencies of your main packages.

## 2. Cleaning Up to Core Requirements

Over time, your `requirements.txt` can become cluttered. A best practice is to only list the top-level packages your project directly depends on. A great tool for this is `pipreqs`, which scans your project's code for imports and generates a clean `requirements.txt` based on what is actually used.

### Step 1: Install `pipreqs`

First, install the tool into your environment.

```bash
pip install pipreqs
```

### Step 2: Generate Clean Requirements

Navigate to your project's root directory (`USDA_Nutrition_Analyser`) in the terminal and run the following command. The `--force` flag will overwrite your existing `requirements.txt` file.

```bash
pipreqs . --force
```

After running this, inspect the new `requirements.txt`. It will be much cleaner, containing only the packages you directly import in your `.py` files, like `pandas`, `openpyxl`, and `requests`. This makes your project easier for others to understand and manage.

## 3. Installing Packages from `requirements.txt`

To install all the packages listed in the `requirements.txt` file into your currently active virtual environment, run the following command.

> **Important:** Ensure your project's virtual environment is active before running this command. Your terminal prompt should be prefixed with `(.venv)`.

```bash
pip install -r requirements.txt