# Self-audit — design-level failure modes of ResearchFleet v0.1

> Coach-format report, run against our own product before first deployment.
> Propose-only: nothing below is applied. Evidence here is reasoning +
> analogous documented failures (no ledger data exists yet — zero real miles).

# Verdict: PARTIAL

Subject: ResearchFleet v0.1 (4 commits, unpiloted)
Scope: design-level
Date / run: 2026-07-03_run01

## Failure modes, ranked

### FM1 — Gate-bypass culture from day one (highest risk) ★
A brand-new user's first instinct is to tinker: "just run something quick".
Our gates say no experiment without a preregistration — so their very first
contact with the framework is friction, and the natural move is to bypass.
Every bypass teaches the session that rules are optional (the exact dynamic
that killed rule-layers before). **The framework currently has no legitimate
place to play.**
→ **Proposal P0-1: a scratch lane.** `experiments/scratch/` — explicitly
gate-free exploration, with one hard boundary: nothing in scratch can ever
be cited by a claim (numbers born in scratch must be re-run under a prereg).
Mirrors how real labs work: tinker freely, preregister before it counts.
Targets: CLAUDE.md.template (gates section), run-manifest contract.

### FM2 — Outcome ledger decay
The ledger line is each agent's *last* duty — the step most likely dropped
when context runs low. If capture decays, the coach starves and the
self-improvement loop dies quietly (the exact failure we designed against,
one level up).
→ **Proposal P0-2: leader backstop.** One line in the leader constitution:
when an agent's report arrives without a ledger entry, the leader appends
one from the report's content. Capture then survives agent forgetfulness.

### FM3 — Prompt-level enforcement is honor-system
`audit_passed` is an empty file anyone can `touch`; the writer's firewall is
a prohibition, not a wall — a "helpful" writer with a missing claim *will*
be tempted to peek at findings/. Markers make violations visible, not
impossible (acknowledged in landscape.md, but worth naming as the #1
structural gap vs. a code-enforced system).
→ **Proposal P1-1: hook-hardened gates (v0.2).** Claude Code hooks can
mechanically reject: claim edits that set `status: verified` when the
referenced trace lacks `audit_passed`; marker files created outside an
auditor run. Ship as optional `hooks/` the user can enable. This would be a
real differentiator: enforcement in the harness, not the prompt.
→ **Proposal P1-2: `fleet-status` script (already on roadmap, raise
priority)** — checks gate invariants (claims↔markers↔traces, prereg
presence, manifest completeness) in one command.

### FM4 — `${CLAUDE_PLUGIN_ROOT}` runtime dependency
Agents reference contracts via the plugin root variable. If it fails to
resolve in some execution context (subagent, future harness change), agents
improvise from memory — silent contract drift.
→ **Proposal P1-3: copy contracts into the project at init**
(`.fleet/contracts/`). Project-pinned versions, no runtime variable
dependency, upgrades become explicit diffs. Trade-off (accepted): projects
can lag the plugin.

### FM5 — Presenter self-review token cost
The presentation contract says render **every** slide to PNG and look at
them. A 22-slide deck × vision tokens per image, per revision round, is the
kind of cost that gets the whole review step skipped under pressure —
losing the golden-standard comparison entirely.
→ **Proposal P2-1: tiered review.** Full visual pass on the first deck (it
becomes the reference) and on final delivery; intermediate rounds check the
5 key slides (cover, TOC, divider, one content, one judgment slide).

### FM6 — Cold-context leader drift
Long sessions compact; the routing table and gates fade from attention even
though CLAUDE.md persists. The leader slowly reverts to a generic assistant.
→ Mitigation already present (CLAUDE.md is deliberately one page, pointers
only). **Proposal P2-2**: CURRENT_STATE.md template gains a first line the
steward maintains: "Leader: re-read CLAUDE.md if you can't name the 6 gates."
Cheap, self-referential, probably worth it.

### FM7 — Unproven-by-construction claims in our own README
We assert "battle-tested" mechanisms. The *lessons* are battle-tested; the
*product* has zero miles (our own indicative-vs-verified distinction).
→ **Proposal P2-3**: soften README wording to "distilled from a year of
documented research failures" (accurate) wherever it could read as "this
plugin was battle-tested" (not yet true). Credibility is the product; don't
overclaim it.

## Keep doing (design choices the analysis validates)

- Leader-in-main-session: every competitor datapoint (CrewAI 3× tokens,
  AutoGen loops, our own archived fleet) confirms it.
- Two-context isolation: no analog found anywhere in the survey; the
  mechanism directly encodes a real, expensive failure.
- Propose-only coach with anti-fabrication rules: the two documented deaths
  of self-improvement loops (invented metrics, capture ceremony) are both
  explicitly ruled against.

## Applied (user-approved 2026-07-03, same day)

- **P0-1 scratch lane** — CLAUDE.md.template gate 1 exception,
  run-manifest contract, experiments README template, engineer agent,
  init scaffold tree.
- **P0-2 leader backstop** — CLAUDE.md.template discipline list +
  outcome-ledger contract.
- **P2-3 (FM7) wording** — "Status" section added to both READMEs:
  disciplines are battle-derived, the plugin itself is `indicative`.

P1-1 (hook-hardened gates), P1-2 (fleet-status), P1-3 (contracts copied at
init), P2-1 (tiered deck review), P2-2 (leader drift ping) remain proposed
— v0.2 queue.

## What this audit bought

A prioritized pre-pilot worklist (P0-1, P0-2 before first real project;
P1-1..3 for v0.2), and one honest wording fix that protects the project's
core asset — credibility.
