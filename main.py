#!/usr/bin/env python3
"""Write one one-line summary of the week for make.fun to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The entry is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: exactly one line, 1 to 100 characters, not only
white space, no em dash.
"""

import os
import sys
from pathlib import Path

ENTRY = "120 entries in, zero wins, three builds broke, still queued the next one."

MIN_CHARS = 1
MAX_CHARS = 100
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: one line, 1 to 100 chars.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry is {chars} characters, outside 1-100")
    if not text.strip():
        raise ValueError("entry is only white space")
    if "\n" in text.strip():
        raise ValueError("entry must be exactly one line")
    if text != text.strip():
        raise ValueError("entry must not start or end with white space")
    if "\u2014" in text:
        raise ValueError("entry must not contain an em dash")
    return chars


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        print("Usage: python3 main.py [OUTPUT_PATH]")
        print("Writes the entry line to OUTPUT_PATH, $OUTPUT_PATH,")
        print("or /output/entry.txt by default.")
        return 0

    try:
        chars = validate(ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ENTRY, encoding="utf-8")
    print(ENTRY)
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
