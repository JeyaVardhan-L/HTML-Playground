#!/usr/bin/env python3
"""
Launcher script that automatically executes generate.py using the project-local
virtual environment (tools/lab-report-generator/.venv).
Enables seamless execution via:
    npm run lab-report -- --assignment 2
    python tools/lab-report-generator/run.py --assignment 2
"""

import os
import sys
import subprocess
from pathlib import Path

# Configure stdout and stderr for UTF-8 encoding
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TOOLS_DIR = Path(__file__).resolve().parent
VENV_PYTHON_WIN = TOOLS_DIR / ".venv" / "Scripts" / "python.exe"
VENV_PYTHON_UNIX = TOOLS_DIR / ".venv" / "bin" / "python"
GENERATE_SCRIPT = TOOLS_DIR / "generate.py"


def main():
    # Pick python interpreter
    if os.name == "nt" and VENV_PYTHON_WIN.exists():
        py_exe = str(VENV_PYTHON_WIN)
    elif VENV_PYTHON_UNIX.exists():
        py_exe = str(VENV_PYTHON_UNIX)
    else:
        # Fallback to current running python interpreter
        py_exe = sys.executable

    cmd = [py_exe, str(GENERATE_SCRIPT)] + sys.argv[1:]
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
