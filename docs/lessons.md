# Lessons — the scar tissue this framework is made of

ResearchFleet is not a best-practices thought experiment. Every mechanism in
it exists because we paid for its absence during a year of LLM-agent-driven ML
research: one full paper cycle that ended borderline-reject (with a written
postmortem), and a second cycle that shipped. Below: the wound, then the
mechanism that scarred over it.

Fifteen lessons. The first eight killed or nearly killed a paper. The rest
cost weeks.

## Strategy-level (these kill papers)

### 1. The experiment was audited; the question wasn't
We ran 15+ rounds of rigorous execution-level auditing — numbers vs files,
byte-level. The paper still failed, because the *design* was wrong from day
one (an evaluation rubric copy-pasted from an adjacent subfield that couldn't
measure what we claimed to study). No amount of execution auditing can save a
wrongly designed experiment.
→ **Mechanism**: the auditor's `design-audit` mode fires BEFORE
implementation (Gate 2), asking "is this the right experiment at all?" — and a
FAIL blocks the engineer.

### 2. Post-hoc framing smells
We planned reactively: every null result triggered a reframe. The final paper
read as "what survived our audits", and reviewers can smell that from the
abstract.
→ **Mechanism**: preregistration gate — criteria and kill conditions written
before running (`docs/prereg/`), locked sections never edited after launch.

### 3. No story contract, double hedging cost
The paper straddled "method paper" and "analysis paper" for months; every
section paid hedging costs to two different reviewer rubrics.
→ **Mechanism**: `paper/NARRATIVE.md` forces the choice (method / analysis /
position — pick one) plus headline claim + evidence + fallbacks, before the
first production run.

### 4. Proxy ground truth discovered too late
All headline results were "agreement with an LLM judge", not "agreement with
humans" — and a late human pilot showed the judge was systematically
miscalibrated. Retrofitting human labels cannot rescue a headline; it can
only measure the damage.
→ **Mechanism**: the constitution's Labels section forces naming the ground
truth honestly on day one, and every proxy enters the disclosure checklist
that the writer MUST ship in Methods/Limitations.

### 5. Convenience choices, invisible until review
Aspects, judges and datasets had been chosen by pipeline convenience, not by
argument. Each looked like a small pragmatic call; jointly they predetermined
the paper's ceiling.
→ **Mechanism**: anchor-paper-per-decision — the scout finds a recent
peer-reviewed precedent for every non-obvious design choice; a decision with
no anchor is flagged provisional and design-audited.

## Evidence-level (these kill claims)

### 6. Single-seed effects evaporate
A "+4.1pp" single-seed result died on the 3-seed rerun. More than once.
→ **Mechanism**: 3 seeds, ≥2/3 CIs excluding zero, or the number is labeled
`indicative` and cannot enter a claim. Mechanical, no judgment calls.

### 7. In-sample numbers are fiction
In-sample evaluation inflated an effect by ~10pp; a distilled model's
"breakthrough" on one dataset was +9pp of memorization.
→ **Mechanism**: held-out always; the in-train vs held-out gap is a mandatory
report field, and a large gap voids the number by rule (not by debate).

### 8. Metric switching is self-deception
A "+3.6pp" on one dataset's preferred metric was +0.5pp on the project
metric — a threshold artifact sold to ourselves as an effect.
→ **Mechanism**: one headline metric, fixed in the constitution; companion
metrics reported but never substituted, per-dataset switching = cherry-picking
by definition.

### 9. A positive effect needs a kill experiment
Our strongest coupling result became credible only when a random-coupling
control *hurt* performance — proving the gain was learned structure, not
extra capacity.
→ **Mechanism**: prereg §5 requires kill conditions; the auditor checks that
a claimed effect has survived its control, not just reached its threshold.

### 10. Silent skips shrink N
`except: continue` quietly dropped samples; sample counts drifted between
pipeline stages; debugging took days because nothing failed.
→ **Mechanism**: fail-loud rules in the engineer agent — no bare excepts,
assert expected counts, treat >10% external-API error rates as fatal.

### 11. Smoke tests must include the edge cases
A production run died on an input 30× longer than anything in the 5-sample
dry run. Random small samples systematically miss the inputs that kill runs.
→ **Mechanism**: smoke gate checks three things (no errors / non-degenerate
effect / by-design behavior) on a sample that explicitly includes edge cases.

### 12. Panic verdicts are their own failure mode
An automated audit once concluded "retract the main finding" — the real cause
was a normalization mismatch in *our* cross-architecture comparison. Hours of
targeted re-auditing rescued a true result from a false alarm.
→ **Mechanism**: the "blame ourselves first" rule in verdict-format — a
verdict implying retraction must enumerate which implementation holes were
checked before panicking.

## Memory-level (these waste months)

### 13. Dead ideas resurrect
Without a written epitaph, a killed direction came back months later and
consumed another week before dying the same death.
→ **Mechanism**: the Graveyard in `CURRENT_STATE.md` — one-line epitaph plus
the trace that killed it, checked before any new experiment.

### 14. Numbers drift between documents
The same metric appeared as three slightly different values across docs — one
was a from-memory paste that survived into a draft.
→ **Mechanism**: single-source-of-truth authority map (pointers, not copies)
+ the writer's "numbers are copied, never remembered" rule + paper-audit
cross-checking abstract == body == claims.

### 15. Honest bookkeeping poisoned the paper's voice ★
The one that motivated this framework's signature design. Our internal
culture was radically honest: every negative result, kill verdict and doubt
recorded in full. That archive was an asset — until paper-writing time, when
it flooded the writing context. Drafts oscillated between two failure modes:
a sanitized version an external reviewer scored 4/10 for hiding diagnostics,
and an "honest" version whose headline drowned in caveats and internal
skepticism. Same evidence, both unpublishable.
→ **Mechanism**: **two-context isolation**. `docs/findings/` stays brutally
honest and is *firewalled from the writer*. The paper is written only from
`claims/` (verified results with explicit usage boundaries) and
`NARRATIVE.md` (story contract + phrasing red lines). Honesty and narrative
each get a context where they can be total.

---

*The point is not that agents are careless. It's that research pressure makes
everyone — human or model — want to skip the boring steps exactly when they
matter most. Rules that live in prose get skipped; rules that live in file
formats, markers and firewalls don't.*
