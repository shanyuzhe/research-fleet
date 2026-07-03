# Preregistration — readout_gap

> Locked before implementation. The auditor design-checked this doc; the
> engineer implemented exactly it. §4/§5 criteria are frozen; §6 was filled
> after the run with facts only.

## 1. Question

Can a linear probe read judge-quality from a small VLM's hidden states more
accurately than the model's own distilled score decoding? If so, the
capability exists in the representation but is not exposed at the decoding
interface.

## 2. Design

- Data: 3 held-out evaluation datasets (image-question-judgement triples).
- Model: frozen small VLM; mean-pooled late-layer hidden states as probe input.
- Procedure: cross-fit linear probe (read path) vs distilled score decoding
  (write path); macro-over-aspect AUC is the headline metric (per CONSTITUTION).

## 3. Predictions

If the hypothesis holds, the probe beats decoding by a positive margin on all
3 datasets. If false, the margin is zero or negative, or collapses under the
random-coupling control.

## 4. Success criteria (locked)

- Headline metric: macro-over-aspect AUC.
- Bar: read path beats write path with 3/3 datasets clearing a 3-seed CI that
  excludes zero.

## 5. Kill conditions (locked)

- Random-coupling control matches the real coupling → the effect is capacity,
  not readable structure; finding voided.
- Held-out gap > in-train gap by a large margin → memorization; numbers void.

## 6. Outcome (filled after the run — facts only)

- Read path beat write path on 3/3 datasets; 3-seed CIs exclude zero.
- Random-coupling control did not reproduce the margin (kill condition not met).
- Verdict: PASS. This run bought the project's anchor finding (read >> write).
