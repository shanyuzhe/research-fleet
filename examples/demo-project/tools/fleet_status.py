#!/usr/bin/env python3
"""Fleet status — turn ResearchFleet gate violations into a mechanical check.

The fleet's discipline lives in files, not vigilance: a claim upgrades to
`verified` only when an `audit_passed` marker sits next to a PASS verdict, a
run only counts when its manifest is complete and points at a real prereg,
and the growth log must agree with the claims/traces on disk. This script
reads those files and reports where the invariants are broken — so a
violation is *detected*, not merely visible.

It reads (all paths relative to the project root, auto-detected by walking up
from the cwd until a `.fleet/` directory is found; override with --root):

  claims/*.md                     claim-as-file frontmatter (status, evidence, audit_trace)
  .fleet/traces/**/audit_passed   PASS markers  + sibling verdict.md
  experiments/results/<run>/manifest.json   run packages (non-scratch)
  docs/prereg/*.md                preregistrations referenced by manifests
  .fleet/growth.jsonl             the tree's stage log (last snapshot)
  .fleet/outcomes.jsonl           the outcome ledger (heartbeat)

Checks (🔴 red = blocking, 🟡 yellow = warning):

  C1  claim↔marker    a `verified` claim whose trace dir is missing or has no audit_passed
  C2  marker↔verdict  an audit_passed with no verdict.md, or a verdict that is not PASS
  C3  prereg gate     a non-scratch run whose manifest points at a missing prereg
  C4  manifest        a run manifest missing required fields (git_commit / seeds / env / config)
  C5  evidence        a claim frontmatter evidence path that does not exist
  C6  tree↔ledger     growth.jsonl last snapshot disagrees with claims about verified state
  C7  heartbeat 🟡    no new outcomes.jsonl entry in the last 7 days (disable with --no-heartbeat)

Usage:
  python tools/fleet_status.py                 # dashboard for the auto-detected project
  python tools/fleet_status.py --root PATH      # point at a specific project root
  python tools/fleet_status.py --json           # machine-readable result
  python tools/fleet_status.py --check-claim claims/C3_readout_gap.md
                                                # hook mode: only C1/C5 for one claim
  python tools/fleet_status.py --no-heartbeat   # skip the C7 heartbeat warning
  python tools/fleet_status.py --ascii          # force [OK]/[WARN]/[FAIL] instead of emoji

Exit codes:  0 = all green (yellows allowed)   1 = at least one red   2 = script/usage error

Zero third-party dependencies; Python 3.8+.
"""
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HEARTBEAT_DAYS = 7
VERIFIED_STAGES = ("verified", "paper")  # growth stages that assert a verified claim


def die(msg):
    """Usage / script errors exit 2 (distinct from 1 = a real gate violation)."""
    print(f"[fail] {msg}", file=sys.stderr)
    sys.exit(2)


# --------------------------------------------------------------------------- #
# presentation helpers
# --------------------------------------------------------------------------- #
def _supports_emoji():
    enc = (sys.stdout.encoding or "").lower()
    try:
        "🟢".encode(enc or "ascii")
        return True
    except Exception:
        return False


class Sym:
    """Status glyphs with a plain-ASCII fallback for GBK / dumb terminals."""

    def __init__(self, emoji):
        if emoji:
            self.GREEN, self.YELLOW, self.RED = "🟢", "🟡", "🔴"
            self.OK, self.BAD = "✓", "✗"
        else:
            self.GREEN, self.YELLOW, self.RED = "[OK]  ", "[WARN]", "[FAIL]"
            self.OK, self.BAD = "y", "n"

    def dot(self, level):
        return {"green": self.GREEN, "yellow": self.YELLOW, "red": self.RED}[level]


# --------------------------------------------------------------------------- #
# small parsers (fail loud — a malformed project file is reported, never skipped)
# --------------------------------------------------------------------------- #
def _strip_comment(v):
    # drop a trailing "  # ..." inline comment (whitespace + hash); paths rarely contain " #"
    return re.sub(r"\s+#.*$", "", v).strip()


