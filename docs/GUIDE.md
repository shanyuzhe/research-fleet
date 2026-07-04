# The Guide — how a ResearchFleet project actually flows

> One page to answer the two questions every new user asks: **"when does
> which agent fire?"** and **"what exactly do I do every day?"**
> ([中文版](GUIDE.zh-CN.md))

## The two promises

Everything in this system serves two goals; if a feature ever fights them,
the feature is wrong:

1. **Steady progress.** Every working day moves at least one thread one
   visible step on the tree — and nothing ever silently moves backwards:
   verified results don't get relitigated, dead directions don't get
   resurrected, project state never lives only in a chat scrollback.
2. **You finish smarter.** Every AI output is designed to *leave you
   questions, not answers*: confusions become cards you answer yourself,
   judgment slides stay blank, the vault turns project history into your
   own knowledge web. Automation that makes the human dumber is a bug.

## The one orchestration rule: you never call agents

There is no agent API to learn. You talk to the **leader** (your main
session) in plain language; the leader knows the routing table and the
gates. This table is the whole "orchestration manual":

| the situation | you say something like | who flies | what lands on disk | what only YOU do |
|---|---|---|---|---|
| new idea, unsure if taken | "Has anyone done X?" | scout | `docs/lit/<topic>.md`, novelty verdict | decide if the question is worth a thread |
| ready to test something | "Let's preregister X" | leader (with you) → auditor design-checks | `docs/prereg/x.md` + design-audit trace | sign off criteria & **kill condition** |
| prereg passed audit | "implement and run it" | engineer (smoke → production) | code, `experiments/results/<run>/` | approve runs > 1 h |
| just want to poke around | "let me try something quick" | engineer, scratch lane | `experiments/scratch/` (numbers can't enter claims) | remember: fun ≠ evidence |
| results landed | "are these real?" | auditor (experiment-audit) | verdict + trace (+ `audit_passed` on PASS) | rule on PARTIAL verdicts |
| audit passed | "promote it to a claim" | leader updates `claims/` | claim file `verified` (H1 hook enforces the marker) | decide the claim's phrasing boundaries |
| time to write | "draft the results section" | writer (firewalled) | `paper/src/` | write `NARRATIVE.md` first — the story is yours |
| group meeting Friday | "make the progress deck" | presenter | `presentations/<deck>/` | fill the judgment slides |
| reading a new paper | "paper-study deck for this PDF" | presenter (reverse-learning) | deck + confusion ledger | read the paper *against the ledger* |
| end of the day | "wrap up" | steward | `CURRENT_STATE.md`, growth log, `notes/` refresh | 10-min vault ritual (below) |
| every few weeks | "optimize the fleet" | coach | `docs/fleet/improvement_<date>.md` | approve / reject proposals — none apply themselves |

Two habits cover 90% of days: **start a session by letting the leader read
`docs/CURRENT_STATE.md`** (automatic if you enable the SessionStart hook),
and **end real working days with "wrap up"**.

## The life of one thread (the spine of the whole system)

Every research thread walks the same seven stations. The stages are the
tree emojis; the gates between them are mechanical:

```
 🌰 idea ──"preregister it"──▶ 🌱 prereg ──design-audit PASS──▶ implementation
     ▲                            │ FAIL blocks — that's the point
     │                            ▼
 scout novelty check         smoke gate ──▶ production (3 seeds)
                                              │
                                              ▼
 🍎 in paper ◀── claim verified 🌳 ◀──experiment-audit PASS──🌿 data → 🪴 audited
                (audit_passed marker         │
                 unlocks; H1 hook            └─ FAIL/kill → ✝ graveyard,
                 blocks shortcuts)              epitaph written, never deleted
```

What this buys: at any moment, `python tools/growth_tree.py --ascii` shows
every thread at its true station, and `python tools/fleet_status.py` proves
no thread skipped a gate. That is "steady progress" made checkable.

## How the Obsidian vault gets generated — the SOP map

You never "write notes" as a separate chore, and you never ask for a note
explicitly. The vault is a **by-product of the SOP**: normal research
actions leave raw material behind, and one phrase — **"wrap up"** — makes
the steward harvest all of it into `notes/`. This table is the full
generation map:

| SOP step (what you did today) | raw material it leaves | what appears in `notes/` after "wrap up" | your follow-up |
|---|---|---|---|
| asked "has anyone done X?" (scout) | verified entry in `docs/lit/` | `papers/<slug>.md` — metadata + why it entered the project | add your reading notes below the markers |
| made a paper-study deck (presenter) | `confusion.md` ledger next to the deck | each unresolved confusion → a **concept card stub** + a "worth understanding" checkbox in today's daily note | read the paper against the ledger, answer the card |
| an audit came back (auditor) | Blocking items in the verdict | each blocking item → "worth understanding" entry, concept stub if it names a concept | answer, or rule on the PARTIAL |
| any thread changed stage (prereg/run/verify/paper) | growth-log diff | `daily/<today>.md` "What moved" + the thread's `lines/<slug>.md` timeline | skim; add "My take" if a call was yours |
| killed a thread | kill verdict + epitaph | the line note gains its epitaph + a concept card for the failure mode | write "what I actually learned" — dead threads are tuition |
| made a gate call that felt expensive | your line in the outcome ledger | surfaces in "worth understanding" | one honest sentence is enough |

Two consequences worth spelling out:

- **No "wrap up", no vault growth.** If the vault feels stale, you skipped
  the phrase — it is the single trigger, deliberately (one ritual, not five).
- **The machine only ever asks; sections that make you smarter are yours.**
  Concept-card answers, "My take", "What I actually learned" — if the fleet
  ever fills those in, that's a bug (and a ledger-worthy one).

## The daily 10 minutes (where internalization happens)

The steward maintains `notes/` as an Obsidian vault. Your ritual, after
"wrap up":

1. Open `notes/daily/<today>.md`. **What moved today** is already filled in
   (from the growth log); skim it.
2. **Worth understanding** lists what the fleet couldn't ground today —
   confusion-ledger entries, audit blocking items, gate decisions. Each
   links to a concept card stub.
3. Pick ONE card and write the answer in your own words. That's it.
4. (Optional) add a line under **My take** — why today's calls made sense.

The vault's structure and what the knowledge web looks like as it grows:
see the [obsidian-notes contract](../skills/shared/references/obsidian-notes.md)
and the **living example** in
[`examples/demo-project/notes/`](../examples/demo-project/notes/) — open
that folder in Obsidian and look at the graph view: threads are clusters,
your concept cards are the bridges between them, unanswered cards are the
orphan nodes begging for attention. The fleet asks the questions; the
answers are yours — that is the internalization contract.

## Where you are irreplaceable (by design)

The system will stall rather than guess on these — they are the judgment
calls that make the research *yours*:

- the research question and whether a thread deserves to exist
- preregistration success criteria and kill conditions
- gate rulings on PARTIAL audits ("do we re-run or accept with a caveat?")
- killing a thread (and its one-line epitaph)
- the paper's story (`NARRATIVE.md`) and every judgment slide
- concept-card answers
- approving coach proposals

If a week passes without any of these landing on your desk, something is
wrong — check `docs/CURRENT_STATE.md`'s "pending inputs" section.

## When things feel off

| smell | do this |
|---|---|
| "did we skip something?" | `python tools/fleet_status.py` — red means a gate violation is already on disk |
| leader acting like a generic chatbot | say "re-read CLAUDE.md" (or enable the SessionStart hook) |
| same friction three days in a row | log it honestly in the ledger, then "optimize the fleet" — the coach exists for exactly this |
| tempted to hand-edit a claim to `verified` | don't — run the audit; with hooks on, the edit bounces anyway |
