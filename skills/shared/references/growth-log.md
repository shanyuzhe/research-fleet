# Growth Log — the tree's data spine

`.fleet/growth.jsonl` — append-only, one snapshot per steward sync (or
whenever any line of work changes stage). Cheap capture at write time buys
free reconstruction at render time: the animated tree, the Growth view
table and any future visualization are all replays of this one log.

## Schema

```json
{"ts": "2026-07-03", "lines": [
  {"slug": "readout_gap",  "stage": "verified", "note": "3/3 CI clear"},
  {"slug": "fusion_gate",  "stage": "data", "dead": true, "note": "killed by randomJ control"}
]}
```

- `ts` — snapshot date (YYYY-MM-DD).
- `lines[]` — every line of work known at that date (carry unchanged ones
  forward; each snapshot is complete, not a diff).
- `slug` — naming-table slug, stable across the project's life.
- `stage` — one of `idea | prereg | data | audited | verified | paper`
  (🌰🌱🌿🪴🌳🍎). Same truthfulness rule as the Growth view: a stage the
  files don't support gets downgraded, and downgrades are normal.
- `dead` — `true` once the line enters the graveyard; it keeps its last
  stage and stays in every later snapshot (dead branches are part of the
  tree's honest history, not deletions).
- `note` — optional one-liner shown in the tree's detail panel.

## Rendering

`python tools/growth_tree.py` (copied into the project at init) reads the
log and writes `docs/fleet/tree.html` — a self-contained page: SVG tree,
timeline scrubber, play button, click-a-leaf provenance panel. The steward
regenerates it after appending a snapshot.
