# Incremental Mode
<!-- Loaded on demand by SKILL.md -->

## Incremental mode (default when manifest exists)

The source folder evolves over time: files added, modified, deleted. The skill detects changes automatically and only re-parses what changed.

### Change detection

On every invocation, compare current folder state with manifest:

| Condition                             | Classification | Action                                         |
| ------------------------------------- | -------------- | ---------------------------------------------- |
| File on disk, not in manifest         | NEW            | Parse (full pipeline)                          |
| File on disk, mtime > manifest.mtime  | MODIFIED       | Re-parse (full pipeline, overwrite .md)        |
| File on disk, mtime == manifest.mtime | UNCHANGED      | Skip (use cached .md)                          |
| File in manifest, not on disk         | DELETED        | Remove .md from _parsed/, remove from manifest |

### Comportement de l'arbre (Step 6.5) en incrémental

| Condition source | Action `.md` (existant) | Action `.tree.json` (Step 6.5) |
|---|---|---|
| NEW | Parse | Build tree si éligible |
| MODIFIED | Re-parse | Rebuild tree si éligible |
| UNCHANGED + `tree_status` absent du manifest | Skip | **Lazy upgrade** : build tree sans toucher au `.md` |
| UNCHANGED + `tree_status` présent | Skip | Skip |
| DELETED | Remove `.md` | Remove `.tree.json` |
| Flag `--rebuild-trees` | n/a | Régénérer tous les arbres sans re-parser les `.md` |

**Lazy upgrade** : au premier run après ajout de la feature, les entrées sans champ `tree_status` génèrent uniquement le `.tree.json` éligible. Zero token, zero re-parse.

### Incremental workflow

```text
1. Load _parse_manifest.json
2. List all files on disk (recursive)
3. Compare with manifest:
   - new_files:      on disk but not in manifest
   - modified_files:  mtime differs from manifest
   - deleted_files:   in manifest but not on disk
   - unchanged:       mtime matches (skip)
4. For deleted_files:
   - Delete corresponding .md from _parsed/
   - Remove entry from manifest
5. For new_files + modified_files:
   - Run normal pipeline (pre-analysis -> routing -> extraction)
   - Update manifest entries
   - Save manifest after EACH file (crash resilient)
6. Regenerate _inventory.md (always full, not incremental)
7. Print incremental diff report
```

### Incremental report format

```text
=== Incremental Update ===
Source: /path/to/folder
Changes detected: 5 new | 2 modified | 1 deleted | 38 unchanged

New files parsed:
  + policies/new_policy_v2.pdf       TEXT-HEAVY -> pymupdf, OK
                                     tree: SKIPPED_TOO_SHORT (12 pages)
  + contracts/addendum_2025.docx     python-docx, OK
                                     tree: SKIPPED_TOO_SHORT (3 pages)
  + reports/Q1_2025.pdf              IMAGE-HEAVY -> read_tool, OK (4200 tokens)
                                     tree: SKIPPED_TOO_SHORT (8 pages)
  + contrats/SPA_v4.pdf              TEXT-HEAVY -> pymupdf, OK
                                     tree: OK (pymupdf_toc, 47 nodes, 3 levels)
  + misc/photo.png                   SKIP_IMAGE

Modified files re-parsed:
  ~ policies/RGPD_v6.pdf             TEXT-HEAVY -> pymupdf, OK
                                     tree: SKIPPED_TOO_SHORT (18 pages)
  ~ contrats/SPA_v3.pdf              TEXT-HEAVY -> pymupdf, OK
                                     tree: OK (regenerated)

Trees auto-generated (lazy upgrade):
  → Memos/IM_2024.pdf                tree: OK (62 nodes)
  → Audit/VDD_financier.pdf          tree: OK (104 nodes)

Trees skipped:
  ~ Annexes/CV_team.pdf              tree: SKIPPED_TOO_SHORT (12 pages)
  ~ Scans/contrat_legacy.pdf         tree: SKIPPED_NO_STRUCTURE (avg_words=4)

Deleted files cleaned:
  - old/draft_proposal.pdf            removed from _parsed/ and manifest

Tokens consumed: 6,300 (new/modified Read tool pages only)
Duration: 14 seconds
Inventory updated: _parsed/_inventory.md
```
