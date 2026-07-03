# Contributing

Thanks for your interest! ResearchFleet is young and opinionated; the best
contributions right now are:

1. **War stories.** The framework is built from documented research failures.
   If a mechanism here would (or wouldn't) have caught a failure you lived
   through, open an issue titled `lesson: <one line>` — real failure modes
   drive the roadmap.
2. **Agent/prompt improvements.** Agents are plain Markdown under `agents/`.
   Keep the shape: role → missions → hard rules → forbidden → output
   contract. PRs that add rules must say which failure the rule prevents.
3. **Template refinements** under `skills/research-init/templates/` — same
   bar: every added line must earn its context cost.
4. **Adapters** (see ROADMAP v0.2): forensics, cross-model audit.

## Ground rules

- English for all agent/skill/template content; README may be bilingual.
- No mechanism without a lesson: if you can't name the failure it prevents,
  it's probably ceremony.
- Keep agents lean. Context is the scarcest resource; a 400-line agent is a
  bug even when every line is true.
- Test scaffold changes by running `/research-init` into a temp directory and
  reading the result as if you were a new user.

## License

MIT. By contributing you agree your contributions are MIT-licensed.
