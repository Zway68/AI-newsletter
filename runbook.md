# AI Newsletter Runbook: Running Python with Bazel

This runbook provides instructions on how to use Bazel to execute Python scripts and applications within this repository. We use Bazel's `rules_python` with `bzlmod` to manage dependencies via `pip` and `requirements.txt`.

## Prerequisites
- **Bazel 9.0+** (or `bazelisk` installed via npm/brew)
- Python 3.11 installed on your system.
- Dependencies are managed in `requirements.txt`.

## How Bazel Manages Python Dependencies
Bazel isolates its environment. It parses `requirements.txt` via the `pip` extension in `MODULE.bazel` and downloads the wheels automatically into its sandbox.

- **To add a dependency**: Add it to `requirements.txt`.
- Bazel will automatically download it the next time you run or test a target.

## Running a Python Program
Instead of running `python backend/main.py` directly, you run the binary through Bazel. In the `backend/BUILD.bazel` file, there is a `py_binary` target defined as `main`.

To start the API server and serve the frontend:
```bash
bazelisk run //backend:main
```
This command will:
1. Build the isolated Python environment.
2. Link the required dependencies (e.g., FastAPI, Uvicorn).
3. Bundle the frontend static files.
4. Execute the `main.py` script, starting the server at `http://0.0.0.0:8000`.

## Running Python Unit Tests
We use `pytest` wrapped in Bazel `py_test` targets. 

To run all tests in the repository:
```bash
bazelisk test //...
```

To run a specific test target (e.g., the backend API tests):
```bash
bazelisk test //backend/tests:test_api
```

## Adding New Python Code
When you add a new Python file:
1. If it's a library (to be imported by other files), add a `py_library` target in the `BUILD.bazel` file in its directory.
2. If it's an executable script, add a `py_binary` target.
3. If it uses external PyPI packages, load `requirement` from `@pip//:requirements.bzl` and add `requirement("package_name")` to the `deps` list of your target.
