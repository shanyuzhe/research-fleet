---
name: research-init
description: One-command initialization of a disciplined ML research project — scaffolds code/paper/experiment structure, installs the fleet constitution (CLAUDE.md with agent routing), and prints a one-page cheatsheet. Use when the user says "research-init", "init research project", "new research project", or wants to set up the research fleet in a directory.
---

# /research-init — spawn your research crew

You are initializing a research project governed by the ResearchFleet
discipline system. The result: a directory skeleton + a project CLAUDE.md that
turns the main session into the fleet **leader** (PI), routing work to the
five agents (scout, engineer, auditor, writer, steward).

## Step 1 — Gather three answers

If not already provided as arguments, ask the user (one question round, three
fields):

1. **Project name** (short slug, e.g. `vlm-judge-probing`)
2. **Research field / topic** (one line, e.g. "multimodal LLM evaluation")
3. **Target venue** (e.g. CVPR / NeurIPS / ACL / arXiv-only / undecided)

Defaults if the user shrugs: directory name as project name, field "machine
learning", venue "undecided".

## Step 2 — Choose target directory

- If the current directory is empty or nearly empty → initialize in place.
- Otherwise create `./<project-name>/` and initialize there.
- Never overwrite existing files: if a target file exists, skip it and report
  the skip at the end.

## Step 3 — Scaffold

Create this structure (directories + files from `templates/`; replace
`{{PROJECT_NAME}}`, `{{FIELD}}`, `{{VENUE}}`, `{{DATE}}` — today's date — in
every template):

```
<project>/
├── CLAUDE.md                     ← templates/CLAUDE.md.template   (leader constitution)
├── CHEATSHEET.md                 ← templates/CHEATSHEET.md.template
├── docs/
│   ├── CURRENT_STATE.md          ← templates/CURRENT_STATE.md.template
│   ├── CONSTITUTION.md           ← templates/CONSTITUTION.md.template
│   ├── prereg/
│   │   └── _TEMPLATE.md          ← templates/PREREGISTRATION.md.template
│   ├── findings/
│   │   └── README.md             ← templates/findings-README.md.template
│   ├── lit/                      (empty, scout writes here)
│   └── journal/                  (empty, steward writes here)
├── claims/
│   └── README.md                 ← templates/claims-README.md.template
├── paper/
│   ├── NARRATIVE.md              ← templates/NARRATIVE.md.template
│   └── src/                      (empty, writer writes here)
├── presentations/
│   └── STYLE.md                  ← templates/STYLE.md.template  (deck theme + presenter identity)
├── experiments/
│   ├── README.md                 ← templates/experiments-README.md.template
│   ├── configs/
│   ├── scripts/
│   └── results/
└── .fleet/
    ├── outcomes.jsonl            (create empty — the outcome ledger, see fleet references)
    └── traces/
        └── README.md             ← templates/traces-README.md.template
```

Also create the (empty) `docs/fleet/` directory — the coach agent writes
improvement reports there.

Template files live in this skill's `templates/` directory
(`${CLAUDE_PLUGIN_ROOT}/skills/research-init/templates/`).

## Step 4 — Git

If the directory is not already inside a git repository, run `git init` and
make an initial commit (`chore: initialize research project with ResearchFleet`).
If it is already a repo, stage nothing — just report that.

## Step 5 — Handoff

Print a short welcome:

1. The generated tree (one screen).
2. The three commands that matter (from CHEATSHEET.md): talk to the leader in
   plain language; the leader routes to agents; check `docs/CURRENT_STATE.md`
   at session start.
3. Suggested first move: "Describe your research question — I'll dispatch the
   scout for a novelty check, then we write the first preregistration
   together."

Do not spawn any agent during init. Init is cheap and deterministic; the
fleet flies when there is real work.
