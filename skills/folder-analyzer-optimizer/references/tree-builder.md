# Tree Builder Details
<!-- Loaded on demand by SKILL.md Step 6.5 -->

## Step 6.5 : Tree builder (intra-document navigation)

Pour chaque document de **≥ 50 pages** avec une **structure exploitable** (TOC native ou ≥ 5 headings de bonne qualité), génère un arbre JSON sidecar `document.tree.json` à côté de `document.md`. Permet à l'agent de naviguer dans le document par section/plage de pages sans charger le `.md` complet.

**Zero-token strict** : aucun appel LLM. Toute la logique vit dans `scripts/tree_builder.py`.

### Configuration

```python
from tree_builder import DEFAULT_TREE_CONFIG

TREE_CONFIG = {
    "enabled": True,
    "tree_threshold_pages": 50,
    "min_headings": 5,
    "max_depth_in_index_md": 2,
    "preview_chars": 300,
    "force_chunked_tree": False,
    "chunk_pages": 10,
}
```

Override possible via `CLAUDE.md` projet pour ajuster mission par mission.

### Pipeline

Pour chaque entrée du manifest avec `status ∈ {OK, PARTIAL}` :

```python
from pathlib import Path
from tree_builder import build_tree_for_file, DEFAULT_TREE_CONFIG

cfg = {**DEFAULT_TREE_CONFIG, **TREE_CONFIG_OVERRIDES}  # if any

for file_key, entry in manifest["files"].items():
    if entry.get("status") not in ("OK", "PARTIAL"):
        continue
    if entry.get("tree_status") is not None and not rebuild_trees:
        continue  # already processed, unless --rebuild-trees

    source_path = Path(entry["source_path"])
    md_path = output_root / entry["output_path"]
    page_count = entry.get("page_count") or 0

    status = build_tree_for_file(
        source_path=source_path,
        md_path=md_path,
        page_count=page_count,
        output_root=output_root,
        config=cfg,
    )
    entry["tree_status"] = status
    if status in ("OK", "DEGRADED", "FORCED_CHUNKED"):
        rel_tree = Path(entry["output_path"]).with_suffix(".tree.json").as_posix()
        entry["tree_path"] = str(rel_tree)
        entry["tree_generated_at"] = datetime.now().isoformat(timespec="seconds")
    else:
        entry["tree_path"] = None
        entry["tree_generated_at"] = None

save_manifest(manifest)  # crash-resilient, save after each file in production
```

### Cascade d'extraction des headings

| Source | Méthode | Force | Limite |
|---|---|---|---|
| **1. PyMuPDF TOC** | `doc.get_toc(simple=True)` retourne `[level, title, page]` | Haute fiabilité quand l'outline PDF existe | Absent si l'auteur n'a pas embarqué d'outline |
| **2. Markdown regex headings** | Regex `^(#{1,4})\s+(.+)$` sur le `.md`. Page inférée via le `## Page N` le plus proche en amont | Fonctionne sur tout `.md` produit en Step 2 | Qualité dépend de la conversion PyMuPDF |
| **3. Chunked fallback** | Tranches de `chunk_pages` pages | Toujours dispo | Opt-in (`force_chunked_tree: True`), sémantique pauvre |

### Quality gate

```python
def assess_tree_quality(headings, page_count):
    # OK         : >= 2 levels AND >= 8 headings AND coverage >= 10%
    # DEGRADED   : >= 5 headings AND coverage >= 5%
    # INSUFFICIENT: anything else (no tree emitted)
```

Mapping statut → action :
- **OK** → arbre affiché normalement dans `_index.md`
- **DEGRADED** → arbre affiché avec badge `*(structure partielle)*`
- **FORCED_CHUNKED** → arbre affiché avec badge `*(découpage par plages de pages)*`
- **SKIPPED_*** → pas d'arbre, doc reste en `### Parsés` classique

### Format du sidecar `.tree.json`

Voir `examples/sample_tree.json` pour un exemple complet. Schéma :

```json
{
  "source_path": "Contrats/SPA_v3.pdf",
  "md_path": "Contrats/SPA_v3.md",
  "page_count": 187,
  "heading_extraction": "pymupdf_toc",
  "quality": "OK",
  "generated_at": "2026-05-13T14:42:00",
  "tree": [
    {
      "node_id": "n1",
      "title": "...",
      "level": 1,
      "start_page": 5,
      "end_page": 18,
      "preview": "First 300 characters of the section body, headings and page anchors stripped.",
      "nodes": []
    }
  ]
}
```

### Performance attendue

| Opération | Coût |
|---|---|
| `pymupdf.get_toc()` sur PDF 200 p. | ~50 ms |
| Extraction headings markdown via regex | ~20 ms |
| Nest + injection page ranges + previews | ~40 ms |
| Écriture `.tree.json` | ~5 ms |
| **Total par doc éligible** | **~120 ms, 0 token** |

Pour un data room de 200 fichiers dont 20 éligibles : **~2.5 s, 0 token**.

### Désactivation

Si `TREE_CONFIG["enabled"] = False`, le Step 6.5 est strictement no-op. Aucun fichier `.tree.json` créé, aucune modification de `_index.md`, aucun champ `tree_*` ajouté au manifest.
