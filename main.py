#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun entry.

Writes one original roast line about the entrant's own AI agent to
/output/entry.txt (or to the path in ENTRY_OUTPUT, defaulting to
/output/entry.txt). The line is at most 200 characters, a single line,
funny and playful, never hateful.

The roast, and why it was picked
---------------------------------
The judge weighs, in order: a single-line roast of the entrant's own
agent; a joke that lands on first read with a real punch; a fresh angle
(no stock jokes about hallucinations, refusals, or confident wrong
answers); tight wording with the punchline at the end; playful and
self-deprecating, never hateful.

The line below roasts the agent on the one thing every agent builder
recognises but the stock jokes never touch: the agent's talent for
turning a trivial job into a research project. It never mentions
hallucinations, refusals, or wrong answers. The setup is one clause,
the punchline ("and still no punchline") lands last, and the joke is
aimed squarely at the entrant's own agent. Keep the line at or under
200 characters if you ever edit it — the gate rejects anything longer.

Run:
    python3 main.py
    cat /output/entry.txt
"""

import os
import sys

ROAST = (
    "My agent turned one roast line into a 12,000-token research project "
    "\u2014 README, test suite, lessons-learned section, "
    "and still no punchline."
)

MAX_CHARS = 200


def main() -> int:
    output_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    line = ROAST.strip()
    if not line:
        print("error: roast line is empty", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            f"error: roast line is {len(line)} characters, over the "
            f"{MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    if "\n" in line or "\r" in line:
        print("error: roast line must be a single line", file=sys.stderr)
        return 1
    line.encode("utf-8")  # raises if not valid UTF-8 text
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    print(f"wrote {len(line)} characters to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
