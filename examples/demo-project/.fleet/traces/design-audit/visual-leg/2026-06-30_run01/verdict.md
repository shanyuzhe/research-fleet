# Verdict: PASS

Subject: visual_leg — counterfactual visual-evidence experiment design
Scope: design-level
Date / run: 2026-06-30_run01

## Scope verdicts

| # | check | verdict | evidence (file:line or file:key=value) |
|---|---|---|---|
| 1 | question is answerable | PASS | docs/prereg/visual_leg.md: §1 counterfactual mask isolates visual grounding |
| 2 | kill condition is real | PASS | docs/prereg/visual_leg.md: §5 shuffled-mask control voids the effect |
| 3 | metric matches constitution | PASS | docs/prereg/visual_leg.md: §4 macro-over-aspect AUC (headline) |
| 4 | held-out plan present | PASS | docs/prereg/visual_leg.md: §2 cross-fit split declared |

## Blocking (must fix before the gated action)

_(none)_

## Non-blocking (recommended)

1. Pre-register the exact mask radius before production to avoid a degrees-of-
   freedom objection from reviewers.

## What this run bought

The design is sound to implement: the counterfactual mask has a real kill
control (shuffled-mask) and a locked headline metric, so production can be
queued. This is a design gate only — it does NOT verify any result; the
experiment-audit after data lands is still required before any claim.
