# Audit prompt — readout_gap execution-level

Audit the readout_gap run for execution-level integrity before its claim is
upgraded to `verified`. Files given:

- experiments/results/readout_gap/manifest.json
- experiments/results/readout_gap/summary.json
- experiments/results/readout_gap/per_seed.csv
- docs/prereg/readout_gap.md (locked criteria in §4/§5)

Check: numbers trace to files; the 3-seed CI on the read−write delta excludes
zero on all 3 datasets; the random-coupling kill control was actually run and
did not reproduce the margin; held-out gap rules out memorization. Blame our
own implementation first if anything looks surprising.
