# Preregistration — visual_leg

> Locked before implementation. Design-audited 2026-06-30 (PASS, design-level).
> Production queued; §6 is empty until data lands.

## 1. Question

Is the small VLM judge's decision actually grounded in the image, or is it
driven by the text alone? A counterfactual mask over the image region should
shift the judgement if and only if the decision is visually grounded.

## 2. Design

- Data / model: same held-out triples and frozen VLM as readout_gap.
- Procedure: measure the judge's shift under (a) a true region mask vs (b) a
  shuffled-region control of equal area. Cross-fit split declared for any
  fitted read-out.

## 3. Predictions

If grounded, the true mask shifts the judgement more than the shuffled control.
If not, the two shifts are indistinguishable.

## 4. Success criteria (locked)

- Headline metric: macro-over-aspect AUC (inherited from CONSTITUTION).
- Bar: true-mask effect exceeds shuffled-control effect with a 3-seed CI
  excluding zero.

## 5. Kill conditions (locked)

- Shuffled-mask control matches the true mask → the effect is not grounding-
  specific; run voided.

## 6. Outcome (filled after the run — facts only)

- _Pending: production queued as of 2026-07-03._
