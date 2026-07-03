# Run Manifest — standard experiment run package

> contract-version: 0.2

Every experiment run produces a self-describing directory. If a number cannot
be traced back to one of these, it does not exist.

## Layout

```
experiments/results/<run-slug>/
├── manifest.json     # see below
├── metrics.jsonl     # one JSON object per eval point (append-only)
├── summary.json      # final aggregates, incl. per-seed values
└── (artifacts)       # checkpoints, plots, raw outputs
```

## manifest.json

```json
{
  "run_slug": "readout_gap_v2",
  "date": "2026-07-01",
  "git_commit": "<hash of the code that ran>",
  "config": { "...": "full resolved config, not a pointer" },
  "seeds": [0, 1, 2],
  "env": { "gpu": "...", "python": "...", "key_libs": {} },
  "prereg": "docs/prereg/readout_gap.md",
  "smoke_passed": true
}
```

## The scratch lane

`experiments/scratch/` is exempt from all of this — no manifest, no prereg,
no seed discipline. It exists so exploration has a legitimate home. The one
hard boundary: **scratch numbers never enter a claim, a finding doc, or the
paper.** If a scratch result looks real, it graduates by being re-run as a
preregistered experiment with a full run package.

## Non-negotiable engineering rules (baked into the engineer agent)

1. **Fail loud.** No bare `except: pass/continue`. Raise, or log
   `[fail] <reason>` and count skips; assert expected sample counts at the end.
   Silent skips shrink N and make debugging impossible.
2. **SMOKE before production.** Any run > 1 h gets a smoke run first, and the
   smoke must check three things: (a) zero errors/OOM, (b) the effect/metric is
   non-zero (not all-NaN, not all-equal), (c) by-design behavior holds
   (sample counts, monotonicity, NaN handling). Smoke sampling must include
   edge cases (longest sequence, largest image, rarest class) — a random-5
   sample will miss them.
3. **3 seeds minimum for any claimed effect**; a single seed is labeled
   `indicative` and can never enter a claim.
4. **Held-out evaluation is non-negotiable.** Anything trained must be scored
   on data it never saw (cross-fit / split-half). Always report the
   in-train vs held-out gap; a large gap voids the number (it's memorization).
5. **Eval reloads from checkpoint** in a fresh process — never evaluate the
   live training object.
6. **One metric authority.** The project constitution fixes the headline
   metric; per-dataset metric switching is cherry-picking.
