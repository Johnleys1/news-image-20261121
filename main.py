#!/usr/bin/env python3
"""Entry program for news-image-20261121: THE WORLD, Saturday 21 November 2026.

Copies the front-page image bundled in this repository to the output
directory. Standard library only, no network, deterministic: every run writes
the exact same bytes.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
