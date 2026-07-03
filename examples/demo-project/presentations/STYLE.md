# Presentation style — vlm-judge-probing

> Read by the presenter agent before building any deck. Edit once; every
> deck inherits it. Never hardcode style in build scripts.

## Identity

- Presenter name: _(as it should appear on cover/closing slides)_
- Institution: _(name; logo file path if available, e.g. `presentations/assets/logo.png`)_
- Cover/closing fields policy: presenter name only by default — list any
  additional fields explicitly if you want them (e.g. some presenters
  deliberately omit an "advisor:" line; the agent respects whatever is
  listed here and adds nothing more).

## Theme — "academic blue" (default)

- Canvas: 16:9. Fonts: serif for Latin/numbers (Times New Roman), native
  sans/serif for CJK if bilingual.
- Tokens: NAVY `#1F3864` (titles/emphasis) · ACCENT `#2E74B5` (numerals,
  subtitles) · DARK_GRAY `#404040` (body) · GRAY `#808080` (sources,
  placeholders) · RED `#C00000` (key digits only).
- Grammar: big accent numerals in TOC and section dividers; decorated
  title bar on content slides; `▍` emphasis marker; 10pt gray italic
  source footer.

## Reference deck (visual golden standard)

- Path: _(set after your first accepted deck, e.g.
  `presentations/2026-07-10_attention/deck.pptx`)_
- Every new deck's self-review compares key slides against it
  pixel-honestly: cover, TOC, one divider, one content slide, judgment
  slides (must be blank templates).

## Language

- Deck language(s): _(e.g. bilingual zh/en — zh primary, en subtitles)_
