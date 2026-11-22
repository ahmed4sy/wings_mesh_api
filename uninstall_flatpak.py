#!/usr/bin/env python3
"""Remove only the managed import-path hook from the Flathub Wings init.py."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from wings_installer import discover_plugins_dirs, INIT_RELATIVE, remove_bootstrap, API_FOLDER


def main() -> int:
    parser = argparse.ArgumentParser(description="Remove the Wings Mesh API bootstrap hook.")
    parser.add_argument("--plugins-dir", type=Path, help="Explicit Wings plugins directory.")
    parser.add_argument("--remove-package", action="store_true", help="Also delete plugins/mesh_tools and mesh_tools.conf.")
    args = parser.parse_args()
    candidates = discover_plugins_dirs()
    target = args.plugins_dir or (candidates[-1] if candidates else None)
    if target is None:
        parser.error("No Flathub Wings installation found; pass --plugins-dir.")
    init_path = target / INIT_RELATIVE
    changed = remove_bootstrap(init_path)
    print("Bootstrap hook removed." if changed else "No managed bootstrap hook was present.")
    if args.remove_package:
        shutil.rmtree(target / API_FOLDER, ignore_errors=True)
        conf = target / "mesh_tools.conf"
        if conf.exists():
            conf.unlink()
        print("Installed API files and mesh_tools.conf removed.")
    else:
        print("API files were kept. Use --remove-package to delete them as well.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
