# Examples

`demo-project/` is what `/research-init` scaffolds, plus a few weeks of
simulated project life (one line of work walked through
prereg → audits → verified claim → paper, one killed, one in flight — so the
growth tree has something to show and `tools/fleet_status.py` has real gate
state to check; CI keeps it green). Initialized with:

- project name: `vlm-judge-probing`
- field: multimodal LLM evaluation
- venue: CVPR

Read it top-down as a new user would: `CLAUDE.md` (leader constitution) →
`CHEATSHEET.md` → `docs/CURRENT_STATE.md`. Empty working directories
(`docs/lit/`, `docs/journal/`, `paper/src/`, `experiments/*/`,
`.fleet/traces/<type>/`) are created at init time and omitted here where git
can't track them.
