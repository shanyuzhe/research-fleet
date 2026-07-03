# src — vlm-judge-probing library

All reusable logic lives here, organized by pipeline stage (`data/`,
`models/`, `evaluation/`, …). Rules (full contract: repo-discipline):

- **Modules appear as stages emerge** — don't pre-create empty folders.
- **Scripts stay thin** (`experiments/scripts/` = args → one src call →
  land results); logic used twice gets refactored into a module here.
- **One-way imports**: scripts and scratch import src; src imports neither.
- Naming: `src/<stage>/<slug>.py`, snake_case, content-describing
  (`bootstrap_ci.py`, not `utils2.py`).
