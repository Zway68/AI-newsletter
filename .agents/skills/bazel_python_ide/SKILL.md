---
name: Bazel Python IDE Integration
description: Rules for configuring VS Code and other IDEs to work with Bazel rules_python
---

# Bazel Python IDE Integration Guidelines

When working with `rules_python` in Bazel, the Python interpreter and site-packages are hidden in the Bazel cache. This causes broken IntelliSense and error squiggles in IDEs like VS Code (Pylance).

## 1. Bridging Bazel with a Local Virtual Environment
- **Rule**: Maintain a local `.venv` directory solely for the development environment.
- **Workflow**:
    1.  Generate a `requirements.txt` from your project's `requirements.in` (using `pip-compile`).
    2.  Create a local virtual environment: `python -m venv .venv`.
    3.  Populate it: `./.venv/bin/pip install -r requirements.txt`.
    4.  Instruct the IDE to use it (e.g., in `.vscode/settings.json` set `"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"`).

## 2. Path Mapping for Bazel-Generated Code
- If Bazel generates Python code (e.g., Protobufs or custom rule outputs), add the corresponding `bazel-bin` and `bazel-out` paths to the IDE's extra analysis paths.
- **Rule**: In VS Code, use `"python.analysis.extraPaths": ["${workspaceFolder}/bazel-bin", "${workspaceFolder}/bazel-out"]`.

## 3. Hermeticity vs. IDE Experience
- **Always** run/test using `bazelisk run` or `bazelisk test` to ensure hermetic correctness.
- **Always** use the `.venv` purely for IntelliSense, type checking, and navigation. Never rely on the system Python's state for the build.
