# Method Card — the sanctioned Methods channel through the writer firewall

> contract-version: 0.2

The writer firewall (Lesson 15) blocks `docs/findings/` and `docs/prereg/`
because narrative poisoning is real. But a Methods section needs
architecture, hyperparameters and implementation details — technical facts
that live in preregistrations and run manifests, all behind the wall. Without
a sanctioned channel, the writer either produces an under-specified Methods
section or is tempted to climb the wall. Method cards are that channel:
**harmless technical facts pass through; narrative history does not.**

## One card per method component

Every method component that enters the paper gets exactly one card:
`paper/method_cards/<slug>.md`.

```markdown
---
component: <public term, aligned with paper/NARRATIVE.md — never an internal codename>
source_manifest: experiments/results/<run>/manifest.json
drafted_by: engineer
terminology_locked_by: leader
audit: <trace path of the light check, or "pending">
---

# <Public term>

## Architecture / definition
<What the component is, in paper-ready language. No history, no alternatives.>

## Hyperparameters (copied field-by-field from the manifest — never remembered)
| field | value | manifest key |
|---|---|---|
| learning rate | 1e-4 | config.lr |
| ... | | |

## Dependencies & training configuration
<Frameworks, model checkpoints, data preprocessing — facts a reader needs to
reproduce, copied from the manifest's env/config blocks.>

## Allowed figures / diagrams
<Which architecture figures or schematic diagrams this card licenses,
and where their sources live under paper/.>
```

## Who writes what (three hands, one card)

1. **engineer drafts** — values copied field-by-field from the run manifest
   (`copied-never-remembered` applies to hyperparameters exactly as it does
   to results). The engineer never invents public terminology.
2. **leader locks terminology** — the `component` name and all prose terms
   must match `paper/NARRATIVE.md`. Internal codenames never appear on a card.
3. **auditor light-checks** — field-by-field comparison against the manifest
   (this is a cheap, mechanical check, not a full audit mode). Mismatch = the
   card is corrected from the manifest, never the other way around.

## Rules

- Cards contain **current, locked method facts only** — no dead alternatives,
  no process narrative, no "we first tried". That history belongs in
  `docs/findings/` and, if the paper needs it, the appendix decision table
  (routed through a claim).
- A card without a `source_manifest` is invalid; a card whose values cannot
  be traced to that manifest is a firewall breach, not a shortcut.
- The writer reads `paper/method_cards/` freely (it lives under `paper/`,
  inside the firewall). If a Methods section needs a component with no card,
  the writer STOPS and asks the PI to route one — same protocol as a missing
  claim.
- Results numbers never appear on method cards — results flow through
  `claims/` only. Cards carry the *how*, claims carry the *what*.
