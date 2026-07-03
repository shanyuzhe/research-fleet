# Optional hooks — enforcement in the harness, not the prompt

v0.1 was honest about its biggest structural gap: `audit_passed` is an empty
file anyone can `touch`; markers make violations **visible, not impossible**
(see `docs/fleet/self_audit_2026-07-03.md`, FM3). These hooks close part of
that gap by moving two gates from prompt-discipline into Claude Code's hook
layer, where the model cannot talk itself past them.

Hooks are **opt-in** — ResearchFleet works fully without them. They are also
**fail-open**: if a hook script errors or `tools/fleet_status.py` is missing,
the tool call is allowed with a warning. A broken guard must never brick a
session.

## What ships

| hook | event | what it does |
|---|---|---|
| `claim_gate.py` (H1) | PreToolUse on Write/Edit | reconstructs the post-edit content of any `claims/*.md` write; if it would say `status: verified`, runs `fleet_status --check-claim` on the proposed content and **blocks** the call when the referenced trace lacks a valid `audit_passed` (reason shown to the model) |
| `stop_status.py` (H3) | Stop | runs `fleet_status --json` at turn end; on red gates prints a reminder. Non-blocking by default; add `--block` to the command to hard-block ending the turn while gates are red (pattern borrowed from ARIS's `verify_paper_audits` Stop hook — thanks upstream) |
| `session_gates.py` | SessionStart | injects a one-line summary of the six gates into context — the cheap fix for long-session leader drift (FM6) |

## Enabling

1. Initialize your project with `/research-init` (the hooks call the
   project's `tools/fleet_status.py`).
2. Copy the entries you want from `settings.example.json` into your
   project's `.claude/settings.json`, replacing `<FLEET_HOOKS>` with the
   absolute path to this directory.
3. Verify: try editing a claim to `status: verified` without an audit trace —
   the edit should be rejected with the reason.

## Honest boundary — what these hooks canNOT do (H2)

We wanted a third hook: *only the auditor may create `audit_passed`
markers.* We did not ship it, because the hook layer cannot reliably tell
**which agent** is making a tool call — a marker written by an over-helpful
main session looks identical to one written by a legitimate auditor run. A
guess-based guard would either block real audits or teach users that the
gate cries wolf.

So marker integrity is enforced the honest way instead:

- **after the fact, mechanically** — `fleet_status` C2 flags any
  `audit_passed` whose directory lacks a `verdict.md` with a PASS
  conclusion, and C1 flags any verified claim pointing at an invalid trace;
- **at the choke point** — H1 blocks the *consequence* of a forged marker
  path (the claim upgrade) unless the full trace shape is valid.

If a future Claude Code release exposes the spawning agent to hooks, H2
becomes a five-line script and we will ship it.
