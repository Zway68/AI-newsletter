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

## 3. Building Angular with aspect_rules_js v3 and Bzlmod
- **Load Path**: Use the canonical Bazel external repo name: `@@aspect_rules_js++npm+npm__at_angular_cli__<VERSION>//:package_json.bzl`. Find the correct name with `ls bazel-<workspace>/external/ | grep angular_cli`. This is the correct approach — the `@npm` external repo does NOT contain `package_json.bzl` files.
- **Avoid cross-package issues**: Move `angular.json` and `tsconfig.json` into the same Bazel package as the frontend BUILD (e.g. `frontend/`). This avoids `copy_to_bin` complexity. Update paths in `angular.json` (`root`, `sourceRoot`, etc.) to be relative.
- **Output directories**: Use `out_dirs = ["dist"]` (not `outs`) and `chdir = package_name()` with `--output-path=dist` so Angular writes output in the correct sandbox location.
- **pnpm files**: `package.json` and `pnpm-lock.yaml` must stay at the workspace root (required by pnpm/`npm_translate_lock`), but are NOT needed in `ng build` srcs.
- **Note**: The canonical repo name is version-pinned. When `pnpm-lock.yaml` updates the `@angular/cli` version, the load path must be updated.
