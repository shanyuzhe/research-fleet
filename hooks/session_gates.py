#!/usr/bin/env python3
"""SessionStart hook: inject a one-line summary of the six gates.

Long sessions drift; CLAUDE.md persists but fades from attention. This puts
the gates back into context at every session start for the cost of one line.
stdout of a SessionStart hook is added to the session context.
"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

print(
    "[fleet] Six gates: 1 prereg-before-implementation (scratch lane exempt, "
    "scratch numbers never enter claims) · 2 design-audit before code · "
    "3 smoke before production · 4 claim upgrades need the audit_passed marker · "
    "5 writer reads only claims/ + paper/ (Methods via method cards) · "
    "6 paper body = verified claims only. Details: CLAUDE.md; state: "
    "docs/CURRENT_STATE.md; check: python tools/fleet_status.py"
)
