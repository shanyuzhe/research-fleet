# H1 claim-gate hook — interception demo (2026-07-04)

Method: the hook was exercised at the protocol level — a PreToolUse JSON
payload piped to `hooks/claim_gate.py` stdin, exactly what Claude Code sends
(not yet re-run inside a live interactive session; that live pass is part of
the dogfood pilot).

## Case 1 — forged upgrade: BLOCKED

Payload: `Write` to `claims/C9_forged.md` in the demo project, content sets
`status: verified` with `audit_trace` pointing at a trace directory that was
never created.

```
exit code: 2  (Claude Code: block the tool call, stderr → model)

[claim-gate] BLOCKED: this write would set `status: verified` on
claims\C9_forged.md without a valid gate state.
🔴  C9_forged — 1 violation(s):
    - C9_forged: audit_trace dir missing:
      .fleet/traces/experiment-audit/never-ran/2026-07-04_run01/
No marker, no upgrade — run the auditor first (it writes the audit_passed
marker on PASS), or keep the claim `under-review`.
```

## Case 2 — legitimate upgrade: ALLOWED

Same payload, `audit_trace` pointing at the demo's real PASS trace
(`.fleet/traces/experiment-audit/readout-gap/2026-06-28_run01/`, which
contains `verdict.md` + `audit_passed`). Exit 0, no output — the write
proceeds.

## Case 3 — non-claim file: IGNORED

A `Write` outside `claims/` containing the literal string `status: verified`
passes through untouched (exit 0). The gate matches on path + proposed
frontmatter, not on strings anywhere.

## Notes

- The hook reconstructs the **post-edit** content (Write content / Edit
  old→new applied) and judges the proposed state, not the stale disk state —
  a claim can't be upgraded via a clever partial edit.
- Fail-open confirmed separately: with `tools/fleet_status.py` absent the
  hook warns and allows; a broken guard must not brick a session.
