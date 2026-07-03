# Audit log — readout_gap 2026-06-28_run01

- Loaded summary.json; recomputed pooled delta from per_seed.csv means:
  read mean ≈ 0.792, write mean ≈ 0.641, delta ≈ 0.151 — matches summary.json.
- per_seed.csv: 9 rows = 3 seeds × 3 datasets; every seed's delta > 0.14 on
  every dataset → 3/3 datasets clear, CI comfortably excludes 0.
- Kill control: random_coupling_control.delta_mean=0.004 with ci95 crossing 0
  → control does not reproduce the effect. Kill condition NOT met (good).
- Held-out gap: in_train 0.804 vs held_out 0.792 (Δ 0.012) → no memorization.
- manifest.json complete (git_commit, seeds [0,1,2], env, config, prereg ptr,
  smoke_passed=true) and prereg docs/prereg/readout_gap.md exists.

Conclusion: PASS. Marker written.