def parse_frontmatter(text, path):
    """Minimal YAML-frontmatter reader: top-level `key: value` + `key:`/`- item` lists."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: missing YAML frontmatter (no opening '---')")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError(f"{path}: frontmatter is not closed (no second '---')")

    fm = {}
    cur_key = None
    for raw in lines[1:end]:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- ") and cur_key is not None:
            val = _strip_comment(stripped[2:].strip())
            fm.setdefault(cur_key, [])
            if isinstance(fm[cur_key], list):
                fm[cur_key].append(val)
            continue
        if ":" not in stripped:
            continue
        key, _, rest = stripped.partition(":")
        key = key.strip()
        rest = rest.strip()
        cur_key = key
        fm[key] = [] if rest == "" else _strip_comment(rest)
    return fm


def _scalar(fm, key, default=""):
    v = fm.get(key, default)
    if isinstance(v, list):
        return v[0] if v else default
    return v


def load_claims(root, errors):
    """Return list of parsed claim dicts. Records parse failures in `errors`."""
    out = []
    cdir = root / "claims"
    if not cdir.is_dir():
        return out
    for p in sorted(cdir.glob("*.md")):
        if p.name.lower() == "readme.md":
            continue
        rel = p.relative_to(root).as_posix()
        try:
            fm = parse_frontmatter(p.read_text(encoding="utf-8"), rel)
        except Exception as e:
            errors.append(str(e))
            continue
        cid = _scalar(fm, "id") or p.stem
        out.append({
            "file": p.relative_to(root).as_posix(),
            "id": cid,
            "slug": re.sub(r"^C\d+_", "", cid),  # C3_readout_gap -> readout_gap
            "status": _scalar(fm, "status"),
            "audit_trace": _scalar(fm, "audit_trace"),
            "evidence": [e for e in fm.get("evidence", []) if e] if isinstance(
                fm.get("evidence"), list) else [],
        })
    return out


def load_markers(root):
    """Every audit_passed marker under .fleet/traces, with its sibling verdict."""
    out = []
    tdir = root / ".fleet" / "traces"
    if not tdir.is_dir():
        return out
    for marker in sorted(tdir.rglob("audit_passed")):
        d = marker.parent
        verdict = d / "verdict.md"
        conclusion = None
        if verdict.is_file():
            conclusion = read_verdict_conclusion(verdict)
        out.append({
            "dir": d.relative_to(root).as_posix(),
            "has_verdict": verdict.is_file(),
            "conclusion": conclusion,
        })
    return out


def read_verdict_conclusion(path):
    """Return PASS / PARTIAL / FAIL from a verdict.md's `# Verdict: X` header, or None."""
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"#\s*Verdict:\s*([A-Za-z]+)", line.strip())
        if m:
            return m.group(1).upper()
    return None


def load_runs(root, errors):
    """Immediate non-scratch subdirectories of experiments/results/ as run packages."""
    out = []
    rdir = root / "experiments" / "results"
    if not rdir.is_dir():
        return out
    for run in sorted(rdir.iterdir()):
        if not run.is_dir() or run.name.startswith((".", "_")) or run.name == "scratch":
            continue
        mpath = run / "manifest.json"
        manifest, ok = None, mpath.is_file()
        if ok:
            try:
                manifest = json.loads(mpath.read_text(encoding="utf-8"))
            except Exception as e:
                errors.append(f"run {run.name}/manifest.json: bad JSON: {e}")
                ok = False
        out.append({
            "slug": run.name,
            "has_manifest": mpath.is_file() and manifest is not None,
            "manifest": manifest,
        })
    return out


