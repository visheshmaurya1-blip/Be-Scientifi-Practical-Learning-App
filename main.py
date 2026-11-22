"""Unified Be Scientific desktop app entry point."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = ROOT / "be_scientific"


__version__ = "1.1.0"


def _configure_import_paths() -> None:
    """Expose the unified shell and the offline learning engine as packages."""
    for path in reversed((ROOT, PACKAGE_ROOT)):
        resolved = str(path)
        if resolved in sys.path:
            sys.path.remove(resolved)
        sys.path.insert(0, resolved)


def main() -> None:
    _configure_import_paths()
    from app.application import BeScientificApp

    BeScientificApp().run()


if __name__ == "__main__":
    main()
