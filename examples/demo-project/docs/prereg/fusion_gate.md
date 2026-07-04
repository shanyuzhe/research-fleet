# Preregistration — fusion_gate

- **Date / status**: 2026-06-20 · KILLED 2026-06-28 (kept as record; see
  Graveyard in `docs/CURRENT_STATE.md`)
- **Question**: does a learned gate over read/write probability fusion beat
  the fixed fusion rule?
- **Operationalization**: gate = 2-layer MLP over per-aspect features;
  baseline = fixed rule with matched temperature calibration.
- **Success criterion**: gated fusion beats the calibrated rule baseline on
  held-out macro-AUC, CI excluding zero, on ≥2/3 seeds.
- **Kill condition (pre-committed)**: gain fails the shuffled-gate control —
  if a gate with shuffled inputs reproduces the gain, the "learning" is
  recalibration, not routing. → This is exactly what happened (1/3 seeds).
- **Seeds**: 0, 1, 2.
