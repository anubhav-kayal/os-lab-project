"""Application entrypoint: python src/main.py"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    """Allow `python src/main.py` to import sibling packages under src/."""
    src_dir = Path(__file__).resolve().parent
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))


def main() -> None:
    """Launch the CPU scheduling simulator GUI."""
    _ensure_src_on_path()
    from gui.app import run_app

    run_app()


if __name__ == "__main__":
    main()
