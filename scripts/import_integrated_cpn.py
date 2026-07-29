#!/usr/bin/env python3
"""Import and validate the exact integrated SPoS-MSC CPN Tools model.

The repository does not silently substitute a component or proxy model.  This
helper copies the manuscript-linked integrated model into the canonical path,
checks that it is a CPN Tools XML document, records its tool version, and
writes a SHA-256 digest for release provenance.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
from pathlib import Path

CANONICAL_NAME = "SPoS_MSC_Complete_Benchmark_Hierarchical_Executable_v2.cpn"
REQUIRED_MARKERS = (
    "<workspaceElements",
    "<cpnet>",
    "SPoS-MSC",
    "RECEIPT",
    "COMMITMENT",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def decode_cpn(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("iso-8859-1", "utf-8"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode {path} as ISO-8859-1 or UTF-8")


def detect_version(text: str) -> str:
    match = re.search(r'<generator\s+tool="CPN Tools"\s+version="([^"]+)"', text)
    return match.group(1) if match else "unknown"


def validate(text: str) -> list[str]:
    missing = [marker for marker in REQUIRED_MARKERS if marker not in text]
    if "<generator" not in text or "CPN Tools" not in text:
        missing.append("CPN Tools generator declaration")
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Path to the exact integrated .cpn file")
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (default: inferred from this script)",
    )
    parser.add_argument(
        "--allow-noncanonical-name",
        action="store_true",
        help="Allow a source filename different from the manuscript-linked canonical filename",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    if not source.is_file():
        print(f"ERROR: source file does not exist: {source}", file=sys.stderr)
        return 2
    if source.suffix.lower() != ".cpn":
        print("ERROR: source must have a .cpn extension", file=sys.stderr)
        return 2
    if source.name != CANONICAL_NAME and not args.allow_noncanonical_name:
        print(
            f"ERROR: expected {CANONICAL_NAME!r}, got {source.name!r}. "
            "Use --allow-noncanonical-name only after verifying manuscript provenance.",
            file=sys.stderr,
        )
        return 2

    text = decode_cpn(source)
    missing = validate(text)
    if missing:
        print("ERROR: CPN validation failed; missing markers:", file=sys.stderr)
        for marker in missing:
            print(f"  - {marker}", file=sys.stderr)
        return 3

    destination_dir = args.repo / "model" / "integrated"
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / CANONICAL_NAME
    shutil.copy2(source, destination)

    digest = sha256(destination)
    version = detect_version(text)
    provenance = destination_dir / "MODEL_PROVENANCE.txt"
    provenance.write_text(
        "SPoS-MSC integrated model provenance\n"
        "====================================\n"
        f"Canonical file: {CANONICAL_NAME}\n"
        f"Imported from: {source}\n"
        f"CPN Tools version declared by file: {version}\n"
        f"SHA-256: {digest}\n",
        encoding="utf-8",
    )

    print(f"Imported: {destination}")
    print(f"CPN Tools version: {version}")
    print(f"SHA-256: {digest}")
    print(f"Provenance record: {provenance}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
