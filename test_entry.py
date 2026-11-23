#!/usr/bin/env python3
"""Local gate check for the roast entry.

Mirrors the sealed scorer: /output/entry.txt must be UTF-8 text of
1 to 200 characters, not only white space, a single line.
"""

import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import ROAST  # noqa: E402


def main() -> int:
    failures = []
    line = ROAST.strip()
    if not line or line.isspace():
        failures.append("line is empty or only whitespace")
    if len(line) > 200:
        failures.append(f"line is {len(line)} chars, over the 200 limit")
    if "\n" in line or "\r" in line:
        failures.append("line is not a single line")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as e:
        failures.append(f"line is not valid UTF-8: {e}")

    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "entry.txt")
        env = dict(os.environ, ENTRY_OUTPUT=out)
        proc = subprocess.run(
            [sys.executable, "main.py"], env=env, capture_output=True, text=True
        )
        if proc.returncode != 0:
            failures.append(f"main.py exited {proc.returncode}: {proc.stderr}")
        else:
            with open(out, "rb") as f:
                raw = f.read()
            text = raw.decode("utf-8")
            if text.rstrip("\n") != line:
                failures.append("written file does not match ROAST")
            if len(text.rstrip("\n")) != len(line):
                failures.append("written file length mismatch")
            print(f"wrote {len(text.rstrip(chr(10)))} chars to entry.txt")

    print(f"roast line: {line!r} ({len(line)} chars)")
    if failures:
        for f in failures:
            print(f"FAIL: {f}")
        return 1
    print("PASS: entry is a valid single line of 1-200 UTF-8 characters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
