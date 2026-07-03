# Outcome Ledger — one honest line per finished task

`.fleet/outcomes.jsonl` — append-only, one JSON object per completed agent
task. This is the raw material of the fleet's self-improvement loop: the
coach agent mines it for recurring friction and turns patterns into
evidence-based proposals. Thirty seconds of honesty per task buys a fleet
that actually gets better.

## Schema

```json
{"ts": "2026-07-03", "agent": "engineer", "task": "implement+run readout_gap_v2",
 "outcome": "success",
 "went_well": "smoke edge-case sampling caught a seq-len OOM before production",
 "went_wrong": "prereg didn't specify seed count; had to stop and ask mid-run"}
```

- `ts` — date (YYYY-MM-DD).
- `agent` — who did the work (`scout|engineer|auditor|writer|presenter|steward`
  — or `leader` for main-session gate decisions worth recording).
- `task` — one line, specific enough to find the artifacts again.
- `outcome` — `success | partial | fail`.
- `went_well` — ONE sentence: what made it work (which rule, which file,
  which habit earned its keep).
- `went_wrong` — ONE sentence: what fought you (ambiguous input, missing
  contract detail, rule that got in the way, tool friction). On a success
  this is the friction; on a fail this is the cause.

## Honesty rules

1. **Specific beats polite.** "went_well: task completed" is a ceremony
   entry — it feeds the improvement loop nothing and the coach is instructed
   to flag chronic ceremony as its own finding. Name the file, rule or habit.
2. **Never blank both fields.** A task with nothing learned is rare; if
   truly nothing, write `"-"` in one field, not both.
3. **Failures get the same one-line dignity** — the cause as observed, not
   as excused. On a fail, `went_well` records what was salvaged ("what this
   run bought" culture applies here too).
4. **Blame rules, not people.** "the prereg template lacks a seeds field"
   is actionable; "I was careless" is not.
5. One line per task, not per file — this ledger must stay cheap or it dies.

## Who writes

Every agent appends exactly one line before finishing (it's in each output
contract). The leader may also log gate decisions that felt wrong or
expensive — those are the highest-value entries the coach can get.

**Leader backstop**: if an agent's report arrives without a ledger line, the
leader appends one from the report's content. Capture must survive agent
forgetfulness — a starved ledger kills the improvement loop silently.
