# uv_test.py: Check if running in the correct Python environment (uv-managed)
# If not running under the uv environment, print an error message and show the current Python executable and environment info.
import os
import sys

# Check for uv environment marker (pyproject.toml and uv.lock should exist)
# Optionally, check for a known uv environment variable or path pattern


def is_uv_environment():
    # Check for uv.lock in project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    uv_lock_path = os.path.join(project_root, "..", "uv.lock")
    pyproject_path = os.path.join(project_root, "..", "pyproject.toml")
    if not (os.path.exists(uv_lock_path) and os.path.exists(pyproject_path)):
        return False
    # Check if running in a .venv or uv environment (heuristic)
    # uv uses .venv by default, but user may override
    venv = os.environ.get("VIRTUAL_ENV", "")
    if venv and "uv" in venv:
        return True
    # Check sys.executable path for 'uv' or '.venv'
    if "uv" in sys.executable or ".venv" in sys.executable:
        return True
    return False


if __name__ == "__main__":
    if not is_uv_environment():
        print("[ERROR] This script is not running in the uv-managed Python environment.")
        print(f"sys.executable: {sys.executable}")
        print(f"VIRTUAL_ENV: {os.environ.get('VIRTUAL_ENV', '')}")
        print("Please activate the uv environment and try again (e.g., 'uv run src/uv_test.py').")
    else:
        print("[OK] Running in the uv-managed Python environment.")
