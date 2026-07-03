---
id: C3_readout_gap
title: Probe read path beats distilled decoding by +0.151 AUC (3/3 datasets)
status: verified
status_reason: execution-level audit 2026-06-28_run01 passed; audit_passed marker present
date: 2026-06-28
audit_trace: .fleet/traces/experiment-audit/readout-gap/2026-06-28_run01/
evidence:
  - experiments/results/readout_gap/summary.json
  - experiments/results/readout_gap/per_seed.csv
---

# Claim (one sentence, paper-ready)

On a small VLM judge, a linear probe over late-layer hidden states (read path)
outperforms the model's own distilled score decoding (write path) by +0.151
macro-over-aspect AUC (95% CI [0.132, 0.170]; 3/3 held-out datasets, 3 seeds),
while a random-coupling control does not reproduce the margin.

# Usage & boundaries

- Strongest phrasing allowed: "judge-quality information is present in the
  representation but under-read by the decoding interface" — supported by the
  read>>write gap surviving the random-coupling kill control.
- Red lines: does NOT claim the probe is a deployable judge, nor that the gap
  generalizes beyond the 3 evaluated datasets / this model size. Labels are a
  synthetic proxy (see disclosure checklist) — not human ground truth.

# Provenance

- Preregistration: docs/prereg/readout_gap.md
- Run manifest: experiments/results/readout_gap/manifest.json
- Audit trace: .fleet/traces/experiment-audit/readout-gap/2026-06-28_run01/
