#!/usr/bin/env python3
"""CI lint: every agents/*.md has valid frontmatter (name, description, tools)
and every declared tool is a legal Claude Code tool name.

The presenter once shipped with `PowerShell` in its tools list — not a valid
agent tool name, silently ignored by the harness. This lint exists so that
class of drift turns CI red instead of shipping.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent

VALID_TOOLS = {
    "Read", "Write", "Edit", "MultiEdit", "NotebookEdit",
    "Bash", "BashOutput", "KillShell",
    "Grep", "Glob",
    "WebSearch", "WebFetch",
    "Task", "Agent", "Skill", "SlashCommand", "TodoWrite",
    "ExitPlanMode", "ListMcpResources", "ReadMcpResource",
}

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def main() -> int:
    failures = []
    agent_files = sorted((REPO / "agents").glob("*.md"))
    if not agent_files:
        print("[fail] no agent files found under agents/")
        return 1
    for f in agent_files:
        text = f.read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(text)
        if not m:
            failures.append(f"{f.name}: missing frontmatter block")
            continue
        fields = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fields[k.strip()] = v.strip()
        for required in ("name", "description", "tools"):
            if not fields.get(required):
                failures.append(f"{f.name}: frontmatter missing `{required}`")
        if fields.get("name") and fields["name"] != f.stem:
            failures.append(f"{f.name}: frontmatter name `{fields['name']}` != filename stem")
        for tool in [t.strip() for t in fields.get("tools", "").split(",") if t.strip()]:
            if tool == "*" or tool.startswith("mcp__"):
                continue
            if tool not in VALID_TOOLS:
                failures.append(f"{f.name}: `{tool}` is not a valid Claude Code tool name")

    if failures:
        print(f"[fail] agent lint: {len(failures)} problem(s)")
        for msg in failures:
            print(f"  - {msg}")
        return 1
    print(f"[ok] {len(agent_files)} agents pass frontmatter + tool-name lint")
    return 0


if __name__ == "__main__":
    sys.exit(main())
