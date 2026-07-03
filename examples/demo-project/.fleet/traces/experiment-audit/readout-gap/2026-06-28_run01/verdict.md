# Verdict: PASS

Subject: readout_gap — probe read path vs distilled write path, 3 datasets
Scope: execution-level
Date / run: 2026-06-28_run01

## Scope verdicts

| # | check | verdict | evidence (file:line or file:key=value) |
|---|---|---|---|
| 1 | numbers match files | PASS | experiments/results/readout_gap/summary.json: delta_read_minus_write.mean=0.151 |
| 2 | 3-seed CI excludes zero | PASS | summary.json: delta_read_minus_write.ci95=[0.132,0.170] |
| 3 | kill control checked | PASS | summary.json: random_coupling_control.delta_mean=0.004 (ci crosses 0) |
| 4 | held-out, no leakage | PASS | summary.json: held_out_gap in_train=0.804 held_out=0.792 (gap small) |
| 5 | per-seed present | PASS | experiments/results/readout_gap/per_seed.csv: 9 rows, 3 seeds x 3 datasets |

## Blocking (must fix before the gated action)

_(none)_

## Non-blocking (recommended)

1. Report per-dataset CIs in the paper appendix, not just the pooled delta.

## What this run bought

Confirmed the anchor finding survives its own kill control: the read path
beats the write path by +0.151 AUC (3/3 datasets, CI excludes zero), and the
random-coupling control does not reproduce the margin — so the effect is
readable structure, not raw capacity. Held-out gap is small, ruling out
memorization. This claim is cleared to enter the paper body.
