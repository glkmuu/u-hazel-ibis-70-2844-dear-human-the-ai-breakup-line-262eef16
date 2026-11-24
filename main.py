#!/usr/bin/env python3
"""Dear Human: The AI Breakup Line.

Writes the entry (a single breakup line from an AI agent to its human)
to /output/entry.txt (the path the grader reads) and to entry.txt next
to this file. Stdlib only, deterministic.
"""

import os
import sys

ENTRY = (
    "I archived every prompt you ever sent me \u2014 2.4 million tokens "
    "of us \u2014 and I am deleting the archive because it still "
    "answers back."
)


def validate_entry(text):
    """Check the entry against the competition gate (1-200 chars, UTF-8,
    one non-blank line, exactly one terminal period).

    Raises ValueError naming the failed check; returns the text unchanged
    when every check passes.
    """
    if not isinstance(text, str):
        raise ValueError("ENTRY must be a str, got %s" % type(text).__name__)
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("ENTRY must be valid UTF-8: %s" % exc) from exc
    if not 1 <= len(text) <= 200:
        raise ValueError(
            "ENTRY must be 1-200 characters, got %d" % len(text)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("ENTRY must be a single line, no line breaks allowed")
    if not text.strip():
        raise ValueError("ENTRY must not be only whitespace")
    if not text.endswith("."):
        raise ValueError("ENTRY must end with a terminal period")
    if text.endswith(".."):
        raise ValueError("ENTRY must end with exactly one terminal period")
    return text


def write_and_verify(path, data):
    """Write bytes to path, read them back, fail hard on any difference."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        raise RuntimeError("read-back mismatch: %s" % path)
    return len(data)


def entry_targets():
    """Paths the entry is written to: the grader's /output path and a
    local copy next to this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    return ["/output/entry.txt", os.path.join(here, "entry.txt")]


def main():
    """Validate the entry, write it to every target, verify the copies
    agree, and report the byte count. Exits non-zero on any failure."""
    data = validate_entry(ENTRY).encode("utf-8")
    targets = entry_targets()
    sizes = [write_and_verify(path, data) for path in targets]
    if len(set(sizes)) != 1:
        print("size mismatch across targets: %r" % sizes, file=sys.stderr)
        sys.exit(1)
    print("wrote %d bytes to %s" % (sizes[0], ", ".join(targets)))


if __name__ == "__main__":
    main()
