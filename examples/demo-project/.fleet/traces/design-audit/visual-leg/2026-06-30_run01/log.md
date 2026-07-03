# Audit log — visual_leg 2026-06-30_run01

- Read docs/prereg/visual_leg.md end to end.
- §1 question is a counterfactual: mask the image region, measure judge shift
  → isolates whether the judgement is visually grounded. Answerable.
- §5 kill: shuffled-mask control (mask a random region of equal area). If the
  shuffled control moves the judge as much as the real mask, the effect is not
  grounding-specific → voids the run. Real kill condition, good.
- §4 metric = macro-over-aspect AUC, matches CONSTITUTION headline.
- §2 declares a cross-fit held-out split.

Conclusion: PASS (design-level). No marker written — a design gate does not
verify results; the experiment-audit after data lands remains required.
