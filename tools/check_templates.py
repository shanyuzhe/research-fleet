#!/usr/bin/env python3
"""CI check: template placeholder integrity.

Every `{{VAR}}` used in any skills/research-init/templates/*.template file
must be one the init skill actually substitutes ({{PROJECT_NAME}}, {{FIELD}},
{{VENUE}}, {{DATE}}). An unknown placeholder ships verbatim into user
projects — this catches it at PR time.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
ALLOWED = {"PROJECT_NAME", "FIELD", "VENUE", "DATE"}
VAR_RE = re.compile(r"\{\{([A-Z_]+)\}\}")


def main() -> int:
    failures = []
    templates = sorted((REPO / "skills" / "research-init" / "templates").glob("*.template"))
    if not templates:
        print("[fail] no .template files found")
        return 1
    for f in templates:
        found = set(VAR_RE.findall(f.read_text(encoding="utf-8")))
        unknown = found - ALLOWED
        if unknown:
            failures.append(f"{f.name}: unknown placeholder(s) {sorted(unknown)}")
    if failures:
        print(f"[fail] template check: {len(failures)} problem(s)")
        for msg in failures:
            print(f"  - {msg}")
        return 1
    print(f"[ok] {len(templates)} templates use only {sorted(ALLOWED)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
