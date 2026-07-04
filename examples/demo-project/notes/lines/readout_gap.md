---
type: line
slug: readout_gap
stage: paper
claim: C3
---
# readout_gap

<!-- fleet:begin -->
## Question
Probe readout vs distilled decoding — which carries the judge signal?

## Timeline
- 2026-06-05 🌰 idea
- 2026-06-12 🌱 preregistered — kill: random-coupling control
- 2026-06-20 🌿 3 seeds landed
- 2026-06-28 🌳 verified (3/3 CI excludes zero) → claim C3
- 2026-07-03 🍎 paper §4.1

## Evidence
- claim: `claims/C3_readout_gap.md`
- run: `experiments/results/readout_gap/` · prereg: `docs/prereg/readout_gap.md`
- audit: `.fleet/traces/experiment-audit/readout-gap/2026-06-28_run01/`

## Linked knowledge
- [[held_out_evaluation]] — the gate this thread almost failed
- [[zheng2023_llm_judge]] — anchor paper for the judge-quality framing
<!-- fleet:end -->

## What I actually learned from this thread

The result I'd have bet on was the *opposite* — I assumed decoding sees
everything the probe sees. The gap means the decode head is the bottleneck,
not the representation. Wrote my own summary in [[held_out_evaluation]] of
why the held-out check made this believable.
