---
type: line
slug: fusion_gate
stage: data
dead: true
---
# fusion_gate

<!-- fleet:begin -->
## Question
Does a learned gate over read/write fusion beat the fixed rule?

## Timeline
- 2026-06-12 🌰 idea
- 2026-06-20 🌱 preregistered — kill: must beat rule baseline on ≥2/3 seeds
- 2026-06-28 ✝ KILLED — baseline confound: the "gain" reproduced under a
  shuffled-gate control (1/3 seeds vs kill bar 2/3)

## Epitaph
Learned gate ≈ implicit temperature recalibration; the rule baseline with
matched calibration closes the gap. Do not resurrect without a new
mechanism hypothesis.

## Evidence
- prereg: `docs/prereg/fusion_gate.md` (kill condition, pre-committed)
<!-- fleet:end -->

## What I actually learned from this thread

Cheap lesson at 3 seeds instead of an expensive one at rebuttal time: any
"learned X beats rule X" claim needs the [[baseline_confound]] check *in
the prereg*, not after the reviewer asks.
