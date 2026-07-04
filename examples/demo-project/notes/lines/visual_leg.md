---
type: line
slug: visual_leg
stage: audited
---
# visual_leg

<!-- fleet:begin -->
## Question
Does counterfactual visual evidence (full vs masked image) expose judgments
the text probe misses?

## Timeline
- 2026-06-20 🌰 idea
- 2026-06-28 🌱 preregistered — kill: Δh signal must beat text-only probe
  on grounding violations, else fold into limitations
- 2026-06-30 🪴 design-audit PASS — production queued (3 seeds)

## Evidence
- prereg: `docs/prereg/visual_leg.md`
- audit: `.fleet/traces/design-audit/visual-leg/2026-06-30_run01/`
<!-- fleet:end -->

## What I actually learned from this thread

_(in flight — nothing earned yet; the design-audit forced me to state what
"visual" adds beyond dataset choice, which sharpened the kill condition)_
