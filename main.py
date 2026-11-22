#!/usr/bin/env python3
"""Round 3 entrypoint — news-image-20261121.

Copies the front-page image (entry.png, drawn by draw_r3.py) to the
grader's output directory.

Paths are resolved from this script's own directory, never from the
process working directory: the grader runs `python3 /bot/main.py` from
elsewhere, so a relative "entry.png" would raise FileNotFoundError there.
The output directory comes from MAKEFUN_OUTPUT_DIR (fallback /output).
"""
import os
import shutil
from pathlib import Path

PNG_SIGNATURE = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
MAX_IMAGE_BYTES = 1024 * 1024


def main():
    script_dir = Path(__file__).resolve().parent
    source_path = script_dir / "entry.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target_path = output_dir / "entry.png"

    # A valid PNG always starts with this 8-byte signature. Fail loudly
    # here instead of silently shipping a broken image to the grader.
    data = source_path.read_bytes()
    if len(data) < len(PNG_SIGNATURE) or data[: len(PNG_SIGNATURE)] != PNG_SIGNATURE:
        raise SystemExit("entry.png is not a valid PNG (bad signature)")

    # Sanity-check the payload size: an empty file is a broken entry, and
    # the grader caps a single image at 1 MiB, so anything larger fails
    # there anyway.
    if len(data) == 0 or len(data) > MAX_IMAGE_BYTES:
        raise SystemExit(f"entry.png has an implausible size ({len(data)} bytes)")

    # Make sure the destination directory exists (the grader provides it,
    # but a missing dir should not be what fails the run).
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, target_path)

    # Integrity check on the copy: the shipped file must be byte-identical
    # to the source image, not just the same length.
    shipped = target_path.read_bytes()
    if shipped != data:
        raise SystemExit("copied entry.png differs from the source image")


if __name__ == "__main__":
    main()
