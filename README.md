<div align="center">

# ⛵ ResearchFleet

**One command gives your research project an AI team that can't cut corners on you.**

[![CI](https://github.com/shanyuzhe/research-fleet/actions/workflows/ci.yml/badge.svg)](https://github.com/shanyuzhe/research-fleet/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757.svg)](https://claude.com/claude-code)
[![Version](https://img.shields.io/badge/version-0.2-green.svg)](ROADMAP.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**English** · [中文](README.zh-CN.md)

</div>

---

Everyone doing research with AI eventually hits the same wall: **the AI is
too fluent — so fluent you can't tell which sentences are true.**
ResearchFleet is a Claude Code plugin that doesn't try to do your research
for you. It puts your AI under lab discipline instead — everything it does
leaves evidence, and when it tries to wing it, the system says no.

## Sound familiar?

- 📉 **"Where did this number come from?"** — There's an 87.3 in your paper
  and you've spent half an hour failing to find which run, which config,
  produced it.
- 🎲 **Change the random seed, the conclusion changes** — and nobody wants
  to know that the week before the deadline.
- ✍️ **The AI is a little *too* helpful when writing** — it states an
  unverified number with total confidence, or invents a citation that
  doesn't exist.
- 🧠 **A week away and your mind is blank** — where were we? Which
  directions already died? Time to go archaeology-digging through chat logs.
- 😶 **The project is "done" and you feel *less* sure of it** — a pile of
  AI-generated results and prose you can't defend two questions deep at
  group meeting.

None of this is the AI's fault. It's what happens when **no process is
holding the AI accountable**. Real labs survive on a set of rules: register
the experiment before running it, nothing counts until someone checks it,
the paper only cites verified findings. ResearchFleet installs those rules
into your Claude Code project — and **enforces them automatically**.

## What changes once it's installed

| Before | After |
|---|---|
| Numbers in the paper with no provenance | Every number traces back to the exact run and config file that produced it |
| The AI says "verified" and you just have to trust it | Marking anything "verified" requires an audit record on disk first — without one the edit is **mechanically rejected**, no matter how persuasive the model is |
| The writing AI writes whatever it likes | The writer is locked in a room where it can only see checked conclusions — nothing to spin a story from |
| Project state lives in your head | Come back any time, read one handoff page: where we are, what's next, which paths are dead |
| Progress is invisible | A growing tree 🌳: every research thread from idea → experiment → verified → in-paper, dead branches kept as honest history |
| The AI forms your opinions for you | Conclusions, judgments, limitations stay blank for you to write — **no ghostwriting** |

In one sentence: **you're the boss (PI), seven AI staff do the work, and
every one of them has red lines it cannot cross.**

## ⚡ Getting started: one command, then plain language

```bash
# 1 · Install
claude --plugin-dir /path/to/research-fleet

# 2 · Initialize — three questions: project name, field, target venue
claude
> /research-init          # add --minimal for solo/side projects

# 3 · From here on, just talk
> "Has anyone done X?"                  # → the scout flies, every citation verified live
> "Let's register this experiment"      # → written with you: goal, success criteria, kill condition
> "Implement and run it"                # → auditor challenges the design first, engineer executes
> "Write the results section"           # → writer drafts, using audited conclusions only
> "Show me the tree"                    # → 🌳 watch the project grow
```

`/research-init` is the only command to remember. Routing is the leader
session's job — you make requests in whatever language you like.

📖 **Want the full flow?** [docs/GUIDE.md](docs/GUIDE.md) — when each agent
fires, the life of one research thread, the daily 10-minute ritual, and
what the knowledge vault grows into.

## 👥 Seven staff, one desk each

| who | does | what it must never do |
|---|---|---|
| 🔭 scout | literature, novelty checks, citation verification | fabricate a reference — anything unverifiable is marked `[UNVERIFIED]` |
| 🔧 engineer | code, run experiments, monitor training, statistics | change the protocol on its own; sell a single run as a conclusion |
| 🔍 auditor | challenge designs before code, numbers after runs, the paper before submission | be agreeable — every verdict must cite file-level evidence |
| ✍️ writer | outline, LaTeX, figures, compile | read internal working notes (story-poisoning); write numbers from memory |
| 📽️ presenter | paper-study decks, progress reports, talks | redraw figures (screenshots only); write your judgment slides |
| 📋 steward | handoff page, progress tree, learning notes | judge results; dress up "no progress" as progress |
| 🎯 coach | reviews the work ledger, proposes improvements | speak without evidence; change anything without your sign-off |

The leader isn't an AI staffer — it's the main session you're already
talking to, plus a constitution that teaches it how to delegate and when it
must come back to you.

---

<details>
<summary><b>🔬 Technical details (mechanisms, enforcement, repo layout, FAQ)</b></summary>

## The rhythm of one result

```
prereg → design-audit → smoke → production (3 seeds) → experiment-audit
      → claim (under-review → verified, unlocked by audit marker) → paper
```

Skipping a step doesn't make the result arrive faster; it makes it arrive
twice — the second time from a reviewer. Want to just try something?
`experiments/scratch/` is gate-free; scratch-born numbers simply can never
enter claims.

## Enforcement you can grep — three layers

1. **Files** — a claim can't reach `verified` without an `audit_passed`
   marker on disk; an experiment can't start without a preregistration
   file. Rules live in file formats, not good intentions.
2. **Script** — `python tools/fleet_status.py` renders every gate invariant
   (claims↔markers, marker orphans, prereg presence, manifest completeness,
   evidence paths, tree-vs-ledger consistency) as a red/yellow/green
   dashboard, exit codes wired for CI. Every check has a destructive test:
   manufacture the violation, watch it go red.
3. **Hooks (optional)** — [`hooks/`](hooks/README.md) moves the claim gate
   into Claude Code's tool-call layer: an edit that would set
   `status: verified` without a valid audit trace is **blocked**, reason
   shown to the model. What hooks can't enforce (e.g. "only the auditor
   writes markers") is documented honestly in the same file.

## The signature mechanism: two-context isolation

The internal ledger (`docs/findings/`) is brutally honest — negative
results, kill verdicts, doubts, all of it. The writer is firewalled from
that folder and works from exactly three inputs: audited claims (results),
method cards (implementation facts, copied field-by-field from run
manifests), and the story contract `NARRATIVE.md` (how to tell it). Internal
honesty gets to be total, and so does the narrative — neither poisons the
other.

## The growth tree

One append-only growth log, three views:

```bash
python tools/growth_tree.py            # docs/fleet/tree.html — animated SVG tree
python tools/growth_tree.py --ascii    # same tree in any terminal / ssh
```

```
  2026-07-03
  │
  ├─🍎 readout_gap    [paper]    in section 4.1
  ├─✝  fusion_gate    [data]     killed: baseline confound
  └─🪴 visual_leg     [audited]  production queued
```

Daily review runs through an Obsidian-ready vault (`notes/`): whatever
nobody understood gets harvested into concept cards you answer yourself —
you finish the project knowing more, not less.

## What's in the box

```
agents/                 seven agent definitions (plain Markdown, model-agnostic)
commands/               the /research-init entry point
skills/
  research-init/        scaffold + all project templates (incl. fleet_status.py, growth_tree.py)
  shared/references/    versioned contracts: claims · traces · verdicts · method cards ·
                        run manifests · outcome ledger · growth log · presentations · repo discipline
hooks/                  optional harness-level gate enforcement (see hooks/README.md)
tools/                  the repo's own CI checks
docs/
  lessons.md            ★ the 15 real failures this framework is made of
  design.md             architecture & rationale · landscape.md  failure-mode survey
examples/demo-project/  a scaffolded example project — CI keeps its gates green
```

## FAQ

**How does this relate to [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)?**
Same battle scars, opposite posture: ARIS does research *overnight, without
you*; ResearchFleet runs a disciplined crew *with you as PI*. Want
autonomous throughput, use ARIS; want supervision made cheap and mechanical,
use this. (Lineage: [docs/design.md](docs/design.md).)

**Can I use the contracts without the agents?**
Yes. Everything under `skills/shared/references/` is plain Markdown with no
agent dependency — drop it into any workflow. The agents just make following
the rules the path of least resistance.

**What does it cost in tokens?**
Frugal by design: one agent per task, no resident watchers (tried it; the
bill died first), tiered deck review, and a leader that answers most
questions with a file read. `--minimal` halves the ceremony again for solo
projects.

</details>

## 🚧 Status — v0.2, honest per our own rules

The **disciplines** are distilled from a year of real, documented research
cycles (including one full postmortem); the **plugin packaging** is new. By
our own standard that makes the framework `indicative`, not `verified` — the
upgrade path is a full pilot cycle. Try it: your `.fleet/outcomes.jsonl`
plus an issue is exactly the feedback the coach was built to consume.
Roadmap: [ROADMAP.md](ROADMAP.md).

## 🙏 Lineage & credits

ResearchFleet is a role-based reorganization of ideas battle-tested with
[**ARIS**](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)
(AAAI'26) and its reviewer-side dual
[**Anti-Autoresearch**](https://github.com/wanshuiyin/Anti-Autoresearch).
Every mechanism traces to a failure we personally paid for:
**[docs/lessons.md](docs/lessons.md)** — 15 war stories → 15 mechanisms.

## License

[MIT](LICENSE)
