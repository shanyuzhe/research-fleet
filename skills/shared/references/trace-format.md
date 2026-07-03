# Trace Format — audit evidence on disk

> contract-version: 0.2

Every audit writes a trace, **regardless of verdict**. Traces are permanent;
they are never garbage-collected. A verdict that isn't on disk didn't happen.

## Directory layout

```
.fleet/traces/<audit-type>/<subject-slug>/<YYYY-MM-DD>_runNN/
├── prompt.md        # exactly what the auditor was asked, incl. file paths given
├── log.md           # working notes / raw output of the audit run
├── verdict.md       # structured verdict (see verdict-format.md)
├── cross_review.md  # OPTIONAL — second-model review exchange (brief, response,
│                    #   agreement table); present only on cross-model audits
└── audit_passed     # empty marker file — ONLY written on full PASS
```

`<audit-type>` is one of:

| type | fired by | question answered |
|---|---|---|
| `design-audit` | auditor, **before** implementation | "Is this the right experiment at all?" |
| `experiment-audit` | auditor, after data lands | "Do the numbers match the files, honestly?" |
| `paper-audit` | auditor, before submission | "Does every paper number trace to evidence?" |
| `forensics` | auditor (optional self-red-team) | "Would a reviewer's integrity forensics flag this?" |

## Marker semantics

- `audit_passed` is the **only key** that unlocks a claim status upgrade to
  `verified` (see claim-schema.md). No marker, no upgrade — no exceptions,
  including "it obviously passed".
- A `PARTIAL` or `FAIL` verdict still writes the full trace; it simply omits
  the marker. Blocking items in the verdict become the work queue.
- Never write the marker retroactively. If a run was re-audited, that is a new
  `_runNN` directory.

## Why this exists

Rules that rely on the model "remembering to audit" get skipped under
deadline pressure. A deterministic path + marker file turns discipline into a
mechanical gate the leader can check in one `ls`.
