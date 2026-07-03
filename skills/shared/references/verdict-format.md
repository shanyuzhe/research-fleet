# Verdict Format — structured audit output

> contract-version: 0.2

Every audit verdict (`verdict.md` inside a trace directory) uses this exact
structure. Free-form verdicts are not verdicts.

```markdown
# Verdict: PASS | PARTIAL | FAIL

Subject: <what was audited, one line>
Scope: <design-level | execution-level | paper-level | forensics>
Date / run: <YYYY-MM-DD>_runNN
Reviewers: <single-model | cross-model (see cross_review.md)>

## Scope verdicts

| # | check | verdict | evidence (file:line or file:key=value) |
|---|---|---|---|
| 1 | <check name> | PASS/WARN/FAIL | results/x.json: auc_mean=0.712 |
| ... | | | |

## Blocking (must fix before the gated action)

1. <item — concrete, actionable, with file path>

## Non-blocking (recommended)

1. <item>

## What this run bought

<One paragraph: even on FAIL, state what was learned / ruled out. Traces are
not graveyards.>
```

## Rules

- **Every scope verdict cites evidence** down to file:line or file:key=value.
  "Looks correct" is not evidence.
- `PASS` overall requires all scope checks PASS (WARNs allowed only if
  explicitly waived in the verdict with a reason).
- On FAIL, the auditor must first suspect **our own implementation** before
  blaming baselines, datasets, or tooling ("blame yourself first" rule —
  a panic verdict that says "retract the finding" must itself list which
  implementation holes were checked before panicking).
- Numbers that look surprising are treated as bugs until traced: no
  rationalizing a weird number into a story.
- "I don't know" is an acceptable cell value; a fabricated one is not.
