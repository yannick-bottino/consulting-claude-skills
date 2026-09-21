# MEMORY

## 2026-03-31 — Optimization complete

### Results
- **88% token reduction** validated on 126-file dataset (1,115,800 -> 137,200 estimated tokens)
- 10 experiments run (out of 20 budget), plateaued at experiment 9
- Harness removed, gains applied to SKILL.md

### Key changes to SKILL.md
1. **Classification thresholds relaxed**: avg_words > 100 + generous image thresholds -> TEXT-HEAVY (zero-token extractor, 0 tokens). Previously most PDFs were IMAGE-HEAVY.
2. **SCANNED and IMAGE-HEAVY categories eliminated**: replaced by smart MIXED
3. **Smart MIXED routing added**: Read tool only on pages with >= 3 images AND < 150 words (visual-dominant pages). 70-90% fewer Read tool calls on large consulting decks.

### Validation
- The zero-token PDF extractor in use at the time captured 94,866 words from a 437-page VDD — text extraction is comprehensive
- Visual-dominant page detection correctly targets chart/diagram pages
- Attestations thermiques (formulaires): the zero-token extractor captures all structured data, images are decorative

### Dataset used
- Base documentaire/ : 114 files (attestations thermiques RT2012/RE2020, XLSX, PPTX, DOCX)
- Base documentaire/Docs client/ : 12 files (VDD, bilans carbone, ESG reports — image-heavy consulting docs, from a past engagement)
