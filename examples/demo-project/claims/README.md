# Claims — vlm-judge-probing

> The only interface between experiments and the paper. Schema: see the
> ResearchFleet claim-schema contract. Status upgrades to `verified` require
> an `audit_passed` marker in the referenced trace. Index maintained by the
> steward.

## Index

| id | title | status | trace |
|---|---|---|---|
| C3_readout_gap | Probe read path beats distilled decoding by +0.151 AUC (3/3) | verified | .fleet/traces/experiment-audit/readout-gap/2026-06-28_run01/ |

## Disclosure checklist (must appear in the paper's Methods/Limitations)

Every methodological caveat gets a row when it enters the project. The writer
treats this table as mandatory paper content.

| # | disclosure | introduced by | paper section |
|---|---|---|---|
| 1 | Judge labels are a synthetic proxy (single large-model scoring), not human ground truth | C3_readout_gap | Methods / Limitations |
