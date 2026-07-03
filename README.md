<div align="center">

# ⛵ ResearchFleet

**Spawn your research crew in one command.**

A Claude Code plugin that scaffolds a disciplined ML research project and
staffs it with a seven-agent team — led by your main session as PI.

*a.k.a. **The PI Simulator** — your crew never sleeps, never sulks,
and never claims a result without an audit trail.*

[![CI](https://github.com/shanyuzhe/research-fleet/actions/workflows/ci.yml/badge.svg)](https://github.com/shanyuzhe/research-fleet/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757.svg)](https://claude.com/claude-code)
[![Version](https://img.shields.io/badge/version-0.2-green.svg)](ROADMAP.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**English** · [中文](README.zh-CN.md)

</div>

---

Every "AI scientist" demo automates the researcher. Independent evaluations
keep reaching the same verdict: the output isn't trustworthy without the
human supervision these systems claim to remove. ResearchFleet starts from
that verdict — **it automates the lab's discipline instead, and keeps you in
the PI seat.**

One command — `/research-init` — gives you three things:

| | |
|---|---|
| 📁 **A disciplined project skeleton** | constitution · preregistrations · claims · audit traces · handoff page — single-source-of-truth wired, gate invariants checkable by script |
| 🧑‍🔬 **A seven-agent research team** | scout · engineer · auditor · writer · presenter · steward · coach — each with hard rules and forbidden zones |
| 🧭 **A leader constitution** | your main Claude session becomes the PI: it routes work to the fleet, you just talk to it |

Every mechanism here traces to a documented research failure we personally
paid for — **[docs/lessons.md](docs/lessons.md)**: 15 war stories → 15 mechanisms.

## ⚡ Quickstart

```bash
# 1 · Install (pick one)
claude --plugin-dir /path/to/research-fleet      # local clone
#     …or from a plugin marketplace once published

# 2 · Initialize — three questions: project name, field, target venue
claude
> /research-init                    # add --minimal for solo/side projects

# 3 · Do research by talking to the leader in plain language
> "Has anyone probed VLM hidden states for judge quality?"   # → scout flies
> "Let's preregister the probing experiment"                 # → leader + you, together
> "Implement and run it"                                     # → auditor design-checks, engineer runs
> "Write the results section"                                # → writer (verified claims only)
> "Show me the tree"                                         # → 🌳 watch your project grow
```

No commands to memorize beyond `/research-init` — the generated
`CHEATSHEET.md` is one page, and the leader does the routing.

## 🧑‍🔬 The fleet

```mermaid
flowchart TD
    U([You]) <--> L[Leader — your main session<br/>strategy · prereg · gates]
    L --> S[scout 🔭<br/>literature · novelty · citation truth]
    L --> E[engineer 🔧<br/>implement · smoke · run · analyze]
    L --> A[auditor 🔍<br/>design & execution audits · forensics]
    L --> W[writer ✍️<br/>outline · LaTeX · figures]
    L --> P[presenter 📽️<br/>paper-study · progress · talk decks]
    L --> ST[steward 📋<br/>handoff · notes vault · growth log]
    L --> C[coach 🎯<br/>mines outcomes → fleet upgrades]
    S --> lit[(docs/lit)]
    E --> res[(experiments/results)]
    A --> tr[(.fleet/traces + markers)]
    W --> paper[(paper/)]
    P --> decks[(presentations/)]
    ST --> cs[(docs/CURRENT_STATE.md)]
    ol[(.fleet/outcomes.jsonl<br/>one honest line per task)] --> C
    C --> fi[(docs/fleet/ proposals)]
    cl[(claims/ — the only door<br/>between findings and paper)] --> W
    tr -- audit_passed unlocks --> cl
```

| agent | absorbs | the hard rule that earns its keep |
|---|---|---|
| **scout** 🔭 | lit search · novelty checks · reference verification | zero fabrication — every citation verified live, or marked `[UNVERIFIED]` |
| **engineer** 🔧 | implement · smoke · run · monitor · analyze · method cards | fail loud · 3 seeds · held-out always · **cannot change protocol** |
| **auditor** 🔍 | design/experiment/paper audits · forensics · optional cross-model review | design-audit *before* implementation; verdicts cite `file:key=value` |
| **writer** ✍️ | outline · LaTeX · figures · compile · snapshot drafts | context-isolated: sees only `claims/` + `paper/` (Methods via method cards); numbers copied, never remembered |
| **presenter** 📽️ | paper-study decks (reverse-learning) · progress decks · talks | figures are PDF screenshots, never redrawn; judgment slides left blank — **no ghostwriting** |
| **steward** 📋 | handoff page · growth log · Obsidian vault · naming lint | summarizes, never judges; no fabricated progress |
| **coach** 🎯 | self-improvement from the outcome ledger | evidence or silence; proposes, **never applies**; no invented metrics |

The leader stays in your main session — strategy needs you anyway, and
resident watcher fleets die of token cost (we tried).

## 🔁 The rhythm of one result

```
prereg → design-audit → smoke → production (3 seeds) → experiment-audit
      → claim (under-review → verified, unlocked by audit marker) → paper
```

Skipping a step doesn't make the result arrive faster; it makes it arrive
twice — the second time from a reviewer. (Exploration lives in the gate-free
`experiments/scratch/` lane; scratch numbers just can't enter claims.)

## 🛡️ Enforcement you can grep

Most discipline frameworks are prose the model eventually ignores. Here the
rules live in three progressively harder layers:

1. **Files** — a claim can't reach `verified` without an `audit_passed`
   marker on disk; an experiment can't start without a preregistration file.
2. **Script** — `python tools/fleet_status.py` renders a red/yellow/green
   dashboard of every gate invariant (claims↔markers, marker orphans, prereg
   presence, manifest completeness, evidence paths, tree-vs-ledger
   consistency). One command, exit codes for CI.
3. **Hooks (optional)** — [`hooks/`](hooks/README.md) moves the claim gate
   into Claude Code's tool-call layer: an edit that would set
   `status: verified` without a valid audit trace is **mechanically
   rejected**, not merely frowned upon. What hooks can't enforce is
   documented honestly in the same file.

Plus the signature mechanism — **two-context isolation**: your internal
ledger (`docs/findings/`) stays brutally honest; the writer is firewalled
from it and works only from audit-gated claims, the story contract, and
method cards. Honesty and narrative each get a context where they can be
total.

## 🌳 Watch your research grow

Three views over one append-only growth log (`.fleet/growth.jsonl`):

```bash
python tools/growth_tree.py            # docs/fleet/tree.html — animated SVG tree:
                                       #   timeline scrubber · click-a-leaf provenance
                                       #   dead branches kept as honest history
python tools/growth_tree.py --ascii    # the same tree, in any terminal / ssh
```

```
  2026-07-03
  │
  ├─🍎 readout_gap              [paper]    in section 4.1
  ├─✝  fusion_gate              [data]     killed: baseline confound
  └─🪴 visual_leg               [audited]  production queued
```

And for daily review, the steward maintains an **Obsidian-ready learning
vault** (`notes/`): confusion ledgers and audit verdicts harvested into
concept cards you answer yourself. You finish the project knowing more, not
less — blind spots are surfaced, never smoothed over.

## 📦 What's in the box

```
agents/                 seven agent definitions (plain Markdown, model-agnostic)
commands/               /research-init slash command (thin shell over the skill)
skills/
  research-init/        the scaffold skill + all project templates
                        (incl. fleet_status.py + growth_tree.py, copied into projects)
  shared/references/    versioned contracts: claims · traces · verdicts · method cards ·
                        run manifests · outcome ledger · growth log · presentations ·
                        repo discipline · Obsidian vault
hooks/                  optional harness-level gate enforcement (see hooks/README.md)
tools/                  repo CI checks (agent lint, template integrity, count consistency)
docs/
  design.md             architecture & rationale (what we kept from ARIS, what we inverted)
  lessons.md            ★ the 15 failures this framework is made of
  landscape.md          competitive failure-mode survey + differentiation
examples/demo-project/  a scaffolded project with a living growth tree — CI keeps it green
```

## ❓ FAQ

**How does this relate to [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)?**
Same battle scars, opposite posture: ARIS runs research *overnight, without
you*; ResearchFleet runs a disciplined crew *with you as PI*. If you want
autonomous throughput, use ARIS. If you want supervision made cheap and
mechanical, you're in the right repo. (Lineage details:
[docs/design.md](docs/design.md).)

**Can I use the contracts without the agents?**
Yes. Everything under `skills/shared/references/` is plain Markdown with no
agent dependency — the claim schema, trace format, and verdict format work
in any workflow (they predate this plugin). The agents just make following
them the path of least resistance.

**What does it cost in tokens?**
The design is deliberately frugal: one agent per task at clear boundaries,
no resident watchers (we tried; token cost killed them), tiered deck review,
and a leader that answers most questions with a file read. Expect roughly
one agent-conversation per delegated task, not a swarm. `--minimal` trims
ceremony further for solo projects.

## 🚧 Status — v0.2, honest per our own rules

The **disciplines** are distilled from a year of real, documented research
cycles (including one full postmortem); the **plugin packaging** is new and
still accumulating miles. By our own standard that makes the framework
`indicative`, not `verified` — the upgrade path is a full pilot cycle, and
your `.fleet/outcomes.jsonl` plus an issue is exactly the feedback the coach
was built to consume. Roadmap: [ROADMAP.md](ROADMAP.md).

## 🙏 Lineage & credits

ResearchFleet is a role-based reorganization of ideas we battle-tested with
[**ARIS**](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)
(Auto-Research-In-Sleep, AAAI'26) and its reviewer-side dual
[**Anti-Autoresearch**](https://github.com/wanshuiyin/Anti-Autoresearch) —
see [docs/design.md](docs/design.md) for what we kept, inverted, and why.

## License

[MIT](LICENSE)
