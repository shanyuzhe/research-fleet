# Repo Discipline — module structure, commit flow, naming

> contract-version: 0.2

Three habits that keep a research repository readable a year later. The
leader owns the commit flow; the engineer owns code placement; the steward
lints naming.

## 1. Code structure — library fat, scripts thin

```
src/                    # THE library. All reusable logic lives here.
├── data/               # loading, preprocessing, splits
├── models/             # architectures, probes, heads
├── evaluation/         # metrics, aggregation, CI computation
└── ...                 # modules appear as pipeline stages emerge
experiments/scripts/    # thin entry points: parse args → call src → land results
experiments/scratch/    # gate-free; may import src; src NEVER imports scratch
```

- **Create modules as stages emerge** — never pre-create empty folders
  (rigid empty trees are how scaffolds die; see landscape.md §4).
- **Scripts stay ≤ ~50 lines**: argument parsing + one `src` call + landing.
  Logic appearing in a script twice gets refactored into `src/` immediately.
- **One-way dependency**: `scripts → src`, `scratch → src`. Nothing imports
  from scripts or scratch. Copy-paste forks of src code are bugs.
- Notebooks (if any) live in `experiments/scratch/`, are named like any
  other asset, and never hold the canonical version of anything.

## 2. Commit flow — review first, then commit, every task boundary

**Agents never run git.** The leader commits after each landed deliverable
(run landed, claim updated, deck delivered, doc written) — small, frequent,
one logical unit per commit.

Pre-commit review (every time, ~60 seconds):

1. `git status` — only the intended files staged; no secrets/keys, no
   binaries > 5 MB, no generated junk (`__pycache__`, checkpoints, temp
   scripts that should have been deleted).
2. Read the staged diff top to bottom — every hunk explainable in one
   sentence; anything surprising gets resolved before committing, not after.
3. New files pass the naming table (§3).
4. Message type matches content; artifacts referenced.

Message format:

```
<type>(<scope>): <what landed, one line, imperative>

<optional body: artifact pointers — run dir, trace path, claim ID>
```

Types: `exp` (runs/results) · `claim` · `paper` · `deck` · `lit` ·
`fleet` (ledger/coach/state docs) · `fix` · `docs` · `chore`.
Example: `exp(readout): land readout_gap_v2, 3 seeds — results/readout_gap_v2/`

Branch hygiene: work on `main` for a solo research repo is fine; anything
exploratory that would leave main broken gets a branch. Never rewrite
pushed history.

## 3. Naming — one pattern per asset type, no exceptions

Global rules: lowercase `snake_case` slugs, ASCII only, no spaces, no
parentheses, ISO dates (`YYYY-MM-DD`) prefixing anything time-ordered.
Versions are `_v2`, `_v3` — never `_final`, `_new`, `_latest`, `(1)`.
A name states **content**, never history ("readout_gap_analysis.md", not
"notes_tmp2.md"). One concept per file.

| asset | pattern | example |
|---|---|---|
| prereg | `docs/prereg/<slug>.md` | `docs/prereg/readout_gap.md` |
| finding | `docs/findings/YYYY-MM-DD_<slug>.md` | `docs/findings/2026-07-03_readout_gap_null.md` |
| claim | `claims/C<n>_<slug>.md` | `claims/C3_readout_gap.md` |
| run dir | `experiments/results/<slug>_v<n>/` | `experiments/results/readout_gap_v2/` |
| trace | `.fleet/traces/<type>/<slug>/YYYY-MM-DD_runNN/` | `.../experiment-audit/readout_gap/2026-07-03_run01/` |
| deck | `presentations/YYYY-MM-DD_<slug>/` | `presentations/2026-07-10_attention_study/` |
| journal | `docs/journal/YYYY-MM-DD.md` | `docs/journal/2026-07-03.md` |
| fleet report | `docs/fleet/<kind>_YYYY-MM-DD.md` | `docs/fleet/improvement_2026-07-03.md` |
| lit note | `docs/lit/<topic_slug>.md` | `docs/lit/vlm_judge_probing.md` |
| paper figure | `paper/src/figures/fig<n>_<slug>.<ext>` | `fig2_readout_gap.pdf` |
| python module | `src/<stage>/<slug>.py` | `src/evaluation/bootstrap_ci.py` |
| script | `experiments/scripts/<verb>_<slug>.py` | `experiments/scripts/run_readout_gap.py` |

Archive, don't delete: superseded assets move to a sibling `_archive/`
keeping their name, gaining nothing (the date prefix already orders them).

**Naming lint** (steward duty): on each sync pass, glob for violations —
spaces, uppercase slugs, `final|new|latest|tmp|copy` tokens, undated
time-ordered docs — and propose renames (`git mv`) as a checklist. The
steward proposes; the leader applies after review, in a dedicated
`chore(naming)` commit so renames never mix with content changes.
