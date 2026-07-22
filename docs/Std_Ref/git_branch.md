# Understanding and Using Git Branches

This guide explains what Git branches are, why they are useful, and how to use them for common development workflows.

---

## What is a Branch?

A branch in Git is like a movable pointer to a specific commit. Think of it as an independent line of development. When you start a project, you begin on a default branch, usually named `main` or `master`.

When you create a new branch, you are essentially creating a new pointer that starts from your current commit. This allows you to work on a new feature, a bug fix, or an experimental idea in isolation without affecting the main codebase.

**Why use branches?**

- **Isolation:** Work on new features without destabilizing the main project.
- **Collaboration:** Multiple developers can work on different features simultaneously on their own branches.
- **Organization:** Keep different lines of work separate. For example, a `Dev` branch for ongoing development, a `feature-x` branch for a new feature, and a `hotfix-y` branch for an urgent bug fix.

---

## Common Git Branch Commands

Here are the essential commands for working with branches.

### 1. List Branches

To see all the branches in your local repository. The current branch will be marked with an asterisk (`*`).

```bash
git branch
```

### 2. Create a New Branch

This creates a new branch based on your current commit, but **does not** switch to it.

```bash
git branch <new-branch-name>
# Example: git branch Dev
```

### 3. Switch to a Branch

This command moves your working directory to the state of the specified branch.

```bash
git checkout <branch-name>
# Or the modern equivalent:
git switch <branch-name>
```

### 4. Create and Switch to a New Branch

This is a very common shortcut that combines creating and switching into one command.

```bash
git checkout -b <new-branch-name>
# Or the modern equivalent:
git switch -c <new-branch-name>
# Example: git checkout -b Dev
```

### 5. Delete a Branch

Once you have merged the changes from a branch, you can safely delete it. The `-d` flag prevents deletion if the branch has unmerged changes.

```bash
git branch -d <branch-name>
```

---

## Basic Workflow Example

1. **Start on the main branch:** `git checkout main`
2. **Create a new branch for your work:** `git checkout -b Dev`
3. **Make changes and commit them:**

    ```bash
    git add .
    git commit -m "Add new feature"
    ```

4. **When finished, switch back to the main branch:** `git checkout main`
5. **Merge your development branch into main:** `git merge Dev`
6. **(Optional) Push the changes to GitHub:** `git push origin main`
7. **(Optional) Delete the local development branch:** `git branch -d Dev`
