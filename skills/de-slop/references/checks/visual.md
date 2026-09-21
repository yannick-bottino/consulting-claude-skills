---
type: check
layer: 2-company
status: template
last-refreshed: YYYY-MM-DD
source: distilled from your Context/brand doc (visual identity). Re-run the adapter to refresh.
---

# Check: visual

> PLACEHOLDER FILE. The structure is real; the colors, fonts, and tokens are generic examples.
> Replace every bracketed value with your own design system, then delete this note.

Does the visual match the [your brand] design system for its surface. One system governs everything this check grades: web, slides, decks, docs, social graphics, and diagrams. [Note any surface that is out of scope — e.g. social thumbnails that follow their own packaging workflow.] Flag and suggest the concrete change.

## 1. Design language

[Describe your overall design language in a few sentences — e.g. minimalist / neo-brutalist / editorial. What is allowed and what is banned at the conceptual level: gradients, shadows, decoration, photography. The feeling the design should give. Tie it back to your brand stance.]

## 2. Color palette

[State whether flat fills, gradients, etc. are allowed.]

| Color | Hex | Usage |
|---|---|---|
| [Ink / primary text] | `#000000` | [Primary text, borders] |
| [Canvas / background] | `#FFFFFF` | [Default background] |
| [Accent one] | `#XXXXXX` | [Where it is used] |
| [Accent two] | `#XXXXXX` | [Where it is used] |
| [Accent three] | `#XXXXXX` | [Where it is used] |

Hard rule: **[your single most important visual rule, e.g. never a black background on web/slides/docs/social]**. Off-palette colors are a finding.

## 3. Typography

| Usage | Font |
|---|---|
| Headings | [Heading font] |
| Body | [Body font] |
| Data, labels, code | [Mono / label font] |
| Fallback | [Fallback] |

[Casing rule for headings.] No more than [N] weights per layout. Body text never below comfortable reading size for the surface.

## 4. Structural tokens

- Shadows: [your shadow rule — e.g. solid offset, zero blur, specific steps; or none].
- Borders: [your border rule — e.g. 2px solid ink].
- Corner radius: [your radius rules per element type].
- Spacing: [your spacing philosophy — e.g. generous white space, one idea per block]. Dense, cramped layouts are off-brand even with the right palette.

## 5. Per-surface application

| Surface | What on-brand looks like |
|---|---|
| Web and landing pages | [What good looks like here.] |
| Slides and decks | [What good looks like here.] |
| Docs and PDFs | [What good looks like here.] |
| Social graphics | [What good looks like here.] |
| Diagrams | [What good looks like here.] |

Misaligned on these surfaces: [your universal visual failures — e.g. off-palette colors, wrong fonts, banned effects, no focal point, decoration that fights the content].

[If a surface is out of scope, state the skip rule here.]

## Grading

- Aligned: palette, fonts, and tokens all match the surface, one clear focal point, generous spacing.
- Drift: a near-off hex, weak hierarchy, a slightly wrong shadow, cramped spacing, a missing accent.
- Misaligned: anything on the per-surface list above. The universal ones: [your hard bans — e.g. a banned background, a banned effect, an off-system font].
