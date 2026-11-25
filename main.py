#!/usr/bin/env python3
"""One Line, One Laugh — writes a single original hilarious line to entry.txt.

Standard library only, deterministic: the line is a fixed string.
Honours MAKEFUN_OUTPUT_DIR (default /output). Atomic write via a temp
file on the same filesystem, chmod 0644, os.replace.
"""

import os
import sys
import tempfile

LINE = "I asked my plants what they thought of me; they died rather than answer."


def main() -> int:
    text = LINE
    # Runtime self-check: 1-200 chars, not whitespace-only, single line.
    if not (1 <= len(text) <= 200):
        print(f"entry length {len(text)} out of range 1-200", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry is whitespace-only", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    data = text.encode("utf-8")
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, out_path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
