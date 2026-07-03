#!/usr/bin/env python3
"""CI check: docs agree with the actual agent count — counted, not asserted.

v0.1 shipped saying "five agents" in four places while agents/ held seven
files; the drift survived 4 commits of human review. This script counts
`agents/*.md` and fails if any doc/template says "<numberword>-agent",
"<numberword> agents" or "<numberword> specialists" with the wrong number.
Add an eighth agent without touching the docs → CI goes red. That's the point.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent

NUMBER_WORDS = {
    "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10,
}
CN_NUMBERS = {"两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}

EN_RE = re.compile(
    r"\b(" + "|".join(NUMBER_WORDS) + r")[- ]agent(s)?\b"
    r"|\b(" + "|".join(NUMBER_WORDS) + r") specialists\b",
    re.IGNORECASE,
)
CN_RE = re.compile(r"([" + "".join(CN_NUMBERS) + r"])(?:人|个)\s*agent")

SCAN_GLOBS = ["*.md", "skills/**/*.md", "skills/**/*.template", "docs/*.md",
              "examples/**/*.md", "commands/*.md", "hooks/*.md"]
# Files that may legitimately mention historical counts (self-audits quote v0.1 bugs).
EXEMPT = {"docs/fleet/self_audit_2026-07-03.md", "docs/lessons.md", "docs/landscape.md",
          "docs/design.md"}


def read_text_longpath(f: Path) -> str:
    """Windows MAX_PATH-safe read: retry with the \\\\?\\ extended prefix."""
    try:
        return f.read_text(encoding="utf-8")
    except FileNotFoundError:
        if sys.platform == "win32":
            return Path("\\\\?\\" + str(f.resolve())).read_text(encoding="utf-8")
        raise


def main() -> int:
    actual = len(list((REPO / "agents").glob("*.md")))
    failures = []
    seen = set()
    for pattern in SCAN_GLOBS:
        for f in REPO.glob(pattern):
            rel = f.relative_to(REPO).as_posix()
            if rel in seen or rel in EXEMPT:
                continue
            seen.add(rel)
            text = read_text_longpath(f)
            for lineno, line in enumerate(text.splitlines(), 1):
                for m in EN_RE.finditer(line):
                    word = (m.group(1) or m.group(3)).lower()
                    if NUMBER_WORDS[word] != actual:
                        failures.append(f"{rel}:{lineno}: says '{m.group(0)}' but agents/ has {actual}")
                for m in CN_RE.finditer(line):
                    if CN_NUMBERS[m.group(1)] != actual:
                        failures.append(f"{rel}:{lineno}: says '{m.group(0)}' but agents/ has {actual}")

    if failures:
        print(f"[fail] agent-count consistency ({actual} agents on disk):")
        for msg in failures:
            print(f"  - {msg}")
        return 1
    print(f"[ok] all agent-count mentions match reality ({actual} agents, {len(seen)} files scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
