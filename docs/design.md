# Design — why ResearchFleet looks the way it does

## Lineage

ResearchFleet stands on the shoulders of
[ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)
(Auto-Research-In-Sleep, AAAI'26) — a lightweight, Markdown-only skill suite
for autonomous ML research — and its reviewer-side dual
[Anti-Autoresearch](https://github.com/wanshuiyin/Anti-Autoresearch). We used
ARIS in anger for a year across two full research cycles. This project is our
answer to the question: *knowing what we know now, how should that capability
be packaged?*

## What we changed, and why

### 1. Roles, not skills

ARIS grew to 77 skills; in practice a working set of ~30 survived, and the
router needed its own cheatsheet. Capability fragmentation puts the
integration burden on the user ("which of five audit skills do I want?").

ResearchFleet inverts this: **five agents modeled on a research group's
roles** — scout, engineer, auditor, writer, steward. Each absorbs a family of
skills as internal modes. Users address roles ("check if this is novel"), not
a skill catalog. Adding capability means deepening a role, not growing a menu.

### 2. The leader is the main session, not another agent

Enforcement agent fleets die of token cost: an always-on watcher fleet burns
budget on idle vigilance, so it gets archived, so enforcement silently stops.
We know because it happened.

Here, the **main session is the leader (PI)**. Strategy, preregistration,
gate decisions and user conversation stay in the main window — they need the
human anyway. Agents are spawned at clear task boundaries, one per task, and
report back. Enforcement lives in *file formats* (markers, schemas, status
gates the leader can check with an `ls`), not in resident watchers. Cheap
enforcement is enforcement that actually happens.

### 3. Design-level auditing before execution-level

The single most expensive lesson (lessons.md §1): execution audits cannot
save a wrongly designed experiment. The audit pipeline therefore starts
*before* implementation — the auditor design-checks every preregistration,
with blocking power.

### 4. Two-context isolation between ledger and narrative

The signature mechanism (lessons.md §15). Internal findings stay radically
honest; the writer is firewalled to `claims/` + `NARRATIVE.md`. The claim
file — with status gate, usage boundaries, and disclosure checklist — is the
only door in the wall. This resolves the honesty-vs-narrative tension by
construction instead of by willpower.

### 5. Trust nothing without a trace

Inherited from ARIS and hardened: every audit writes
`.fleet/traces/<type>/<slug>/<date>_runNN/` with prompt, log, structured
verdict — and an `audit_passed` marker only on full PASS. The marker is the
only key that upgrades a claim to `verified`. "It obviously passed" is not a
key.

## Anatomy

```
main session = LEADER (PI)
 ├─ strategy, prereg, gates, user dialogue     (stays here)
 ├─ scout    → docs/lit/          (verified literature, novelty verdicts)
 ├─ engineer → experiments/       (prereg-faithful runs, run manifests)
 ├─ auditor  → .fleet/traces/     (design/experiment/paper audits, forensics)
 ├─ writer   → paper/             (sees ONLY claims/ + NARRATIVE.md)
 └─ steward  → docs/CURRENT_STATE.md, claims/README.md, docs/journal/
```

Data flow of one result:

```
prereg ──design-audit──▶ implement ──smoke──▶ production (3 seeds)
   ▲                                              │
   └── revise on FAIL                             ▼
                                        experiment-audit ──▶ trace + marker
                                                  │
                                                  ▼
                             claim (under-review → verified via marker)
                                                  │
                                                  ▼
                          writer (claims/ + NARRATIVE.md only) ──▶ paper
                                                  │
                                                  ▼
                              paper-audit / forensics ──▶ submit
```

## Optional: reviewer-side forensics

The auditor's fourth mode reads your own draft the way
[Anti-Autoresearch](https://github.com/wanshuiyin/Anti-Autoresearch) reads a
suspect paper — integrity forensics from the reviewer's chair (untraceable
numbers, caption/body drift, phantom citations, scope creep, missing
disclosures). A full adapter that invokes the real tool when installed is on
the roadmap (v0.2).

## Non-goals

- **Not an autonomous scientist.** ResearchFleet assumes a human PI making
  the calls; agents execute and verify. Overnight autonomy is what ARIS
  optimizes for — use ARIS if that's what you want.
- **Not a workflow engine.** No YAML pipelines, no queues. The leader routes
  by judgment; the gates are files.
- **Not model-locked.** Plain Markdown agents + skills; nothing here depends
  on private MCP servers (optional adapters may use them).