def load_last_growth(root, errors):
    """Last snapshot of .fleet/growth.jsonl (or None)."""
    src = root / ".fleet" / "growth.jsonl"
    if not src.is_file():
        return None
    snaps = []
    for i, raw in enumerate(src.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            snaps.append(json.loads(raw))
        except json.JSONDecodeError as e:
            errors.append(f".fleet/growth.jsonl:{i}: bad JSON: {e}")
    if not snaps:
        return None
    snaps.sort(key=lambda s: s.get("ts", ""))
    return snaps[-1]


def load_last_outcome_date(root, errors):
    src = root / ".fleet" / "outcomes.jsonl"
    if not src.is_file():
        return None
    last = None
    for i, raw in enumerate(src.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            errors.append(f".fleet/outcomes.jsonl:{i}: bad JSON: {e}")
            continue
        ts = obj.get("ts")
        if ts:
            try:
                d = datetime.strptime(ts, "%Y-%m-%d").date()
            except ValueError:
                errors.append(f".fleet/outcomes.jsonl:{i}: bad ts {ts!r} (want YYYY-MM-DD)")
                continue
            if last is None or d > last:
                last = d
    return last


# --------------------------------------------------------------------------- #
# checks — each returns a list of violation strings
# --------------------------------------------------------------------------- #
def check_c1(root, claims):
    v = []
    for c in claims:
        if c["status"] != "verified":
            continue
        tr = c["audit_trace"]
        if not tr:
            v.append(f"{c['id']}: status=verified but no audit_trace field")
            continue
        d = root / tr
        if not d.is_dir():
            v.append(f"{c['id']}: audit_trace dir missing: {tr}")
        elif not (d / "audit_passed").is_file():
            v.append(f"{c['id']}: trace has no audit_passed marker: {tr}")
    return v


def check_c2(markers):
    v = []
    for m in markers:
        if not m["has_verdict"]:
            v.append(f"{m['dir']}: audit_passed present but no verdict.md")
        elif m["conclusion"] != "PASS":
            v.append(f"{m['dir']}: audit_passed but verdict is {m['conclusion'] or 'unparseable'}")
    return v


def check_c3(root, runs):
    v = []
    for r in runs:
        if not r["has_manifest"]:
            continue  # missing manifest is a C4 concern
        prereg = r["manifest"].get("prereg")
        if not prereg:
            v.append(f"{r['slug']}: manifest has no prereg field")
        elif not (root / prereg).exists():
            v.append(f"{r['slug']}: prereg file not found: {prereg}")
    return v


def check_c4(runs):
    required = ("git_commit", "seeds", "env", "config")
    v = []
    for r in runs:
        if not r["has_manifest"]:
            v.append(f"{r['slug']}: no manifest.json")
            continue
        m = r["manifest"]
        for field in required:
            if field not in m or m[field] in (None, "", [], {}):
                v.append(f"{r['slug']}: manifest missing/empty required field: {field}")
    return v


def check_c5(root, claims):
    v = []
    for c in claims:
        for ev in c["evidence"]:
            if not (root / ev).exists():
                v.append(f"{c['id']}: evidence path does not exist: {ev}")
    return v


def check_c6(snap, claims):
    """Growth log's last snapshot must agree with claims on the verified boundary."""
    if not snap:
        return []
    v = []
    verified_slugs = {c["slug"] for c in claims if c["status"] == "verified"}
    live = [ln for ln in snap.get("lines", []) if not ln.get("dead")]
    growth_verified = {ln["slug"] for ln in live if ln.get("stage") in VERIFIED_STAGES}

    for ln in live:
        if ln.get("stage") in VERIFIED_STAGES and ln["slug"] not in verified_slugs:
            v.append(f"growth stage={ln.get('stage')} for '{ln['slug']}' but no verified claim backs it")
    for slug in verified_slugs:
        if slug not in growth_verified:
            v.append(f"claim '{slug}' is verified but growth log's last snapshot does not show it verified/paper")
    return v


def check_c7(root, last_outcome, today):
    if last_outcome is None:
        return [".fleet/outcomes.jsonl has no dated entries"]
    gap = (today - last_outcome).days
    if gap > HEARTBEAT_DAYS:
        return [f"no outcomes.jsonl entry in {gap} days (last {last_outcome.isoformat()})"]
    return []


# --------------------------------------------------------------------------- #
# root discovery
# --------------------------------------------------------------------------- #
_EXT = "\\\\?\\"  # Windows extended-length prefix: the 4 chars \ \ ? \


def _longpath(p):
    """On Windows, prefix an absolute path with \\?\\ so filesystem ops bypass
    the 260-char MAX_PATH limit even when LongPathsEnabled is off. Without this,
    listdir/scandir raise and is_file() can silently return False on deep paths —
    which would turn a real violation into a false green."""
    if os.name != "nt":
        return p
    s = str(p)
    return p if s.startswith(_EXT) else Path(_EXT + s)


def _display(p):
    """Strip the \\?\\ prefix for human/JSON output."""
    s = str(p)
    return s[len(_EXT):] if s.startswith(_EXT) else s


def find_root(explicit):
    if explicit:
        r = _longpath(Path(explicit).resolve())
        if not (r / ".fleet").is_dir():
            die(f"--root {_display(r)} has no .fleet/ directory")
        return r
    cur = Path.cwd().resolve()
    for cand in (cur, *cur.parents):
        if (_longpath(cand) / ".fleet").is_dir():
            return _longpath(cand)
    die("no .fleet/ found from cwd upward — run inside a fleet project or pass --root")


# --------------------------------------------------------------------------- #
# orchestration
# --------------------------------------------------------------------------- #
CHECK_META = [
    ("C1", "claim<->marker",  "red"),
    ("C2", "marker<->verdict", "red"),
    ("C3", "prereg gate",     "red"),
    ("C4", "manifest",        "red"),
    ("C5", "evidence",        "red"),
    ("C6", "tree<->ledger",   "red"),
    ("C7", "heartbeat",       "yellow"),
]


def run_all(root, no_heartbeat, today):
    errors = []
    claims = load_claims(root, errors)
    markers = load_markers(root)
    runs = load_runs(root, errors)
    snap = load_last_growth(root, errors)
    last_outcome = load_last_outcome_date(root, errors)

    results = {
        "C1": check_c1(root, claims),
        "C2": check_c2(markers),
        "C3": check_c3(root, runs),
        "C4": check_c4(runs),
        "C5": check_c5(root, claims),
        "C6": check_c6(snap, claims),
        "C7": [] if no_heartbeat else check_c7(root, last_outcome, today),
    }
    return errors, claims, markers, runs, snap, results


def level_of(check_id, violations, results, errors):
    if not violations:
        return "green"
    sev = dict((cid, sev) for cid, _, sev in CHECK_META)[check_id]
    return sev


# --------------------------------------------------------------------------- #
# renderers
# --------------------------------------------------------------------------- #
def render_dashboard(root, errors, claims, markers, runs, snap, results, no_heartbeat, sym):
    out = []
    out.append(f"ResearchFleet status — {_display(root)}")
    out.append("=" * 60)

    # parse errors first — a malformed contract file is a red, reported loudly
    if errors:
        out.append("")
        out.append(f"{sym.RED} parse errors ({len(errors)}) — fix these files:")
        for e in errors:
            out.append(f"    - {e}")

    out.append("")
    out.append("Gates")
    for cid, name, _sev in CHECK_META:
        vio = results[cid]
        lvl = level_of(cid, vio, results, errors)
        label = "ok" if not vio else f"{len(vio)} issue(s)"
        out.append(f"  {sym.dot(lvl)}  {cid} {name:<16} {label}")
        for msg in vio:
            out.append(f"        - {msg}")

    # Claims column
    out.append("")
    out.append(f"Claims ({len(claims)})")
    if not claims:
        out.append("    (none)")
    for c in claims:
        bad = [m for m in results["C1"] + results["C5"] if m.startswith(c["id"] + ":")]
        lvl = "red" if bad else ("green" if c["status"] == "verified" else "yellow")
        trace = f"trace {sym.OK}" if c["status"] == "verified" and not bad else c["status"]
        out.append(f"  {sym.dot(lvl)}  {c['id']:<22} {c['status']:<12} {trace}")

    # Traces column
    out.append("")
    out.append(f"Traces ({len(markers)})")
    if not markers:
        out.append("    (none)")
    for m in markers:
        lvl = "green" if m["has_verdict"] and m["conclusion"] == "PASS" else "red"
        out.append(f"  {sym.dot(lvl)}  {m['dir']:<44} {m['conclusion'] or 'no verdict'}")

    # Runs column
    if runs:
        out.append("")
        out.append(f"Runs ({len(runs)})")
        for r in runs:
            bad = [m for m in results["C3"] + results["C4"] if m.startswith(r["slug"] + ":")]
            lvl = "red" if bad else "green"
            state = "manifest " + (sym.OK if r["has_manifest"] else sym.BAD)
            out.append(f"  {sym.dot(lvl)}  {r['slug']:<22} {state}")

    # Summary
    n_red = sum(len(results[cid]) for cid, _, sev in CHECK_META if sev == "red" and results[cid])
    n_yellow = sum(len(results[cid]) for cid, _, sev in CHECK_META if sev == "yellow" and results[cid])
    has_red = bool(errors) or any(
        results[cid] for cid, _, sev in CHECK_META if sev == "red")
    out.append("")
    out.append("-" * 60)
    if has_red:
        tag = f"{sym.RED} RED — {n_red + len(errors)} blocking issue(s), {n_yellow} warning(s)"
    elif n_yellow:
        tag = f"{sym.YELLOW} YELLOW — {n_yellow} warning(s), no blocking issues"
    else:
        tag = f"{sym.GREEN} GREEN — all gates clear"
    out.append("Summary: " + tag)
    return "\n".join(out), has_red


def build_json(root, errors, claims, markers, runs, results):
    checks = []
    for cid, name, sev in CHECK_META:
        vio = results[cid]
        checks.append({
            "id": cid, "name": name, "severity": sev,
            "level": "green" if not vio else sev,
            "violations": vio,
        })
    has_red = bool(errors) or any(
        results[cid] for cid, _, sev in CHECK_META if sev == "red")
    return {
        "root": _display(root),
        "parse_errors": errors,
        "checks": checks,
        "claims": [{"id": c["id"], "status": c["status"]} for c in claims],
        "traces": [{"dir": m["dir"], "conclusion": m["conclusion"]} for m in markers],
        "runs": [{"slug": r["slug"], "has_manifest": r["has_manifest"]} for r in runs],
        "exit_code": 1 if has_red else 0,
    }


# --------------------------------------------------------------------------- #
# --check-claim: hook mode, only C1 + C5 for one file
# --------------------------------------------------------------------------- #
def check_single_claim(root, claim_path, as_json, sym):
    cand = Path(claim_path)
    if cand.is_absolute():
        p = _longpath(cand)                         # hook may pass an out-of-project temp file
    else:
        p = root / claim_path                       # inherits any \\?\ prefix
        if not p.is_file():
            p = _longpath(Path.cwd() / claim_path)  # fall back to cwd-relative
    if not p.is_file():
        die(f"claim file not found: {claim_path}")
    errors = []
    try:
        fm = parse_frontmatter(p.read_text(encoding="utf-8"), p.name)
    except Exception as e:
        if as_json:
            print(json.dumps({"claim": str(p), "ok": False, "violations": [str(e)]}))
        else:
            print(f"{sym.RED}  {p.name}: {e}")
        return 1
    cid = _scalar(fm, "id") or p.stem
    claim = {
        "id": cid, "file": p.name, "status": _scalar(fm, "status"),
        "audit_trace": _scalar(fm, "audit_trace"),
        "evidence": [e for e in fm.get("evidence", []) if e] if isinstance(
            fm.get("evidence"), list) else [],
    }
    vio = check_c1(root, [claim]) + check_c5(root, [claim])
    if as_json:
        print(json.dumps({"claim": str(p), "ok": not vio, "violations": vio}))
    else:
        if vio:
            print(f"{sym.RED}  {cid} — {len(vio)} violation(s):")
            for m in vio:
                print(f"    - {m}")
        else:
            print(f"{sym.GREEN}  {cid} — C1/C5 clean (status={claim['status']})")
    return 1 if vio else 0


# --------------------------------------------------------------------------- #
def main(argv):
    flags = {a for a in argv if a.startswith("--")}
    as_json = "--json" in flags
    no_heartbeat = "--no-heartbeat" in flags
    sym = Sym(emoji=("--ascii" not in flags) and _supports_emoji())

    def opt(name):
        if name in argv:
            i = argv.index(name)
            if i + 1 < len(argv):
                return argv[i + 1]
            die(f"{name} needs an argument")
        return None

    root = find_root(opt("--root"))
    today = date.today()

    claim_file = opt("--check-claim")
    if claim_file:
        return check_single_claim(root, claim_file, as_json, sym)

    errors, claims, markers, runs, snap, results = run_all(root, no_heartbeat, today)
    if as_json:
        payload = build_json(root, errors, claims, markers, runs, results)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return payload["exit_code"]

    text, has_red = render_dashboard(
        root, errors, claims, markers, runs, snap, results, no_heartbeat, sym)
    print(text)
    return 1 if has_red else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except SystemExit:
        raise
    except Exception as e:  # unexpected = script bug, not a project violation
        print(f"[fail] fleet_status crashed: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
