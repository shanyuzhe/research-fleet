#!/usr/bin/env python3
"""H1 — PreToolUse hook: mechanically reject illegal claim upgrades.

Fires on Edit/Write/MultiEdit. If the write would leave a file under claims/
with `status: verified`, the proposed content is checked via
`tools/fleet_status.py --check-claim` (C1 marker + C5 evidence). A violation
blocks the tool call (exit 2) with the reason on stderr.

Fail-open by design: if fleet_status.py is missing or errors, the call is
allowed with a warning — a broken hook must not brick the session.

Wiring: see hooks/README.md and hooks/settings.example.json.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

VERIFIED_RE = re.compile(r"^status:\s*verified\b", re.MULTILINE)


def proposed_content(tool_name: str, tool_input: dict, path: Path) -> str | None:
    """Reconstruct what the file would contain after the tool call."""
    if tool_name == "Write":
        return tool_input.get("content", "")
    current = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    if tool_name == "Edit":
        old, new = tool_input.get("old_string", ""), tool_input.get("new_string", "")
        if tool_input.get("replace_all"):
            return current.replace(old, new)
        return current.replace(old, new, 1)
    if tool_name == "MultiEdit":
        for e in tool_input.get("edits", []):
            old, new = e.get("old_string", ""), e.get("new_string", "")
            current = current.replace(old, new) if e.get("replace_all") else current.replace(old, new, 1)
        return current
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"[claim-gate] cannot parse hook payload ({e}); allowing", file=sys.stderr)
        return 0

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}
    if tool_name not in ("Write", "Edit", "MultiEdit"):
        return 0

    file_path = tool_input.get("file_path", "")
    if not file_path:
        return 0
    path = Path(file_path)
    cwd = Path(payload.get("cwd", "."))
    try:
        rel = path.resolve().relative_to(cwd.resolve())
    except ValueError:
        return 0  # outside the project
    if not (rel.parts and rel.parts[0] == "claims" and path.suffix == ".md"):
        return 0

    content = proposed_content(tool_name, tool_input, path)
    if content is None or not VERIFIED_RE.search(content):
        return 0  # not an upgrade to verified — no gate

    checker = cwd / "tools" / "fleet_status.py"
    if not checker.exists():
        print("[claim-gate] tools/fleet_status.py not found; allowing (install it to enforce)", file=sys.stderr)
        return 0

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tf:
        tf.write(content)
        tmp = tf.name
    try:
        r = subprocess.run(
            [sys.executable, str(checker), "--check-claim", tmp, "--root", str(cwd)],
            capture_output=True, text=True, timeout=30,
        )
    except Exception as e:  # noqa: BLE001 — hook must fail open, loudly
        print(f"[claim-gate] fleet_status failed to run ({e}); allowing", file=sys.stderr)
        return 0
    finally:
        Path(tmp).unlink(missing_ok=True)

    if r.returncode == 0:
        return 0
    if r.returncode == 1:
        print(
            "[claim-gate] BLOCKED: this write would set `status: verified` on "
            f"{rel} without a valid gate state.\n{r.stdout.strip()}\n"
            "No marker, no upgrade — run the auditor first (it writes the "
            "audit_passed marker on PASS), or keep the claim `under-review`.",
            file=sys.stderr,
        )
        return 2  # block
    print(f"[claim-gate] checker errored (exit {r.returncode}): {r.stderr.strip()}; allowing", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
