#!/usr/bin/env python3
"""
Clean generated artifacts from the repository.

Removes debug directories, C# intermediate directories and Python caches.
The ``bin/Release`` directory is explicitly protected and is never scanned
or removed. By default this only lists what would be removed; pass ``--apply``
to delete after confirmation, or ``--yes`` to skip the confirmation prompt.
"""

from __future__ import annotations

import argparse
import fnmatch
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
EXCLUDED = {".git", "cleaner.py"}
PROTECTED_DIR_NAMES = {"bin/release"}

CACHE_DIR_NAMES = {"__pycache__", ".pytest_cache", ".ruff_cache"}
CACHE_DIR_NAMES_CASEFOLDED = {name.casefold() for name in CACHE_DIR_NAMES}
CLEAN_DIR_NAMES = CACHE_DIR_NAMES_CASEFOLDED | {"debug", "obj"}
CACHE_FILE_PATTERNS = {"*.pyc"}


def _is_protected(path: Path) -> bool:
    """Return whether a directory must remain completely untouched."""
    return "/".join(path.parts[-2:]).casefold() in PROTECTED_DIR_NAMES


def _category(name: str, is_dir: bool) -> str | None:
    """Return the cleanup category for a path name, or None."""
    if is_dir and name.casefold() in CLEAN_DIR_NAMES:
        if name.casefold() in CACHE_DIR_NAMES_CASEFOLDED:
            return "caches"
        if name.casefold() in {"debug", "obj"}:
            return "build"
    if not is_dir and any(
        fnmatch.fnmatch(name, pattern) for pattern in CACHE_FILE_PATTERNS
    ):
        return "caches"
    return None


def _walk(targets: dict[str, list[Path]], current: Path) -> None:
    """Recursively collect removable paths while pruning protected paths."""
    try:
        children = sorted(current.iterdir(), key=lambda path: path.name.casefold())
    except OSError as exc:
        print(f"error reading {current}: {exc}", file=sys.stderr)
        return

    for child in children:
        if child.name in EXCLUDED:
            continue
        if child.is_dir() and _is_protected(child):
            continue

        category = _category(child.name, child.is_dir())
        if category is not None:
            targets[category].append(child)
            continue
        if child.is_dir() and not child.is_symlink():
            _walk(targets, child)


def collect_targets(root: Path) -> dict[str, list[Path]]:
    """Collect generated artifacts below root."""
    targets: dict[str, list[Path]] = {"caches": [], "build": []}
    _walk(targets, root)
    return targets


def print_targets(root: Path, targets: dict[str, list[Path]]) -> None:
    """Print collected artifacts grouped by category."""
    labels = {"caches": "Python caches", "build": "Debug and C# intermediates"}
    for category, items in targets.items():
        print(f"{labels[category]}:")
        for item in items:
            print(f"  {item.relative_to(root)}")
        if not items:
            print("  (none)")
        print()


def remove(targets: dict[str, list[Path]]) -> bool:
    """Remove collected artifacts and report failures."""
    ok = True
    for items in targets.values():
        for path in items:
            try:
                if path.is_dir() and not path.is_symlink():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                print(f"removed {path}")
            except OSError as exc:
                ok = False
                print(f"error removing {path}: {exc}", file=sys.stderr)
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="actually delete artifacts (default is a dry run)",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="skip the confirmation prompt (implies --apply)",
    )
    args = parser.parse_args()

    targets = collect_targets(REPO_ROOT)
    total = sum(len(items) for items in targets.values())
    print_targets(REPO_ROOT, targets)

    if total == 0:
        print("No removable artifacts found.")
        return 0

    if not args.apply and not args.yes:
        print(f"{total} item(s) found. Run with --apply to remove them.")
        return 0

    if not args.yes:
        answer = input(f"Remove {total} item(s)? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted.")
            return 0

    return 0 if remove(targets) else 1


if __name__ == "__main__":
    raise SystemExit(main())
