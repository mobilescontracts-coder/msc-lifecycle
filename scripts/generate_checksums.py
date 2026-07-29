#!/usr/bin/env python3
"""Generate a stable SHA-256 manifest for release-relevant repository files."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

EXCLUDED_PARTS = {".git", ".venv", "__pycache__", "outputs", "checksums"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def eligible(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return False
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root"
    )
    parser.add_argument(
        "--output", type=Path, default=None, help="Manifest path (default: checksums/SHA256SUMS)"
    )
    args = parser.parse_args()
    root = args.repo.resolve()
    output = args.output or (root / "checksums" / "SHA256SUMS")
    output.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    for path in sorted(root.rglob("*")):
        if eligible(path, root):
            lines.append(f"{file_digest(path)}  {path.relative_to(root).as_posix()}")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} checksums to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
