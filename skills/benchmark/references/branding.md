# Branding Contract

Operational reference. Read before generating any visual deliverable (Phase 5).

This skill ships **no** brand charter of its own. It consumes one through the contract below, so the same skill can run on your own firm's charter, on a client's own charter, or with no charter at all. Never hardcode a colour, a logo, or a font family into the skill or into a generated file: resolve tokens through this contract.

## Contents
1. Resolution order
2. Token contract
3. Logo handling
4. Neutral fallback tokens
5. Phase 0 detection

---

## 1. Resolution order

Resolve the branding source once, at Phase 0, and record the result in `mission-config.json → branding`.

| Order | Condition | Action |
|-------|-----------|--------|
| 1 | `branding.skill` is set in mission-config | Invoke that skill and read its token values. It owns the charter; this skill only consumes tokens |
| 2 | `branding.tokens_file` is set | Read that file and map its values onto the token contract in section 2 |
| 3 | Neither is set | Use the neutral fallback of section 4 and say so in the delivery summary |

mission-config block:

```json
"branding": {
  "skill": "your-brand-skill | client-brand-skill | null",
  "tokens_file": "path relative to project root | null",
  "logo_path": "path to a logo file | null",
  "resolved": "skill | tokens_file | neutral-fallback"
}
```

Rules:
- A missing brand source is never a blocker. Fall back and continue.
- Never read a brand skill's internals to copy values into this skill's files. Consume at run time, per mission.
- If the consultant names a brand charter that has no skill and no token file, ask for the token values once, record them in `branding.tokens_file`, and continue.

---

## 2. Token contract

Generated HTML declares these CSS variables on `:root` and references nothing else. Every rule in `references/html-report-spec.md` is written against this list.

| Token | Role |
|-------|------|
| `--font-title` | Headings |
| `--font-body` | Body text |
| `--bg` | Page background |
| `--surface` | Card and table surface, section separators |
| `--text` | Primary text |
| `--text-muted` | Secondary text, captions, sources |
| `--accent` | Brand accent: section numbers, highlights, active states |
| `--accent-soft` | Accent at low opacity: hovers, row highlights |
| `--border` | Card and table borders |
| `--header-bg` | Table header background |
| `--header-text` | Table header text |
| `--positive` | Full or favourable indicator |
| `--warning` | Partial, optional, or watch-out indicator |
| `--negative` | Absent or unfavourable indicator |

A brand source that supplies fewer tokens is completed from the neutral fallback, token by token. Do not drop a token.

---

## 3. Logo handling

- `branding.logo_path` set: inline the file as a base64 `data:` URI so the report stays a single self-contained file.
- Not set: render no logo block at all. Do not draw a placeholder, a frame, or a text substitute. An empty brand slot costs credibility.
- Never fetch a logo from the web, and never reuse a logo from a previous mission's outputs.

---

## 4. Neutral fallback tokens

Brand-free defaults. Readable, printable, and unmistakably generic so a missing charter is visible rather than faked.

```css
:root {
  --font-title: system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-body:  system-ui, -apple-system, "Segoe UI", sans-serif;
  --bg:           #FFFFFF;
  --surface:      #F5F6F8;
  --text:         #16181D;
  --text-muted:   #5A6069;
  --accent:       #2D6CDF;
  --accent-soft:  rgba(45,108,223,0.08);
  --border:       #E3E6EA;
  --header-bg:    #16181D;
  --header-text:  #FFFFFF;
  --positive:     #1F8A4C;
  --warning:      #B5761B;
  --negative:     #B3261E;
}
```

---

## 5. Phase 0 detection

At Step 0.1, in the same pass as scraper detection:

1. Read `branding` from an existing mission-config if the mission is being resumed.
2. Otherwise check whether a brand skill is available in the environment, then whether the project holds a token file (`brand-tokens.*`, `design-tokens.*`, a charter file in `sources/`).
3. State the outcome in the mission brief, one line:
   - resolved by skill: "Charte : [skill name]"
   - resolved by token file: "Charte : [path]"
   - fallback: "Charte : palette neutre (aucune charte fournie)"
