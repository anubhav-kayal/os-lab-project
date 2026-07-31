"""Application entrypoint: python src/main.py"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    """Allow `python src/main.py` to import sibling packages under src/."""
    src_dir = Path(__file__).resolve().parent
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))


def _tkinter_missing_message() -> str:
    """Return a platform-aware hint when Tk is not available."""
    exe = sys.executable
    return f"""
Tkinter is not available in this Python:

  {exe}

The scheduling tests can still run, but the GUI needs a Python build linked
with Tcl/Tk (the `_tkinter` module).

On macOS, try one of these instead:

  /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -m pip install -r requirements.txt
  /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 src/main.py

  # or:
  /usr/bin/python3 -m pip install -r requirements.txt
  /usr/bin/python3 src/main.py

Or install Tcl/Tk and rebuild your pyenv Python, e.g.:

  brew install tcl-tk
  # then reinstall the pyenv version so it links against that Tcl/Tk
""".strip()


def main() -> None:
    """Launch the CPU scheduling simulator GUI."""
    _ensure_src_on_path()
    try:
        from gui.app import run_app
    except ModuleNotFoundError as exc:
        if exc.name in {"_tkinter", "tkinter"} or "_tkinter" in str(exc):
            print(_tkinter_missing_message(), file=sys.stderr)
            raise SystemExit(1) from exc
        raise

    run_app()


if __name__ == "__main__":
    main()
