#!/usr/bin/env python3
"""Render the project's growth log as an animated research tree.

Reads .fleet/growth.jsonl (see the growth-log contract), writes
docs/fleet/tree.html — a single self-contained page with an SVG tree,
a timeline scrubber, a play button and a click-a-leaf detail panel.

Usage:
  python tools/growth_tree.py [project_root]            # write docs/fleet/tree.html
  python tools/growth_tree.py [project_root] --ascii    # print current tree in terminal
  python tools/growth_tree.py [project_root] --ascii --replay   # animate history in terminal
"""
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

STAGES = ["idea", "prereg", "data", "audited", "verified", "paper"]
EMOJI = {"idea": "🌰", "prereg": "🌱", "data": "🌿",
         "audited": "🪴", "verified": "🌳", "paper": "🍎"}


def ascii_tree(snaps, replay):
    frames = snaps if replay else [snaps[-1]]
    for fi, s in enumerate(frames):
        lines = s["lines"]
        done = sum(1 for l in lines if l["stage"] in ("verified", "paper"))
        dead = sum(1 for l in lines if l.get("dead"))
        print(f"\n  {s['ts']}  ({fi + 1}/{len(snaps)})" if replay else f"\n  {s['ts']}")
        print("  │")
        for i, l in enumerate(lines):
            conn = "└─" if i == len(lines) - 1 else "├─"
            mark = "✝ " if l.get("dead") else EMOJI[l["stage"]]
            note = f"  {l['note']}" if l.get("note") else ""
            print(f"  {conn}{mark} {l['slug']:<24} [{l['stage']}]{note}")
        print(f"\n  verified+: {done}/{len(lines)} · graveyard: {dead}")
        if replay and fi < len(frames) - 1 and sys.stdout.isatty():
            time.sleep(0.5)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    root = Path(args[0]) if args else Path(".")
    src = root / ".fleet" / "growth.jsonl"
    if not src.exists():
        raise SystemExit(f"[fail] growth log not found: {src}")

    snaps = []
    for i, raw in enumerate(src.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            snaps.append(json.loads(raw))
        except json.JSONDecodeError as e:
            raise SystemExit(f"[fail] {src}:{i} bad JSON: {e}")
    if not snaps:
        raise SystemExit("[fail] growth log is empty — no snapshot logged yet")

    snaps.sort(key=lambda s: s.get("ts", ""))
    for s in snaps:
        if "ts" not in s or "lines" not in s:
            raise SystemExit(f"[fail] snapshot missing ts/lines: {s}")
        for ln in s["lines"]:
            if ln.get("stage") not in STAGES:
                raise SystemExit(
                    f"[fail] snapshot {s['ts']}: unknown stage {ln.get('stage')!r} "
                    f"(allowed: {STAGES})")

    if "--ascii" in flags:
        ascii_tree(snaps, replay="--replay" in flags)
        return

    out = root / "docs" / "fleet" / "tree.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(PAGE.replace("__DATA__", json.dumps(snaps, ensure_ascii=False)),
                   encoding="utf-8")
    n_lines = len({ln["slug"] for s in snaps for ln in s["lines"]})
    print(f"[ok] wrote {out} — {len(snaps)} snapshots, {n_lines} lines of work")


PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research tree</title>
<style>
  body { font: 14px/1.5 Georgia, "Times New Roman", serif; color: #2b2b2b;
         background: #faf8f2; margin: 0; padding: 24px; }
  h1 { font-size: 20px; margin: 0 0 2px; }
  .sub { color: #857f6f; font-size: 12px; margin-bottom: 14px; }
  .wrap { display: flex; gap: 18px; flex-wrap: wrap; }
  svg { background: linear-gradient(#f3efe4, #faf8f2 70%); border: 1px solid #e2dcc9;
        border-radius: 8px; max-width: 100%; height: auto; }
  .panel { flex: 1; min-width: 220px; max-width: 320px; }
  .card { border: 1px solid #e2dcc9; border-radius: 8px; padding: 12px 14px;
          background: #fffdf7; margin-bottom: 12px; }
  .card h2 { font-size: 14px; margin: 0 0 6px; }
  .muted { color: #857f6f; }
  .controls { display: flex; align-items: center; gap: 10px; margin: 14px 0; }
  input[type=range] { flex: 1; }
  button { font: inherit; padding: 4px 14px; border: 1px solid #b9b19a;
           border-radius: 6px; background: #fffdf7; cursor: pointer; }
  .leaf { cursor: pointer; }
  .legend span { margin-right: 10px; white-space: nowrap; }
  #date { font-variant-numeric: tabular-nums; font-weight: bold; min-width: 96px; }
</style>
</head>
<body>
<h1>🌳 Research tree</h1>
<div class="sub">Every branch is a line of work; its leaf color is the lifecycle stage.
Dead branches stay on the tree — they are part of its history.</div>
<div class="wrap">
  <div style="flex:2;min-width:460px">
    <svg id="tree" viewBox="0 0 900 640" xmlns="http://www.w3.org/2000/svg"></svg>
    <div class="controls">
      <button id="play">▶ Play</button>
      <input id="scrub" type="range" min="0" value="0">
      <span id="date"></span>
    </div>
    <div class="card legend" id="legend"></div>
  </div>
  <div class="panel">
    <div class="card"><h2 id="d-title">Click a leaf</h2>
      <div id="d-body" class="muted">Details of the selected line of work appear here.</div>
    </div>
    <div class="card"><h2>Snapshot</h2><div id="d-snap" class="muted"></div></div>
  </div>
</div>
<script>
const SNAPS = __DATA__;
const STAGES = ["idea","prereg","data","audited","verified","paper"];
const EMOJI = {idea:"🌰",prereg:"🌱",data:"🌿",audited:"🪴",verified:"🌳",paper:"🍎"};
const COLOR = {idea:"#b8a98c",prereg:"#9acd32",data:"#58a758",
               audited:"#2e8b57",verified:"#166b3f",paper:"#c8443c"};
const DEAD = "#8a6d4b";

// stable branch slot per slug, by first appearance in history
const slot = {}; let nSlots = 0;
SNAPS.forEach(s => s.lines.forEach(l => { if (!(l.slug in slot)) slot[l.slug] = nSlots++; }));

const svg = document.getElementById("tree");
const scrub = document.getElementById("scrub");
scrub.max = SNAPS.length - 1;

const BASE_X = 450, BASE_Y = 590;
function draw(fi) {
  const snap = SNAPS[fi];
  const present = snap.lines;
  const maxSlot = Math.max(...present.map(l => slot[l.slug]), 0);
  const trunkH = Math.min(90 + (maxSlot + 1) * 48, 520);
  let g = `<line x1="60" y1="${BASE_Y}" x2="840" y2="${BASE_Y}" stroke="#b9b19a"/>`;
  g += `<path d="M ${BASE_X} ${BASE_Y} Q ${BASE_X-8} ${BASE_Y-trunkH/2} ${BASE_X} ${BASE_Y-trunkH}"
        stroke="#6b4f2a" stroke-width="10" fill="none" stroke-linecap="round"/>`;
  present.forEach(l => {
    const i = slot[l.slug], side = i % 2 === 0 ? 1 : -1;
    const ay = BASE_Y - 70 - i * 48;
    const stIdx = STAGES.indexOf(l.stage);
    const len = 60 + stIdx * 26;
    const droop = l.dead ? 34 : -18 - stIdx * 4;   // dead branches droop
    const ex = BASE_X + side * len;
    const ey = ay + droop;
    const col = l.dead ? DEAD : COLOR[l.stage];
    g += `<path d="M ${BASE_X} ${ay} Q ${BASE_X + side*len*0.5} ${ay - (l.dead ? -6 : 14)} ${ex} ${ey}"
          stroke="${l.dead ? DEAD : "#7a5c33"}" stroke-width="4" fill="none"
          ${l.dead ? 'stroke-dasharray="5 4"' : ""} stroke-linecap="round"/>`;
    g += `<circle class="leaf" data-slug="${l.slug}" cx="${ex}" cy="${ey}" r="${9 + stIdx}"
          fill="${col}" stroke="#faf8f2" stroke-width="2"/>`;
    g += `<text x="${ex + side*14}" y="${ey + 4}" font-size="12"
          text-anchor="${side === 1 ? "start" : "end"}"
          fill="${l.dead ? DEAD : "#2b2b2b"}">${l.dead ? "✝ " : ""}${l.slug} ${EMOJI[l.stage]}</text>`;
  });
  svg.innerHTML = g;
  document.getElementById("date").textContent = snap.ts;
  document.getElementById("d-snap").textContent =
    `${snap.ts} — ${present.length} lines of work, ` +
    `${present.filter(l => l.stage === "verified" || l.stage === "paper").length} verified+, ` +
    `${present.filter(l => l.dead).length} in the graveyard`;
  svg.querySelectorAll(".leaf").forEach(c => c.addEventListener("click", () => {
    const l = present.find(x => x.slug === c.dataset.slug);
    document.getElementById("d-title").textContent = `${EMOJI[l.stage]} ${l.slug}`;
    document.getElementById("d-body").innerHTML =
      `stage: <b>${l.stage}</b>${l.dead ? " (dead — see graveyard)" : ""}` +
      `<br>${l.note ? l.note : "<span class='muted'>no note</span>"}`;
  }));
}

document.getElementById("legend").innerHTML =
  STAGES.map(s => `<span>${EMOJI[s]} ${s}</span>`).join("") + `<span>✝ graveyard</span>`;
scrub.addEventListener("input", () => draw(+scrub.value));

let timer = null;
document.getElementById("play").addEventListener("click", function () {
  if (timer) { clearInterval(timer); timer = null; this.textContent = "▶ Play"; return; }
  if (+scrub.value >= SNAPS.length - 1) scrub.value = 0;
  this.textContent = "⏸ Pause";
  timer = setInterval(() => {
    if (+scrub.value >= SNAPS.length - 1) { clearInterval(timer); timer = null;
      document.getElementById("play").textContent = "▶ Play"; return; }
    scrub.value = +scrub.value + 1; draw(+scrub.value);
  }, 700);
});

draw(SNAPS.length - 1);
scrub.value = SNAPS.length - 1;
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
