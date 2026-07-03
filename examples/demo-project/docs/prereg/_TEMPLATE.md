# Preregistration — <experiment name>

> Copy this template to `docs/prereg/<slug>.md` and fill it in BEFORE any
> implementation. The auditor design-checks this document; the engineer
> implements exactly this document. Results are filled into §6 as they come —
> the criteria in §4/§5 are never edited after the run starts.

## 1. Question

What will this experiment tell us that we don't know?

## 2. Design

- Data / model / procedure (operational definitions, not vibes).
- Anchor paper(s) for non-obvious design choices (ask the scout).

## 3. Predictions

What do we expect if the hypothesis is true? If it's false?

## 4. Success criteria (locked)

- Metric + threshold + seed/CI bar (inherit from CONSTITUTION unless stated).

## 5. Kill conditions (locked)

- Concrete result(s) that falsify the idea or void the run
  (e.g., "random-coupling control matches the real coupling → effect is
  capacity, not structure"; "held-out gap > X → memorization, numbers void").

## 6. Outcome (filled after the run — facts only)

- Result vs §4/§5, per seed.
- Verdict: PASS / FAIL / VOID — and if FAIL/VOID, **what this run bought**.

## Why prereg at all

Post-hoc framing is the smell reviewers detect first. A paper that reads as
"what we set out to test" beats a paper that reads as "what survived our
audits" — and the only way to get the former is to write this page first.
