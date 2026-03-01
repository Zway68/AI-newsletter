---
name: Package Managers
description: Rules for managing Python and JavaScript dependencies
---

# Package Manager Guidelines

When working on this project (AI-newsletter), you MUST strictly use the following package managers for their respective languages:

## 1. Python: Pip & Bazel
- **Always** use `pip` and manage dependencies via `requirements.txt`.
- **Do not** use `conda`, `virtualenv`, or `poetry`.
- The environment and third-party dependencies are strictly managed by Bazel via `MODULE.bazel`.
- To install new packages, add them to `requirements.txt` at the root of the workspace.
- **CRITICAL EXECUTION RULE**: Whenever running Python scripts or tests, you MUST use Bazel. Do not invoke the global `python` executable. Use `bazelisk run //path/to:target` or `bazelisk test //path/to:target`.

## 2. JavaScript: NPM
- **Always** use `npm` for managing JavaScript/Node.js dependencies.
- **Do not** use `yarn` or `pnpm`.
- The package configuration is stored in `env/package.json`.
- All JS dependencies can be installed or updated by running `./install.sh`. Alternatively, `npm install` commands should be run by navigating to the `env` directory where the `package.json` resides.

By enforcing these standards, we ensure consistency across all local and remote environments.
