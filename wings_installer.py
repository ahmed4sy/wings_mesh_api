"""Safe installer helpers for Wings Mesh API on the Flathub build of Wings 3D."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

APP_ID = "com.wings3d.WINGS"
DATA_RELATIVE = Path(".var/app") / APP_ID / "data" / "Wings3D"
API_FOLDER = "mesh_tools"
INIT_RELATIVE = Path("wpc_scripting_shapes_init") / "py" / "init.py"
BEGIN_MARKER = "# >>> WINGS_MESH_API_BOOTSTRAP (managed) >>>"
END_MARKER = "# <<< WINGS_MESH_API_BOOTSTRAP (managed) <<<"


def _version_key(path: Path):
    """Sort version folders numerically where possible (2.10 > 2.9)."""
    parts = re.split(r"([0-9]+)", path.name)
    return tuple(int(part) if part.isdigit() else part.lower() for part in parts)


def discover_plugins_dirs(home: Path | None = None) -> list[Path]:
    home = Path(home or Path.home()).expanduser()
    wings_data = home / DATA_RELATIVE
    if not wings_data.is_dir():
        return []
    found = []
    for version_dir in wings_data.iterdir():
        plugins_dir = version_dir / "plugins"
        if plugins_dir.is_dir() and (plugins_dir / INIT_RELATIVE).is_file():
            found.append(plugins_dir)
    return sorted(found, key=lambda p: _version_key(p.parent))


def build_bootstrap_block() -> str:
    """Return a version-independent path hook for the original plugin init.py."""
    return f'''{BEGIN_MARKER}
# Expose the Mesh API package to every Shape/Command script, regardless of
# the script's own location. This is intentionally independent of Wings version.
from pathlib import Path as _WMAPath
_wma_plugins_dir = _WMAPath(__file__).resolve().parents[2]
_wma_api_candidates = (
    _wma_plugins_dir / "mesh_tools",
    _wma_plugins_dir / "plugin_scripts" / "mesh_tools",
)
for _wma_api_root in _wma_api_candidates:
    if (_wma_api_root / "wings" / "__init__.py").is_file():
        _wma_api_text = str(_wma_api_root)
        if _wma_api_text not in sys.path:
            sys.path.insert(0, _wma_api_text)
        break
if not any((_wma_root / "wings" / "__init__.py").is_file()
           for _wma_root in _wma_api_candidates) and __import__("os").environ.get("WINGS_MESH_API_DEBUG") == "1":
    sys.stderr.write("Wings Mesh API: package folder not found beside the scripting plugin\\n")
{END_MARKER}
'''


def patch_init(init_path: Path) -> bool:
    """Patch original init.py once; return True only when a change was made."""
    init_path = Path(init_path)
    source = init_path.read_text(encoding="utf-8")
    if BEGIN_MARKER in source and END_MARKER in source:
        return False
    if "run_path(script_file, g)" not in source or "import sys" not in source:
        raise RuntimeError(
            f"Refusing to patch unexpected scripting bootstrap: {init_path}. "
            "The expected wpc_scripting_shapes init.py markers were not found."
        )
    backup = init_path.with_name(init_path.name + ".wings-mesh-api.bak")
    if not backup.exists():
        shutil.copy2(init_path, backup)

    # Insert after the exact top-level import sys, before the script loader starts.
    anchor = "import sys\n"
    if anchor not in source:
        raise RuntimeError(f"Could not find safe insertion point in {init_path}")
    source = source.replace(anchor, anchor + build_bootstrap_block(), 1)
    init_path.write_text(source, encoding="utf-8")
    return True


def remove_bootstrap(init_path: Path) -> bool:
    """Remove only the managed block, preserving all other init.py changes."""
    init_path = Path(init_path)
    source = init_path.read_text(encoding="utf-8")
    start = source.find(BEGIN_MARKER)
    if start < 0:
        return False
    end = source.find(END_MARKER, start)
    if end < 0:
        raise RuntimeError(f"Bootstrap block is incomplete in {init_path}")
    end += len(END_MARKER)
    if end < len(source) and source[end] == "\n":
        end += 1
    source = source[:start] + source[end:]
    init_path.write_text(source, encoding="utf-8")
    return True


def install_into(plugins_dir: Path, source_root: Path) -> dict[str, Path | bool]:
    """Install API files and patch the corresponding scripting bootstrap."""
    plugins_dir = Path(plugins_dir).expanduser().resolve()
    source_root = Path(source_root).resolve()
    init_path = plugins_dir / INIT_RELATIVE
    package_source = source_root / "wings"
    if not init_path.is_file():
        raise FileNotFoundError(f"Original scripting init.py not found: {init_path}")
    if not (package_source / "__init__.py").is_file():
        raise FileNotFoundError(f"Wings package not found in release folder: {package_source}")

    api_root = plugins_dir / API_FOLDER
    api_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(package_source, api_root / "wings", dirs_exist_ok=True)
    for filename in ("parametric_box.py", "parametric_box.wscr"):
        source = source_root / filename
        if source.is_file():
            shutil.copy2(source, api_root / filename)
    config_source = source_root / "plugin_scripts" / "mesh_tools.conf"
    config_target = plugins_dir / "mesh_tools.conf"
    if config_source.is_file():
        if config_target.exists():
            backup_config = config_target.with_name(config_target.name + ".wings-mesh-api.bak")
            if not backup_config.exists():
                shutil.copy2(config_target, backup_config)
        shutil.copy2(config_source, config_target)

    changed = patch_init(init_path)
    return {
        "plugins_dir": plugins_dir,
        "api_root": api_root,
        "init_path": init_path,
        "init_patched": changed,
        "backup_path": init_path.with_name(init_path.name + ".wings-mesh-api.bak"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Install Wings Mesh API and make `from wings import Mesh` work from any script path."
    )
    parser.add_argument(
        "--plugins-dir", type=Path,
        help="Explicit Wings plugins directory. Auto-detected from the Flathub data directory if omitted.",
    )
    parser.add_argument("--list", action="store_true", help="List detected Flathub Wings plugin directories and exit.")
    args = parser.parse_args(argv)

    found = discover_plugins_dirs()
    if args.list:
        if not found:
            print("No Flathub Wings installation found.")
            return 1
        for item in found:
            print(item)
        return 0

    target = args.plugins_dir
    if target is None:
        if not found:
            print("ERROR: Could not locate Flathub Wings data directory.", file=sys.stderr)
            print(f"Expected: {Path.home() / DATA_RELATIVE / '<version>' / 'plugins'}", file=sys.stderr)
            print("Run with --plugins-dir /absolute/path/to/plugins to specify it manually.", file=sys.stderr)
            return 2
        target = found[-1]
        if len(found) > 1:
            print(f"Detected {len(found)} Wings installations; using newest: {target}")

    source_root = Path(__file__).resolve().parent
    try:
        result = install_into(target, source_root)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print("Wings Mesh API 1.3.0 installed successfully.")
    print(f"API package: {result['api_root']}")
    print(f"Patched engine: {result['init_path']}")
    print(f"Original backup: {result['backup_path']}")
    print("Restart Wings 3D. Scripts from any folder can now use: from wings import Mesh")
    print("The installer does not replace or rename the original init.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
