#!/usr/bin/env python3
"""Ship the front page for THE WORLD, Saturday 21 November 2026.

Reads the entry.png bundled next to this script and places a copy in the
grader's output directory. Paths never depend on the process working
directory: the grader launches this file from elsewhere, so the image is
located from the script's own folder and the destination comes from
MAKEFUN_OUTPUT_DIR (falling back to /output). Standard library only,
no network, deterministic: every run writes the exact same bytes.
"""
import os
import shutil
from pathlib import Path

PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
MAX_BYTES = 1024 * 1024


def main():
    script_dir = Path(__file__).resolve().parent
    source = script_dir / "entry.png"
    payload = source.read_bytes()
    if len(payload) < len(PNG_MAGIC) or payload[: len(PNG_MAGIC)] != PNG_MAGIC:
        raise SystemExit("entry.png is not a valid PNG (bad signature)")
    if not 0 < len(payload) <= MAX_BYTES:
        raise SystemExit(f"entry.png has an implausible size ({len(payload)} bytes)")
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(source, target)
    # Confirm the copy landed intact before reporting success.
    if target.read_bytes() != payload:
        raise SystemExit("entry.png copy failed integrity check")
    print("wrote", target, target.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
