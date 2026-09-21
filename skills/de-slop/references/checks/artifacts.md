---
type: check
layer: 1-universal
status: active
last-refreshed: 2026-06-10
---

# Check: artifacts

The cheap "did the AI actually finish" check. Catch leftover junk that should never ship. These bundle into the mechanical "clean the mechanical stuff" item. Flag and suggest. For every finding, quote the artifact and give the fix: the real value, or delete it.

## 1. Placeholders

- Bracket and template tokens: [brackets], {{curly}}, <angle placeholders>, "[your name]", "[Company]", "{date}".
- Editorial markers: TODO, TBD, TK, FIXME, XXX, "INSERT X HERE", "ADD LINK".
- Filler text: lorem ipsum, "sample text," an obviously fake example name or number left in place.

## 2. Model and chat residue

- Assistant phrases left in: "as an AI language model," "here is the revised version," "sure, here you go," "I've updated the section as requested."
- Meta-commentary meant to be deleted: "(this paragraph addresses the feedback)," "Note to self," a leftover instruction from the prompt.
- Conversation leakage: references to "the document above," "as discussed in our chat," "per your last message" in a standalone piece.
- Duplicated blocks from regeneration: the same paragraph or list appearing twice with minor variation.

## 3. Broken structure

- Malformed markdown: an unclosed list or code fence, raw `**asterisks**` or `#` showing in a rendered context, a heading with nothing under it.
- Tables missing cells, a column that lost its header, rows misaligned.
- Truncated endings: a sentence that cuts off mid-thought, "...", "(continued)", a final section that is just a heading.
- Numbering that breaks: a list that goes 1, 2, 2, 4, or footnote markers pointing nowhere.

## 4. Dead and placeholder links, assets, and values

- example.com, a bare [link], "URL here," an obviously templated or broken URL.
- An image reference to a file that does not exist, an empty embed, a broken anchor.
- Inconsistent template values: one slot filled with the real client name and another still holding the previous client or the example value.
- Stray file junk in a deliverable folder: temp files, "-v2-final-FINAL" duplicates, unreferenced assets.

## Grading

- Aligned: nothing left over. The piece reads as finished.
- Drift: a stray cosmetic artifact, not embarrassing (a broken footnote number, one raw markdown asterisk in an internal doc).
- Misaligned: a placeholder, model artifact, dead link, truncated ending, or wrong-client value that would ship visibly.
