# Roadmap

## v0.1 (current) — MVP

- [x] `/research-init` one-command project scaffold
- [x] Seven-agent fleet: scout / engineer / auditor / writer / presenter /
      steward / coach
- [x] Self-improvement loop: per-task outcome ledger (`.fleet/outcomes.jsonl`,
      one honest line per finished task) → coach mines it into evidence-cited
      proposals for CLAUDE.md / agents / templates (propose-only)
- [x] presenter: reverse-learning paper decks (confusion ledger), progress
      decks from claims, talk decks; zero-hallucination visuals +
      no-ghostwriting judgment slides (presentation-contract)
- [x] Contract layer: claim schema, trace format, verdict format, run manifest
- [x] Two-context isolation (findings ledger ⟂ writer)
- [x] Lessons doc (15 war stories → mechanisms)

## v0.2 — depth

- [ ] **Anti-Autoresearch adapter**: when the tool is installed, the
      auditor's forensics mode invokes the full 61-signal analysis and lands
      its verdict as a trace
- [ ] **Cross-model audit** (optional): route design/experiment audits to a
      second model family via user-configured MCP; disagreement escalates to
      the PI instead of majority-voting silently
- [ ] **rebuttal mode** for the writer (parse reviews, coverage-checked,
      grounded-in-claims responses)
- [ ] **ablation-planner mode** for the engineer (reviewer-perspective
      ablation matrix from a verified main result)
- [ ] Proof-checking mode for the auditor (theory papers)
- [ ] `/fleet-status` command: one-screen gate/claim/trace dashboard — and a
      mechanical gate-invariant checker (markers make violations visible;
      this makes them detectable by script)
- [ ] `--minimal` init variant for solo/side projects (anti-rigidity: the
      cookiecutter lesson, see docs/landscape.md §4)
- [ ] **MCP adapters & shipped assets**: detect-and-prefer Zotero / arXiv /
      Semantic Scholar MCP for the scout, WandB for the engineer's training
      checks; cloud-GPU deployment recipes (Vast/Modal/AutoDL) for the
      engineer; deck_kit.py + figure renderer shipped with the plugin;
      pluggable completion notifications (e.g. mobile push)

## v0.3 — distribution

- [ ] Publish to a plugin marketplace
- [ ] `examples/` gallery: an initialized project with one full
      prereg → run → audit → claim → paper cycle walked through
- [ ] Template variants per venue (rebuttal norms, page budgets)
- [ ] Scheduled coach runs (cron) + cross-project ledger aggregation, so
      improvements learned in one project propose upstream plugin changes

Suggestions welcome — see CONTRIBUTING.md.
