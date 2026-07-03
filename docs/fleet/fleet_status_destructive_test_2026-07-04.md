# fleet_status.py — destructive test (2026-07-04)

`tools/fleet_status.py` turns ResearchFleet gate violations from *visible* into
*script-detected* (design philosophy: "enforcement lives in files, not
vigilance"). This doc records the destructive test that proves each check fires
on a real violation and clears after the fix.

## Method

The test harness (`C:/lpt/destructive_test.py`, not committed) copies
`examples/demo-project/` to a short temp path, asserts the baseline is green,
then for each check: snapshots the target file, manufactures one violation,
runs `fleet_status.py --json`, asserts exit code 1 with that specific check
flagged, restores the file, and asserts the project is green again.

Runner: `python fleet_status.py --root <proj> --json` (exit 0 = green,
1 = red, 2 = script/usage error).

## Results — 6/6 detected, 6/6 repaired to green

| check | what it guards | how it was broken | detected? | restored green? |
|---|---|---|---|---|
| C1 claim↔marker | a `verified` claim must point at a trace with an `audit_passed` marker | deleted the `audit_passed` marker under the verified claim's trace | ✅ | ✅ |
| C2 marker↔verdict | an `audit_passed` marker must sit beside a PASS verdict | kept the marker, flipped `verdict.md` header to `# Verdict: FAIL` | ✅ | ✅ |
| C3 prereg gate | a non-scratch run's manifest must point at a real prereg | set manifest `prereg` to `docs/prereg/does_not_exist.md` | ✅ | ✅ |
| C4 manifest | a run manifest must carry git_commit / seeds / env / config | deleted the `seeds` field from `manifest.json` | ✅ | ✅ |
| C5 evidence | every claim `evidence:` path must exist on disk | pointed one evidence path at `…/ghost.json` | ✅ | ✅ |
| C6 tree↔ledger | the growth log's last snapshot must agree with claims on the verified boundary | downgraded `readout_gap` to stage `data` while its claim stayed `verified` | ✅ | ✅ |

C7 (heartbeat) is a warning, not a red: aging `outcomes.jsonl` to 33 days back
produces a 🟡 yellow row with `exit_code: 0` (non-blocking), and `--no-heartbeat`
suppresses it. Verified separately.

Fail-loud check: a claim file with no YAML frontmatter is reported as a red
`parse errors` row (`missing YAML frontmatter (no opening '---')`) with exit 1 —
malformed contract files are surfaced, never silently skipped.

### Harness output (tail)

```
  [PASS] C1  verified claim, marker deleted  (detected=True, restored-green=True)
  [PASS] C2  marker present, verdict FAIL  (detected=True, restored-green=True)
  [PASS] C3  manifest prereg -> missing file  (detected=True, restored-green=True)
  [PASS] C4  manifest missing 'seeds'  (detected=True, restored-green=True)
  [PASS] C5  claim evidence -> missing file  (detected=True, restored-green=True)
  [PASS] C6  growth downgrades a verified claim  (detected=True, restored-green=True)

  6/6 checks: break detected AND repair returns green
```

## Dashboard output samples

Green baseline (`--ascii` shown for portability; the default uses 🟢🟡🔴 emoji):

```
Gates
  [OK]    C1 claim<->marker   ok
  [OK]    C2 marker<->verdict ok
  [OK]    C3 prereg gate      ok
  [OK]    C4 manifest         ok
  [OK]    C5 evidence         ok
  [OK]    C6 tree<->ledger    ok
  [OK]    C7 heartbeat        ok

Claims (1)
  [OK]    C3_readout_gap         verified     trace y
Traces (1)
  [OK]    .fleet/traces/experiment-audit/readout-gap/2026-06-28_run01 PASS
Runs (1)
  [OK]    readout_gap            manifest y
------------------------------------------------------------
Summary: [OK]   GREEN — all gates clear
```

Red (C1 marker deleted):

```
Gates
  [FAIL]  C1 claim<->marker   1 issue(s)
        - C3_readout_gap: trace has no audit_passed marker: .fleet/traces/experiment-audit/readout-gap/2026-06-28_run01/
  [OK]    C2 marker<->verdict ok
  ...
Summary: [FAIL] RED — 1 blocking issue(s), 0 warning(s)
```

## Changes made to demo-project

The demo previously carried a `growth.jsonl` that asserted `readout_gap` had
reached stage `paper` (i.e. verified-and-in-paper) and `visual_leg` stage
`audited`, but the repo had **zero** claim files, traces, or run packages
backing those stages — so a correct C6 legitimately went red on the shipped
demo. The demo was incomplete, not the checker. I minimally completed it into a
coherent green baseline that also gives every check something real to inspect:

- `claims/C3_readout_gap.md` — `status: verified`, `audit_trace` → the trace
  below, `evidence` → the run's `summary.json` + `per_seed.csv`.
- `.fleet/traces/experiment-audit/readout-gap/2026-06-28_run01/` — `prompt.md`,
  `log.md`, `verdict.md` (`# Verdict: PASS`), and the empty `audit_passed`
  marker (the key that legitimizes the claim's `verified` status).
- `experiments/results/readout_gap/` — `manifest.json` (full resolved config,
  git_commit, seeds `[0,1,2]`, env, `prereg` pointer, `smoke_passed`),
  `summary.json`, `per_seed.csv`, `metrics.jsonl`.
- `docs/prereg/readout_gap.md` — the preregistration the manifest points at.
- `docs/prereg/visual_leg.md` + `.fleet/traces/design-audit/visual-leg/2026-06-30_run01/`
  (`prompt.md`, `log.md`, `verdict.md` PASS) — backs `visual_leg`'s `audited`
  stage. This design-audit trace intentionally has **no** `audit_passed`
  marker: a design gate decides whether to implement, it does not verify a
  result, so it must not carry the marker that would unlock a `verified` claim.
- `claims/README.md` — registered the verified claim in the index and added the
  synthetic-proxy-labels row to the disclosure checklist.

## Note for future maintainers: Windows MAX_PATH

The demo lives under a very long non-ASCII base path. With `LongPathsEnabled=0`
(this machine) and a resolved path > 260 chars, `os.listdir`/`scandir` **raise**
and `Path.is_file()` can silently return `False` — which would turn a real
violation (or a missing marker) into a **false green**. `fleet_status.py`
defends against this by prefixing the resolved project root with the Windows
extended-length marker `\\?\` (`_longpath()`), so every filesystem op bypasses
the 260-char limit regardless of the registry flag; the prefix is stripped from
human/JSON output via `_display()`. Without this, the checker reported a phantom
"no audit_passed marker" C1 red on the green demo.
