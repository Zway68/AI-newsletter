---
name: Bazel Web Testing and Configuration
description: Rules for testing Javascript in Bazel and setting up Python in Bazel 9
---

# Bazel 9 & Web Testing Guidelines

## 1. Bazel 9 Module Definition
- Starting with Bazel 9, `Bzlmod` is enabled by default. Legacy `WORKSPACE` configurations for `rules_python` or `rules_nodejs` will fail to resolve without proper manual flags.
- **Rule**: Always create a `MODULE.bazel` file in the repository root.
- To use Python, declare `bazel_dep(name = "rules_python", version = "0.31.0")` and use `pip_parse` to load dependencies from a locked `requirements.txt` file.

## 2. Testing JavaScript/Node.js in Bazel Sandbox
- **Problem**: Executing native Node.js tools like `jest` or `npm test` inside a Bazel `sh_test` is non-hermetic and prone to `Command not found` errors, as Bazel macOS/Linux sandboxes aggressively strip the host environment `PATH`.
- **Solution**: Avoid configuring brittle `rules_nodejs` when simple logic validation is required.
- **Rule**: Write a lightweight Python test wrapper (`py_test`) that reads and uses static assertions or `subprocess` to validate JavaScript logic. Because Python is strictly managed and hermetic under `rules_python`, a `py_test` wrapper **never** fails due to missing host binaries.
