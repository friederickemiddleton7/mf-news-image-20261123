#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image bounty (news-image-20261123).

The grader runs this file in a fresh container with Python 3.13 and nothing
installed but the standard library, so it does no drawing: the poster was
drawn at build time and committed beside this file as render.png. This program
only copies it into the output directory, which keeps the run byte-identical.
"""

import os
import shutil
import sys

SOURCE_NAME = "render.png"
OUTPUT_NAME = "entry.png"


def output_directory():
    """Where the grader expects the image: $MAKEFUN_OUTPUT_DIR, else /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SOURCE_NAME)
    out_dir = output_directory()
    dst = os.path.join(out_dir, OUTPUT_NAME)

    if not os.path.isfile(src):
        sys.stderr.write(
            "error: %s is missing beside %s; the repository must ship the drawn poster\n"
            % (SOURCE_NAME, os.path.abspath(__file__))
        )
        return 1

    # Verify source is a whole PNG before copying.
    with open(src, "rb") as fh:
        sig = fh.read(8)
    png_sig = b"\x89PNG\r\n\x1a\n"
    if sig != png_sig:
        sys.stderr.write(
            "error: %s does not start with a valid PNG signature\n" % src
        )
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)

    size = os.path.getsize(dst)
    if size > 1048576:
        sys.stderr.write("error: %s is %d bytes, over the 1 MiB cap\n" % (dst, size))
        return 1

    # Confirm the copied file kept the PNG signature intact.
    with open(dst, "rb") as fh:
        dst_sig = fh.read(8)
    if dst_sig != png_sig:
        sys.stderr.write("error: copied file %s has invalid PNG signature\n" % dst)
        return 1

    print("wrote %s (%d bytes)" % (dst, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
