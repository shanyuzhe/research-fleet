# .fleet/traces — audit evidence

Layout: `<audit-type>/<subject-slug>/<YYYY-MM-DD>_runNN/{prompt.md, log.md, verdict.md, audit_passed?}`

- Every audit writes a trace, PASS or FAIL. Traces are permanent.
- The empty `audit_passed` marker (written only on full PASS) is the only key
  that unlocks a claim upgrade to `verified`.
- Full contract: ResearchFleet trace-format + verdict-format references.
