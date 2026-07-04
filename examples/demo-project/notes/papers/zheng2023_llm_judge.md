---
type: paper
verified: scout 2026-06-06
---
# zheng2023_llm_judge

<!-- fleet:begin -->
## Metadata (scout-verified)
- Zheng, L., Chiang, W.-L., Sheng, Y., et al. *Judging LLM-as-a-Judge with
  MT-Bench and Chatbot Arena.* NeurIPS 2023 (Datasets and Benchmarks).

## Why it's in this project
Anchor paper for the judge-quality framing: establishes LLM-as-a-judge
agreement rates and the known biases (position, verbosity,
self-enhancement). Our delta: they evaluate the *decoded* judgment; we ask
whether the *representation* holds a better one ([[readout_gap]]).

## Which decisions it anchors
- prereg `readout_gap`: judge-agreement as the reference metric family
<!-- fleet:end -->

## My reading notes

Their bias taxonomy is the checklist our auditor reuses on judge outputs.
Worth re-reading §4 if visual_leg ever needs pairwise comparisons — the
position-bias mitigation matters more for pairs than for pointwise scores.
