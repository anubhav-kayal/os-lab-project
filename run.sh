#!/usr/bin/env bash
# Launch the GUI using a Python that has Tkinter (_tkinter).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

candidates=(
  "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
  "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"
  "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3"
  "/usr/local/bin/python3"
  "/usr/bin/python3"
  "python3"
)

pick=""
for py in "${candidates[@]}"; do
  if command -v "$py" >/dev/null 2>&1 || [[ -x "$py" ]]; then
    if "$py" -c "import tkinter" >/dev/null 2>&1; then
      pick="$py"
      break
    fi
  fi
done

if [[ -z "$pick" ]]; then
  echo "No Python with Tkinter found." >&2
  echo "Install python.org macOS Python, or: brew install python-tk" >&2
  exit 1
fi

echo "Using: $pick"
"$pick" -m pip install -q -r requirements.txt
exec "$pick" src/main.py
