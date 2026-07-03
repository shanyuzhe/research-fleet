# Presentation Contract — decks that survive a hostile audience

> contract-version: 0.2

Governs the presenter agent. Distilled from a battle-tested paper-study
pipeline ("reverse-learning method") and its accumulated pitfall list.

## The reverse-learning method (paper-study decks)

Build the deck **before** deep-reading the paper. Slide-building forces
operational understanding: every figure you must place, every number you
must source, every formula you must transcribe is a probe. Whatever you
cannot ground goes to `confusion.md`:

```markdown
# Confusion ledger — <paper>
- [ ] Eq. 7: why is the temperature inside the softmax, not outside? (§3.2)
- [ ] Table 3 row 2 beats row 4 — contradicts the §5 story?
```

The human then reads the paper *against this ledger* — an order of
magnitude more efficient than linear reading. Never let the deck hide a
confusion behind fluent prose; a papered-over gap resurfaces in Q&A.

## Slide grammar (defaults; theme tokens in `presentations/STYLE.md`)

- **Cover**: paper title (original + translated if bilingual), authors,
  venue, presenter name from STYLE.md. Include ONLY the fields STYLE.md
  lists (e.g., some users forbid an "advisor:" line — respect it).
- **TOC**: numbered entries, big accent numerals + primary-language title +
  secondary-language subtitle.
- **Section dividers**: oversized section numeral + bilingual heading.
- **Content slides**: decorated title bar; ≤ ~15 lines; key digits bold in
  accent color; marker glyph (`▍`) for emphasis lines; **source footer on
  every content slide**.
- **Judgment slides** (Limitations / Conclusion / Takeaway): blank template
  + placeholder hint. Never filled by AI.
- **Closing**: thanks + presenter name (same field policy as cover).
- Word budget: ≲1000 words of bullets across the whole deck — slides carry
  visuals and anchors, the speaker carries the prose.

Default deck skeleton (18–22 slides, scale to paper complexity):
cover → TOC → §1 background/motivation → §2 method/architecture (figures
from PDF) → §3 setup (digits verified) → §4 results (main table + ablations
from PDF) → §5 judgment slides (BLANK) → closing.

## Figure extraction (zero-hallucination visuals)

- Extract with PyMuPDF at ≥300 DPI. Locate figures/tables by **text
  anchors** (`page.get_text("dict")`, search "Figure N:", "Table N:") —
  never eyeball page numbers or bboxes.
- Determine the figure's extent from **drawings + image clusters** (vector
  lines and images), not from "the text block above" — table rows are text
  blocks too, and y-offset heuristics swallow body text.
- Caption bbox: use the block containing the caption's first line, not a
  fixed-pt expansion.
- If a caption can't be located (split across pages, parser noise):
  fall back to a full-page screenshot — getting the real figure matters
  more than a tight crop.
- After extraction, **Read every image** to confirm the crop before
  building slides.

## Build pipeline

1. **Probe the source** — metadata (title/authors/venue/pages) + a
   figure/table index with exact page numbers. Show it to the user for
   confirmation before designing.
2. **Design the skeleton inline** — full slide table (number, layout,
   title, figure source, who-writes: AI or BLANK-for-user) pasted into the
   conversation, adjusted with the user before building.
3. **Extract figures** (rules above).
4. **Build the deck** via a reusable project helper module (create
   `tools/deck_kit.py` on first use; keep all layout helpers, color
   constants and template post-processing there — per-deck scripts contain
   only content). python-pptx notes: it does not parse markdown (`**bold**`
   must become styled runs); template sample slides need id-list AND
   relationship removal; template-bundled logos must be replaced with the
   STYLE.md logo; layouts without placeholders need absolute-positioned
   text boxes. On Windows, kill any open PowerPoint process before writing,
   and export via a PowerShell COM script run with `-NoProfile`.
5. **Self-review, tiered** — rendering every slide to PNG on every round is
   the kind of cost that gets the whole review step skipped under pressure,
   so tier it: **full render** on the first complete build (it becomes the
   visual reference) and on final delivery; **intermediate rounds render
   only the 5 key slides** (cover, TOC, one section divider, one content
   slide, one judgment slide). Whatever is rendered gets the same checks:
   compare against the reference deck named in STYLE.md; verify digits,
   source footers, no literal `**` markdown residue, no stretched images.
6. **Reviewer audit** (below), then deliver with evidence.

## Reviewer audit checklist

| check | how |
|---|---|
| Digit hallucination | every number re-checked against source, digit-by-digit |
| Self-consistency | same fact phrased identically across slides ("h=8" vs "8 heads") |
| Missing sources | any slide with a number/figure but no source footer |
| Formula fidelity | symbols, sub/superscripts, summation bounds vs source |
| Deleted-section residue | after removing a section, grep the deck for dangling references |
| External-claim hallucination | "later adopted by X" claims verified or removed |
| Comparison discipline | "X beats Y" needs both numbers, not "significantly" |
| Ghostwriting scan | judgment slides are genuinely blank; grep for speculation markers ("possibly to", "likely because") — each either gets a source or becomes a placeholder |
| Style-policy fields | forbidden fields (per STYLE.md) appear nowhere |

Output: finding list with P0 (must fix) / P1 (should) / P2 (optional).
Findings are reported, not silently fixed — the human decides.

## Fleet integration

- Progress decks: result slides cite claim IDs; claim status shown honestly
  (`verified` vs `indicative`) — a deck is a claim consumer, same rules as
  the paper.
- Talk decks: NARRATIVE.md terminology map applies; internal codenames
  never reach a screen.
- Unresolved confusion entries are returned to the PI as candidate
  research questions — the ledger feeds the research loop, not a drawer.
