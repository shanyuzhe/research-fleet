# Obsidian Notes — the researcher's learning vault

> contract-version: 0.2

`notes/` is an Obsidian-ready folder (open it as a vault, or add the project
to an existing vault). It exists for **the human's learning**: the project's
threads become a linked knowledge web, reviewed daily. The steward generates
and updates it from project state; the user annotates it. Structure is
rigid on purpose — tidy structure is what makes daily review frictionless.

## Vault layout (fixed — no other folders, no loose files)

```
notes/
├── 00_MOC.md            # Map of Content — the single hub, links everything
├── daily/               # one review note per working day
│   └── 2026-07-03.md
├── lines/               # one note per line of work (the 脉络 carriers)
│   └── readout_gap.md
├── concepts/            # knowledge cards — resolved confusions, methods, terms
│   └── held_out_evaluation.md
└── papers/              # literature notes, one per read paper
    └── vaswani2017_attention.md
```

Naming follows the repo naming table: snake_case slugs, ISO dates,
filenames match wikilink targets exactly.

## The auto/user split (the one rule that makes this work)

Every generated note has machine sections and human sections:

- Machine sections sit between `<!-- fleet:begin -->` / `<!-- fleet:end -->`
  markers. The steward rewrites ONLY inside these markers on update.
- Everything outside the markers belongs to the human and is **never
  touched**. Regeneration must be idempotent for user content.
- A note the user created entirely by hand (no markers) is never edited.

## Templates

### daily/YYYY-MM-DD.md — the review ritual (≤1 screen)

```markdown
---
type: daily
date: 2026-07-03
---
# 2026-07-03

<!-- fleet:begin -->
## What moved today
- [[readout_gap]] 🌳 → 🍎 — entered paper §4.1 (claim C3)

## Worth understanding (from confusion ledgers & audit verdicts)
- [ ] why the held-out gap voids a dataset's numbers → [[held_out_evaluation]]
<!-- fleet:end -->

## My take (why did today's calls make sense?)

## Tomorrow
```

"What moved" comes from the growth log diff + git log; "Worth understanding"
harvests presenter confusion ledgers, audit blocking items and gate
decisions — each linked to a concept card (created as a stub if missing).

### lines/<slug>.md — one thread, whole life

```markdown
---
type: line
slug: readout_gap
stage: paper          # kept in sync with the growth log
claim: C3
---
# readout_gap

<!-- fleet:begin -->
## Question
Probe readout vs distilled decoding — which carries the signal?

## Timeline
- 2026-06-05 🌰 idea
- 2026-06-12 🌱 preregistered — kill: random-coupling control
- 2026-06-28 🌳 verified (3/3 CI) → claim C3
- 2026-07-03 🍎 paper §4.1

## Evidence
- claim: `claims/C3_readout_gap.md` · run: `experiments/results/readout_gap_v2/`
<!-- fleet:end -->

## What I actually learned from this thread
```

Dead lines keep their note; the machine section gains an epitaph line
linking the killing trace. Threads are never deleted — a dead thread you
can re-read is tuition; one you deleted is just a bill.

### concepts/<slug>.md — knowledge cards

Stub generated on first reference (frontmatter `type: concept` + the
question that spawned it + backlinks); body is 100% human. The fleet asks
the questions; the human owns the answers — that's the internalization
contract.

### papers/<slug>.md — literature notes

Machine section: verified metadata (title/authors/venue/year, scout-checked)
+ why it entered the project + which decision it anchors. Human section:
actual reading notes.

## The 脉络 (the web, for free)

No manual linking discipline needed: daily notes link lines, lines link
claims/concepts/papers, concepts backlink everywhere they're referenced.
Obsidian's graph view then *is* the research map — clusters are threads,
orphan nodes are unstudied confusions, and the daily folder is a diary of
the tree growing.

## Living example

A filled vault (three threads, one answered card, one open card, one paper
note, populated MOC) ships in `examples/demo-project/notes/` — open it in
Obsidian and check the graph view to see the web this contract produces.

## Update triggers

Steward regenerates machine sections on each sync pass / end of session
(same trigger as CURRENT_STATE + growth log). The daily note for today is
created if absent. Nothing is generated retroactively for silent days —
no fabricated diary entries.
