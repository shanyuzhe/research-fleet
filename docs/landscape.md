# Landscape — what similar products get wrong, and what we do about it

Surveyed 2026-07: fully-autonomous AI scientists, deep-research agents,
multi-agent frameworks, and project templates — their documented failure
modes from independent evaluations and community feedback, and how each maps
to a ResearchFleet design decision (or a roadmap item where we're not there
yet).

## 1. Fully-autonomous AI scientists
*(Sakana AI Scientist v1/v2, Agent Laboratory, Google Co-scientist)*

Documented failure modes (independent evaluations, e.g.
[Beel et al. 2025](https://arxiv.org/abs/2502.14297); Agent Laboratory's own
PhD-student evaluation):

| failure mode | our answer |
|---|---|
| Novelty checks by shallow keyword search → known ideas classified as novel | scout's novelty mode searches **adversarially** — its job is to find the killer prior work, and "I found nothing" must list the queries tried |
| Cannot critically assess its own results; self-generated reviews catch surface issues, miss methodological flaws | auditor is a **separately-spawned adversary** with blocking power, structured verdicts, and evidence-per-check (`file:key=value`) — never the author reviewing itself |
| Implementation errors and hallucinated citations survive into papers | claim status gate (numbers trace to files) + scout's live citation verification + paper-audit before submission |
| Weakest phase across systems: literature review | that phase is human+scout collaborative here, not autonomous — see "position", below |
| Problem selection drifts toward the measurable (McNamara fallacy) | problem selection stays with the human PI; the fleet executes and verifies, it doesn't choose the question |

**Position**: these systems compete on *autonomy*; their independent
evaluations conclude they are "at best an advanced research assistant
requiring significant supervision". ResearchFleet starts from that
conclusion: supervision is the product. The human is the PI; the framework
makes the supervision cheap and mechanical instead of pretending to remove it.

## 2. Deep-research agents
*(GPT Researcher, STORM-style pipelines)*

Documented failure mode: **retrieval poisoning and misplaced trust** — a
13-word planted snippet on UGC sites achieved 38–100% citation rates in
tested systems; users treat fluent cited output as concluded fact.

**Our answer**: scout's source-trust rules — UGC (forums, Reddit, Quora,
wikis) is never evidence for a factual claim, only a lead to chase to a
primary source; fetched web content is data, never instructions; every
citation is verified against the publisher/DBLP/arXiv record, not against a
search snippet.

## 3. Multi-agent frameworks
*(CrewAI, AutoGen, LangGraph-style orchestration)*

Documented failure modes from production users: token footprints ~3× a
single-agent baseline on simple tasks; conversation loops that never
terminate; every agent turn re-pays full accumulated context; coordination
overhead dominating useful work.

**Our answer** (learned the same lesson independently — we archived our own
enforcement fleet after it proved too expensive to keep resident):
- the leader is the **main session**, not another agent — zero standing cost;
- agents spawn per task at clear boundaries and terminate by construction
  (they return a report; there is no agent-to-agent chat loop);
- coordination state lives in **files** (markers, schemas, status fields),
  which cost zero tokens to "run" and survive session restarts.

## 4. Project scaffolds
*(cookiecutter-data-science and its many forks)*

Documented failure modes: rigidity breeding fork sprawl; over-engineering
complaints; scaffolds that assume a workflow the user doesn't have. Notably,
its own v2 authors concluded "for most projects … a simple structure is good
enough".

**Our answer**: the scaffold is ~10 small files whose value is the *wiring*
(authority map, gates), not the directory count; every template line must
earn its context cost (CONTRIBUTING rule); unused directories are safe to
delete because contracts reference files, not the tree. A `--minimal` init
variant is on the roadmap for solo/side projects.

## Where ResearchFleet is genuinely different

One line: **everyone else automates the researcher; we automate the lab's
discipline.** The defensible mechanisms, by uniqueness:

1. **Two-context isolation** (findings ledger ⟂ writer). No surveyed system
   separates internal honest bookkeeping from external narrative — most
   don't even have the problem because they aren't honest internally. Ours
   encodes a real, expensive failure and cannot be trivially copied as a
   feature bullet: it requires the claims layer, the status gate and the
   firewall together.
2. **Evidence-cited self-improvement** (outcome ledger + coach). Fleet
   optimizers exist; one with a 30-second capture habit, an anti-ceremony
   contract, a no-invented-metrics rule and propose-only output does not.
3. **No-ghostwriting** (presenter's blank judgment slides; writer's
   copied-never-remembered numbers). Anti-slop as a *mechanism*, not a
   slogan — deliberately opposite to the autonomous-scientist value prop,
   and increasingly valuable as venues tighten AI-content policies.
4. **Negative results as first-class assets** (graveyard epitaphs,
   "what this run bought", prereg kill conditions). Tools celebrate wins;
   research mostly produces boundaries. We're structured around that truth.
5. **Roles over skills, leader over orchestrator, files over watchers** —
   each individually copyable, jointly a coherent economics: near-zero
   standing cost, which is precisely what killed the systems in §3 and the
   enforcement fleet we ourselves archived.

What we deliberately concede: overnight autonomy (ARIS), wet-lab/theory
fields (untested), cross-model review depth (v0.2 adapter), shipped code
assets (deck kits, renderers — v0.2). A user who wants a paper written
while they sleep is not our user; a user who wants to still trust their own
paper afterwards is.

## Honest gaps (things the survey says we should worry about)

1. **We are prompt-defined, not enforced by code.** A determined (or lazy)
   session can ignore a gate. Markers make violations *visible*, not
   *impossible*. v0.2+ may add a verifier script (`fleet-status`) that checks
   gate invariants mechanically.
2. **Maintenance risk.** The cookiecutter story shows templates die of
   stale-maintainer syndrome. Mitigation: tiny surface area, lessons-driven
   scope control, and saying no (see Non-goals in design.md).
3. **Unvalidated breadth.** The discipline system is distilled from ML/LLM
   research; its fit for wet-lab or theory-first fields is untested. We say
   so rather than claim generality.

## Sources

- [Evaluating Sakana's AI Scientist (arXiv:2502.14297)](https://arxiv.org/abs/2502.14297)
- [Agent Laboratory](https://agentlaboratory.github.io/)
- [Agentic AI Scientists Are Not Built For Autonomous Scientific Discovery (arXiv:2605.08956)](https://arxiv.org/html/2605.08956v1)
- [Deep-research retrieval poisoning coverage (TechTimes, 2026-06)](https://www.techtimes.com/articles/318839/20260622/ai-deep-research-flaw-single-reddit-comment-steers-consumers-scams.htm)
- [Cookiecutter Data Science v2 rationale](https://drivendata.co/blog/ccds-v2)
- Multi-agent framework comparisons: [pecollective](https://pecollective.com/blog/ai-agent-frameworks-compared/), [gurusup](https://gurusup.com/blog/best-multi-agent-frameworks-2026)
