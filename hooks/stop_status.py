#!/usr/bin/env python3
"""H3 — Stop hook: remind (never brick) when fleet-status shows red.

Runs `tools/fleet_status.py --json` at the end of a turn. If any check is
red, prints a one-line reminder. Non-blocking by default; pass --block to
upgrade to a hard stop-blocker (the reminder is then fed back to the model
as {"decision": "block"}).

Wiring: see hooks/README.md and hooks/settings.example.json.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    block = "--block" in sys.argv
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}
    cwd = Path(payload.get("cwd", "."))
    checker = cwd / "tools" / "fleet_status.py"
    if not checker.exists():
        return 0
    try:
        r = subprocess.run(
            [sys.executable, str(checker), "--json"],
            capture_output=True, text=True, timeout=60, cwd=str(cwd),
        )
    except Exception as e:  # noqa: BLE001 — a broken reminder must not brick the session
        print(f"[fleet-status] hook error ({e}); skipping", file=sys.stderr)
        return 0
    if r.returncode != 1:
        return 0  # green (0) or checker self-error (2): stay silent

    try:
        reds = [c for c in json.loads(r.stdout).get("checks", []) if c.get("level") == "red"]
        summary = "; ".join(f"{c['id']}: {c['message']}" for c in reds[:3])
    except (json.JSONDecodeError, KeyError):
        summary = "run `python tools/fleet_status.py` for details"
    msg = f"fleet-status has RED gate violations — {summary}"
    if block:
        print(json.dumps({"decision": "block", "reason": msg}))
    else:
        print(f"[fleet-status] {msg}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
