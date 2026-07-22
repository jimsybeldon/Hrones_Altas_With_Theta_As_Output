`uv` is an extremely fast, modern **Python package and project manager** written in Rust, designed to be a drop-in replacement for traditional tools like **`pip`**, **`venv`**, and **`pip-tools`**. This means you can often replace your familiar `pip` commands with their `uv` equivalent.

Here is a general guide on how to use `uv` for installing packages and managing your environment.

-----

## 🚀 Key `uv` Commands

The `uv` tool offers a comprehensive set of commands that often simplify and combine the steps you would take with multiple separate tools (like creating a virtual environment, installing, and locking dependencies).

### 1\. Installing `uv`

Before you can use it, you need to install the `uv` binary. The recommended method is via the standalone installer:

* **macOS and Linux:**

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

* **Windows (PowerShell):**

    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

You can also install it using `pipx` or `pip` itself:

```bash
pipx install uv
# or
pip install uv
```

### 2\. Package Installation (The `pip` Interface)

For straightforward package installation, `uv` provides a **`pip` interface** which is designed to feel identical to running `pip` but with significant speed improvements.

| `pip` Command | `uv` Equivalent Command | Purpose |
| :--- | :--- | :--- |
| `python -m venv .venv` | **`uv venv`** | Create a virtual environment (automatically defaults to `.venv`). |
| `pip install requests` | **`uv pip install requests`** | Install a package into the active environment. |
| `pip install -r requirements.txt` | **`uv pip install -r requirements.txt`** | Install packages from a requirements file. |
| `pip uninstall requests` | **`uv pip uninstall requests`** | Remove a package. |
| `pip freeze` | **`uv pip freeze > requirements.txt`** | Output installed packages in requirements format. |

### 3\. Project Management (The Recommended Way)

For new projects, the official documentation often recommends using the higher-level project management commands, which automatically handle virtual environments and dependency locking.

* **Initialize a New Project:**

    ```bash
    uv init myproject
    cd myproject
    ```

    This command automatically creates a project directory, a **virtual environment** (`.venv`), and a `pyproject.toml` file.

* **Add a Dependency:**

    ```bash
    uv add requests
    ```

    This command **resolves and installs** the `requests` package (and its dependencies) into your project's virtual environment. It's similar to `pip install`, but also manages the environment and can update project files.

* **Synchronize Dependencies:**

    ```bash
    uv sync
    ```

    This command installs all dependencies listed in your project's configuration (`pyproject.toml` or `requirements.txt`) into the virtual environment, ensuring it matches the defined state. This is often used when setting up a project on a new machine.

* **Run a Script or Command:**

    ```bash
    uv run python my_script.py
    ```

    This executes a command *within* the project's virtual environment without you needing to explicitly activate it first.

### Key Advantages of `uv`

* **Speed:** `uv` is consistently **10-100x faster** than `pip` and `pip-tools` for dependency resolution and package installation due to being written in Rust and using parallel operations.
* **Integrated Tooling:** It combines the functionality of **`pip`**, **`venv`**, **`pip-tools`** (for dependency locking/compiling), and **`pipx`** (for installing command-line tools) into a single, cohesive utility.
* **Reproducibility:** It is designed to ensure reproducible builds by automatically managing and creating lock files (`uv.lock`) which pin the exact version of every dependency.

-----

The video below offers a complete guide on how to install and use `uv`, showing how it replaces and speeds up your existing package management workflow.

[UV Python Tutorial: 10-100x Faster Than pip\! Complete Guide 2025](https://www.youtube.com/watch?v=Em4BNYJpgTk)

<http://googleusercontent.com/youtube_content/0>
