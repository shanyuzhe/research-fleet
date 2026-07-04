---
type: concept
status: answered
spawned_by: "[[2026-07-03]] — experiment-audit of readout_gap"
---
# held_out_evaluation

<!-- fleet:begin -->
## The question the fleet couldn't answer for you
Why is a small in-train vs held-out gap a *precondition* for believing
readout_gap, rather than a reporting detail?

Backlinks: [[readout_gap]], [[2026-07-03]]
<!-- fleet:end -->

## My answer (own words — this section is why the vault exists)

The probe has enough parameters to memorize the training split. If it were
memorizing, its accuracy would be a fact about *the split*, not about *the
representation* — and the read≫write claim would collapse into "lookup
table beats decoder", which is trivially true and worthless. The held-out
number is the only one measuring what I actually claim: that the judgment
is linearly present in states the probe never saw. Small gap ⇒ the probe
found structure, not samples. That's why the audit treats a big gap as a
kill, not a caveat.
