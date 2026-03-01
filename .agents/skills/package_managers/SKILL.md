---
name: Package Managers
description: Rules for managing Python and JavaScript dependencies
---

# Package Manager Guidelines

When working on this project (AI-newsletter), you MUST strictly use the following package managers for their respective languages:

## 1. Python: Conda
- **Always** use `conda` for managing Python environments and dependencies.
- **Do not** use `virtualenv`, `venv`, or `poetry`.
- The environment configuration is stored in `env/environment.yml`.
- To install new packages, update the `env/environment.yml` file and then run `./setup.sh` to apply the changes (or use `conda env update --file env/environment.yml --prune`).
- **CRITICAL EXECUTION RULE**: Whenever running Python scripts or tests, you MUST use `conda run -n ai-newsletter --no-capture-output python <script.py>` or the equivalent utility command, rather than activating the environment manually or using the global `python` executable.

## 2. JavaScript: NPM
- **Always** use `npm` for managing JavaScript/Node.js dependencies.
- **Do not** use `yarn` or `pnpm`.
- The package configuration is stored in `env/package.json`.
- All JS dependencies can be installed or updated by running `./setup.sh`. Alternatively, `npm install` commands should be run by navigating to the `env` directory where the `package.json` resides.

By enforcing these standards, we ensure consistency across all local and remote environments.
