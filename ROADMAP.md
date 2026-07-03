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

## v0.2 — depth (in progress)

Landed 2026-07-04:

- [x] **`fleet_status.py` gate-invariant checker** — one-screen
      gate/claim/trace dashboard + `--json` + `--check-claim`; checks C1-C7
      (claims<->markers, marker orphans, prereg presence, manifest
      completeness, evidence paths, tree-vs-ledger consistency, ledger
      heartbeat). Markers made violations visible; this makes them
      detectable by script. Destructive test record: `docs/fleet/`
- [x] **Optional hooks** (`hooks/`) — H1 blocks illegal claim upgrades at
      the tool-call layer; Stop-hook red-gate reminder; SessionStart gate
      summary against leader drift. Honest H2 boundary documented in
      `hooks/README.md`
- [x] **Method-card contract** — the sanctioned Methods channel through the
      writer firewall (engineer drafts from manifests, leader locks
      terminology, auditor spot-checks)
- [x] **Cross-model audit** (optional): second-model review for
      design/experiment audits via user-configured MCP; verdict header
      declares single-model vs cross-model; disagreement escalates to the
      PI instead of majority-voting silently
- [x] `--minimal` init variant for solo/side projects (anti-rigidity: the
      cookiecutter lesson, see docs/landscape.md §4) — cuts ceremony, keeps
      all six gates
- [x] Contracts pinned into projects at init (`.fleet/contracts/`,
      versioned) — no runtime plugin-root dependency
- [x] CI: growth-tree render, fleet-status green on demo, agent frontmatter
      lint, template placeholder integrity, agent-count-vs-docs consistency

Queued:

- [ ] **Anti-Autoresearch adapter**: when the tool is installed, the
      auditor's forensics mode invokes the full 61-signal analysis and lands
      its verdict as a trace
- [ ] **rebuttal mode** for the writer (parse reviews, coverage-checked,
      grounded-in-claims responses)
- [ ] **ablation-planner mode** for the engineer (reviewer-perspective
      ablation matrix from a verified main result)
- [ ] Proof-checking mode for the auditor (theory papers)
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
