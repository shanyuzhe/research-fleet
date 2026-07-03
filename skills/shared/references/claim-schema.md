# Claim Schema — claim-as-file contract

Every paper-bound result lives in exactly one file: `claims/<ID>_<slug>.md`.
Claims are the **only** interface between experiments and the paper. The writer
agent reads claims; it never reads raw findings. This isolation is deliberate
(see `docs/lessons.md`, Lesson 15).

## File format

```markdown
---
id: C3_readout_gap
title: Probe readout beats distilled decoding by +X pp (3/3 datasets)
status: under-review          # under-review | partially-verified | verified
status_reason: awaiting execution-level audit of run 2026-07-01
date: 2026-07-01
audit_trace: .fleet/traces/experiment-audit/readout-gap/2026-07-01_run01/
evidence:
  - experiments/results/readout_gap/summary.json
  - experiments/results/readout_gap/per_seed.csv
---

# Claim (one sentence, paper-ready)

<Exact statement with effect size, CI, seed count, and metric name.>

# Usage & boundaries

- How this may be phrased in the paper (and the strongest phrasing allowed).
- Red lines: what this claim does NOT support. Never delete this section.

# Provenance

- Preregistration: docs/prereg/<file>.md
- Run manifest: experiments/results/<run>/manifest.json
```

## Status gate (hard rule)

| status | meaning | requirement |
|---|---|---|
| `under-review` | data landed, no audit yet | evidence paths must exist |
| `partially-verified` | execution-level audit passed | `audit_trace` points to a verdict with `PASS` or `PARTIAL` |
| `verified` | design-level AND execution-level audit passed | `audit_trace` directory contains the `audit_passed` marker file |

- **Only `verified` claims may appear in the paper body.** `partially-verified`
  may appear in appendix with an explicit qualifier.
- Downgrades are allowed and normal. Upgrades without a new audit trace are
  forbidden.
- Negative results get claims too (status can be `verified`): a verified
  negative is a boundary statement, often a selling point.

## Index

`claims/README.md` maintains a one-line-per-claim table
(`id | title | status | trace`) plus a **disclosure checklist** — every
methodological caveat (proxy labels, synthetic ground truth, single-judge
scoring, ...) that the paper's Methods/Limitations section MUST contain.
The steward agent keeps this index in sync.
