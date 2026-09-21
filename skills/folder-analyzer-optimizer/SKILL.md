---
name: folder-analyzer-optimizer
description: >
  Transforme un dossier de documents heterogenes (PDF, DOCX, PPTX, XLSX) en
  knowledge base Markdown navigable (LLM Wiki pattern, Karpathy). Pipeline
  hybride zero-token (PyMuPDF, python-docx, python-pptx) avec mode
  incremental et arbre intra-document optionnel pour les gros fichiers
  (>= 50 pages). Use this skill proactively whenever the user mentions a
  data room, due diligence corpus, ESG/B Corp documentation review, VDD
  bundle, M&A dataroom, audit folder, client documentation review, or any
  need to navigate a folder of mixed-format documents efficiently — even if
  they don't use the words "parse" or "index". Trigger phrases include:
  "Analyse ce dossier", "Parse les documents", "Cree un miroir markdown",
  "Met a jour le parsing", "Refresh the parsed files", "Index the folder",
  "Scan this directory", "Prepare the data room", "Build a knowledge base
  from this folder", "Set up the document corpus".
---

# Folder Analyzer & Optimizer

Skill generique de conversion documentaire. Transforme n'importe quel dossier de documents en **knowledge base LLM-navigable** : miroir Markdown individuel par document + index hierarchiques par dossier (LLM Wiki pattern, Karpathy).

Fonctionne pour tout domaine : ESG/B Corp, legal, M&A, audit, RH, due diligence, etc.

Pipeline hybride PyMuPDF/python-docx/pptx valide en production : 85-95% de reduction de tokens vs Read-tool-only.

## Principe LLM Wiki (Karpathy)

Trois couches :
1. **Sources brutes** — documents originaux, jamais modifies
2. **Wiki** — pages Markdown individuelles (document.md) + index de dossier (_index.md)
3. **Schema** — CLAUDE.md du projet, configure les mappings metier

Navigation : lire `_index.md` racine → aller au sous-dossier pertinent → lire le document cible.
**Tous les fichiers sont visibles dans les index**, meme ceux non parsables (images, .doc legacy) : rien n'est invisible dans la knowledge base.

### Navigation intra-document via arbre

Pour les documents longs (≥ 50 pages) avec une structure exploitable (TOC native ou headings clairs), un **arbre JSON sidecar** est généré à côté du `.md` : `document.tree.json`. Cet arbre, inspiré de PageIndex (Vectify AI) mais porté en zero-token, contient les sections du document avec leurs plages de pages et un aperçu de 300 caractères par nœud.

L'agent navigue ainsi :
1. `_parsed/_index.md` racine → choisit le dossier
2. `_parsed/dossier/_index.md` → voit la section "Documents structurés" avec l'aperçu des chapitres des gros documents
3. Lit le `.md` ciblé sur la plage de pages identifiée — pas la totalité du document

Voir Step 6.5 pour les détails.

## Deux modes d'invocation

| Mode             | Declencheur                                                  | Comportement                                                        |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------------- |
| **Full scan**    | "Analyse ce dossier" (premiere execution ou pas de manifest) | Parse tout depuis zero                                              |
| **Incremental**  | "Met a jour le parsing" / "Refresh" (manifest existe deja)   | Detecte changements, ne re-parse que les fichiers nouveaux/modifies |
| **Force rescan** | "Force un rescan complet"                                    | Ecrase le manifest et re-parse tout                                 |

Le mode incremental est le **mode par defaut** quand un `_parse_manifest.json` existe deja.

## Domain mapping (optionnel)

Le skill accepte un `domain_mapping` : dictionnaire `{nom_dossier: [tags]}` injecte dans les index.

Exemple B Corp V7 :
```python
DOMAIN_MAPPING = {
    "Gouvernance": ["PSG1-5", "FR1-3", "GACA1-2"],
    "Collaborateurs": ["FW1-2", "JEDI1-2", "HR1"],
    "Environnement": ["ESC2", "ESC5", "CA2", "CA3"],
    "Clients": ["PSG4"],
}
```

Si fourni, chaque `_index.md` affiche les tags correspondants. Si non fourni, les index sont generes sans enrichissement metier.

## Output

```text
{project_root}/
+-- _parsed/
    |-- _parse_manifest.json    # Manifest JSON: etat de parsing + tree_* fields
    |-- _inventory.md           # Inventaire tabullaire + table de navigation par dossier
    |-- _index.md               # ROOT INDEX: navigation vers tous les sous-dossiers
    |-- subfolder_A/
    |   |-- _index.md           # INDEX: liste tous les fichiers (parsés + non-parsés)
    |   |-- document1.md        # Miroir Markdown du document original
    |   |-- document1.tree.json # Arbre sidecar (si document1 >= 50p et structuré)
    |   +-- document2.md
    +-- subfolder_B/
        |-- _index.md
        +-- report.md
```

---

## Step 0: Dependency check and install

Before any parsing, verify that the required Python packages are installed. If any are missing, ask the user for confirmation before installing.

```python
import subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # Windows fix

REQUIRED = {
    "pymupdf": "pymupdf>=1.27.0",
    "docx": "python-docx>=1.1.0",
    "pptx": "python-pptx>=1.0.0",
}

missing = []
for import_name, pip_name in REQUIRED.items():
    try:
        __import__(import_name)
    except ImportError:
        missing.append(pip_name)

if missing:
    print(f"Missing dependencies: {', '.join(missing)}")
    # Ask user confirmation before installing
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
    print("Dependencies installed successfully.")
else:
    print("All dependencies available.")
```

**Package roles**:

| Package                 | Import name | Role                                                                                    |
| ----------------------- | ----------- | --------------------------------------------------------------------------------------- |
| `pymupdf` (>=1.27.0)    | `pymupdf`   | Primary PDF text/table extractor + pre-analysis (image/word counting) + PNG conversion for Read tool |
| `python-docx` (>=1.1.0) | `docx`      | DOCX extraction (paragraphs, tables, headings)                                          |
| `python-pptx` (>=1.0.0) | `pptx`      | PPTX extraction (slides, text frames, tables, notes)                                    |

---

## Step 1: File discovery and pre-analysis

### 1a. Identify the source folder

The source folder is either:

- Explicitly provided by the user: "Analyse le dossier X"
- The current project root (if the user says "Analyse ce dossier")
- Auto-discovered from CLAUDE.md or project structure

### 1b. Recursive file listing

List all files in the source folder recursively. For each file, classify by extension:

| Extension                               | Action                                                                        |
| --------------------------------------- | ----------------------------------------------------------------------------- |
| `.pdf`                                  | PyMuPDF pre-analysis -> classification -> routing (Step 2)                    |
| `.docx`                                 | python-docx extraction                                                        |
| `.pptx`                                 | python-pptx extraction                                                        |
| `.xlsx`, `.xls`                         | Inventory only (sheet names, column headers, row counts). NOT text extraction |
| `.doc`                                  | SKIP_LEGACY_FORMAT. Alert user: "Convert to .docx for parsing"                |
| `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg` | SKIP_IMAGE. Note as "visual asset" in inventory                               |
| `.md`, `.txt`                           | Copy directly (already text/markdown). Include in inventory                   |
| `.json`                                 | Extract top-level keys and structure. Include in inventory                    |
| `.csv`                                  | Read first 5 rows as preview. Include in inventory                            |
| Other                                   | SKIP_UNSUPPORTED. Log in manifest                                             |

### 1c. PDF pre-analysis (PyMuPDF, ~0.3s per file)

For every PDF file, run PyMuPDF pre-analysis to count images and words per page:

```python
import pymupdf

def preanalyze_pdf(file_path):
    doc = pymupdf.open(str(file_path))
    page_count = len(doc)
    total_images = 0
    total_words = 0
    page_details = []

    for page_num in range(page_count):
        page = doc[page_num]
        text = page.get_text("text")
        images = page.get_images()
        words = len(text.split())
        total_images += len(images)
        total_words += words
        page_details.append({
            "page": page_num + 1,
            "words": words,
            "images": len(images)
        })

    doc.close()

    avg_images = total_images / page_count if page_count > 0 else 0
    avg_words = total_words / page_count if page_count > 0 else 0

    if avg_words < 10:
        classification = "SCANNED"
    elif avg_images < 25 and total_images < 1500 and avg_words > 100:
        classification = "TEXT-HEAVY"
    else:
        classification = "MIXED"

    image_heavy_pages = [p["page"] for p in page_details
                         if p["images"] >= 3 and p["words"] < 150]

    return {
        "page_count": page_count,
        "total_images": total_images,
        "total_words": total_words,
        "avg_images_per_page": round(avg_images, 2),
        "avg_words_per_page": round(avg_words, 2),
        "classification": classification,
        "image_heavy_pages": image_heavy_pages
    }
```

**Classification thresholds** (optimized — validated on 126-file autoresearch dataset + 90-file scanned corpus):

| Classification | Condition                                                          | Rationale                                                                      |
| -------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| SCANNED        | avg_words < 10                                                     | Image-based / scanned PDF. Text extraction returns nothing. Route directly to vision |
| TEXT-HEAVY     | avg_images < 25 AND total_images < 1500 AND avg_words > 100       | PyMuPDF extracts text+tables for free. Images are decorative                 |
| MIXED          | Everything else                                                    | PyMuPDF for text + Read tool only on visual-dominant pages                   |

**Smart MIXED page selection**: A page needs Read tool only if `images >= 3 AND words < 150`. Pages with enough text (>= 150 words) have annotations that describe the visual content. This reduces Read tool usage by 70-90% on large consulting decks (e.g., 437-page VDD: 43 pages instead of 437).

---

## Step 2: Extraction routing

Based on classification from Step 1, route each file to the appropriate extractor.

### Routing matrix (summary)

| Classification | Extractor                                      | Tokens                        | Speed      |
| -------------- | ---------------------------------------------- | ----------------------------- | ---------- |
| SCANNED        | Read tool vision (all pages)                   | ~700 x N_pages                | ~2s/page   |
| TEXT-HEAVY     | PyMuPDF (text extraction)                      | 0                             | ~0.1s/doc  |
| MIXED          | PyMuPDF (text) + Read tool (visual-dominant pages) | ~700 x N_visual_pages     | varies     |
| DOCX           | python-docx                                    | 0                             | ~0.5s      |
| PPTX           | python-pptx                                    | 0                             | ~0.5s      |

**Decision rule**: Route to SCANNED first (avg_words < 10), before attempting any free extractor. Running PyMuPDF text extraction on a scanned PDF wastes time and produces PARTIAL status with 0 words — a silent failure.

**Detailed implementation, code, and edge cases**: see [references/pdf-routing.md](references/pdf-routing.md).

---

## Step 3: Manifest management

The manifest file `_parsed/_parse_manifest.json` is the single source of truth for parsing state. It tracks every file, its status, extractor used, classification, and cache metadata.

See `examples/sample_manifest.json` for a complete example.

Key manifest fields: `source_path`, `output_path`, `mtime`, `parsed_at`, `page_count`, `word_count`, `status` (OK/PARTIAL/FAILED/SKIP_*), `extractor`, `routing_classification`, `preanalysis`, `error`, `tree_status`, `tree_path`, `tree_generated_at`.

Save manifest after **each file** (crash resilience). Use `mtime` comparison for cache invalidation.

**Detailed schema table, cache invalidation code, and crash resilience**: see [references/manifest-schema.md](references/manifest-schema.md).

---

## Step 4: Quality gates

After extraction, calculate average words per page and assign a quality status:

| Status  | Condition                   | Meaning                                                                                           |
| ------- | --------------------------- | ------------------------------------------------------------------------------------------------- |
| OK      | avg >= 50 words/page        | Full extraction, reliable content                                                                 |
| PARTIAL | avg 1-49 words/page         | Some content extracted but may be incomplete (scanned pages, image-heavy pages without Read tool) |
| FAILED  | 0 words OR extraction error | No usable content. File logged in manifest with error message                                     |

**FAILED files do NOT block the pipeline.** They are logged in the manifest and reported in the inventory. The user can manually review or provide alternative formats.

### Mandatory vision fallback check (post-extraction)

After the initial extraction pass, **always** inspect the PARTIAL distribution before declaring success:

```python
partials = [(k, v) for k, v in manifest["files"].items() if v.get("status") == "PARTIAL"]
near_zero = [p for p in partials if p[1].get("word_count", 0) <= 10]

if near_zero:
    pct = len(near_zero) / max(len(partials), 1) * 100
    print(f"WARNING: {len(near_zero)} PARTIAL files have word_count <= 10 ({pct:.0f}% of partials)")
    print("These are likely scanned/image-based PDFs. Applying Read tool vision fallback.")
    # → Re-route through Step 2a (SCANNED route) for all near_zero files
```

**Alert triggers** — investigate immediately if any of these are true after a full scan:
- More than 20% of PDFs are PARTIAL
- Any PARTIAL file has `word_count <= 10` (near-zero = scanned, not partial)
- Full scan completed faster than 1 file/second on average (speed anomaly = no real content)
- Median word count across PARTIAL files < 20

---

## Step 5: Inventory generation

Generate `_parsed/_inventory.md` — vue tabullaire complète regeneree a chaque run (full ou incremental).

### Inventory format

Sections: **Navigation LLM Wiki** (table of folders → `_index.md` links with parsed/total counts + domain tags), **Resume** (counts by type: PDF/DOCX/PPTX/XLSX/images/.doc), **Inventaire tabullaire** (row per file: #, path, type, status, word count).

Header metadata: Source path, scan date, mode (Full scan / Incremental with N new/modified/deleted), duration.

---

## Step 6: LLM Wiki — hierarchical folder indexes

**Generer un `_index.md` pour CHAQUE dossier** (y compris racine et sous-dossiers intermediaires). C'est la couche de navigation centrale de la knowledge base.

### Principe

Chaque `_index.md` contient :
1. Les **sous-dossiers directs** avec liens vers leurs propres `_index.md` et comptage fichiers
2. Les **fichiers directs** du dossier, groupes en deux sections :
   - **Parsés** : lien vers le `.md` + metadata (pages, mots, statut)
   - **Non parsés (référence)** : nom + raison du skip — **visibles, jamais omis**
3. Les **tags metier** si `domain_mapping` fourni

### Regle critique : visibilite totale

**Tout fichier presente dans le dossier source doit apparaitre dans l'index**, quel que soit son statut. Un fichier `SKIP_IMAGE` ou `SKIP_LEGACY_FORMAT` reste visible avec son label. L'objectif est qu'une personne (ou un LLM) lisant l'index ait une vue exhaustive du contenu du dossier source, y compris les elements non accessibles en texte.

### Format _index.md

````markdown
# [Dossier] — Index

**Standards/tags** : [tags metier si domain_mapping fourni]

*Index genere le [date]*

---

## Documents structurés
<!-- Section incluse UNIQUEMENT si au moins un document du dossier a un .tree.json -->

### [filename.pdf] — [doc complet]([filename.md]) · [arbre]([filename.tree.json])
*N p. | N,NNN mots | structure [pymupdf_toc|markdown_regex_headings|chunked]*

- **[Section niveau 1]** *(p. X-Y)* — [preview 80 caractères…]
  - [Section niveau 2] *(p. X-Y)*
  - [Section niveau 2] *(p. X-Y)*

---

## Sous-dossiers

- [SubA/](_parsed/SubA/_index.md) — N/M docs parsés [— Tags: X, Y]
- [SubB/](_parsed/SubB/_index.md) — N/M docs parsés

## Documents

### Parsés

- [rapport.pdf](_parsed/dossier/rapport.md) — 12p | 3,200 mots
- [contrat.docx](_parsed/dossier/contrat.md) — 850 mots *(extraction partielle)*

### Non parsés (référence)

> Ces fichiers existent dans le dossier source mais n'ont pas été parsés en texte.
> Ils sont listés ici pour que la knowledge base soit exhaustive.

- `photo_equipe.jpg` — **[IMAGE .JPG]** *(asset visuel — non parsé)*
- `ancien_contrat.doc` — **[LEGACY .DOC]** *(non parsé — convertir en .docx)*
- `export.eml` — **[FORMAT NON SUPPORTÉ .EML]**
````

### Règles de rendu de la section "Documents structurés"

- **Inclusion** : section affichée seulement si au moins un fichier du dossier a un `tree_status ∈ {OK, DEGRADED, FORCED_CHUNKED}`.
- **Niveau 1** : toujours montré, preview tronqué à 80 caractères inline (suffixe `…`).
- **Niveau 2** : toujours montré (`max_depth_in_index_md` = 2 par défaut), sans preview.
- **Niveau 3+** : non affichés dans `_index.md`. L'agent ouvre le `.tree.json` directement pour les détails fins.
- **Cap visuel** : au-delà de 6 nœuds niveau 1, n'afficher que les 6 premiers + `*(+ N sections de niveau 1)*`.
- **Badges** :
  - quality `DEGRADED` → suffixer le titre du doc par `*(structure partielle)*`
  - heading_extraction `chunked` → suffixer par `*(découpage par plages de pages)*`

L'implémentation Python utilise `render_structured_documents_section()` depuis `scripts/tree_builder.py` (cf. Step 6.5).

### Implementation Python (key functions)

```python
def write_folder_index(folder_rel, all_folders, folder_contents, manifest, output_root, domain_mapping=None):
    """Generates _index.md for one folder: domain tags header, Documents structurés
    (calls render_structured_documents_section() from scripts/tree_builder.py),
    Sous-dossiers list, then Parsés / Non parsés file lists."""

def format_file_entry(file_key, entry) -> str:
    """Markdown list item for a file. Parsed: linked with page/word count metadata.
    Skipped/Failed: backtick name + SKIP_IMAGE/SKIP_LEGACY_FORMAT/FAILED label."""

def get_domain_tags(folder_str, domain_mapping) -> list:
    """Tags for a folder path by matching path parts against domain_mapping keys."""
```
### Incremental: regenerer tous les index

Les `_index.md` sont **toujours regeneres en totalite** a chaque run (full ou incremental), car l'ajout/suppression d'un fichier dans un dossier affecte son index. Cout negligeable (pur Python, zero tokens).

---

## Step 6.5 : Tree builder (intra-document navigation)

Pour chaque document de **≥ 50 pages** avec une **structure exploitable** (TOC native ou ≥ 5 headings de bonne qualité), génère un arbre JSON sidecar `document.tree.json`. Permet à l'agent de naviguer par section/plage de pages sans charger le `.md` complet.

**Zero-token strict** : aucun appel LLM. Toute la logique vit dans `scripts/tree_builder.py`.

### Configuration (summary)

```python
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

### Cascade d'extraction (summary)

1. **PyMuPDF TOC** — haute fiabilité si l'outline PDF est embarqué
2. **Markdown regex headings** — regex `^(#{1,4})\s+(.+)$` sur le `.md`, page inférée via `## Page N`
3. **Chunked fallback** — tranches de `chunk_pages` pages (opt-in via `force_chunked_tree`)

### Status → action

- **OK** — arbre affiché normalement dans `_index.md`
- **DEGRADED** — badge `*(structure partielle)*`
- **FORCED_CHUNKED** — badge `*(découpage par plages de pages)*`
- **SKIPPED_*** — pas d'arbre, doc reste en `### Parsés` classique

**Detailed implementation, pipeline code, quality gate, tree.json format, and performance**: see [references/tree-builder.md](references/tree-builder.md).

---

## Incremental mode (default when manifest exists)

On every invocation, compare folder state with manifest:

| Condition                             | Classification | Action                                         |
| ------------------------------------- | -------------- | ---------------------------------------------- |
| File on disk, not in manifest         | NEW            | Parse (full pipeline)                          |
| File on disk, mtime > manifest.mtime  | MODIFIED       | Re-parse (full pipeline, overwrite .md)        |
| File on disk, mtime == manifest.mtime | UNCHANGED      | Skip (use cached .md)                          |
| File in manifest, not on disk         | DELETED        | Remove .md from _parsed/, remove from manifest |

**Lazy upgrade**: entries without `tree_status` field auto-generate `.tree.json` on next run — zero tokens, zero re-parse.

**Detailed change detection logic, tree behavior in incremental mode, workflow, and report format**: see [references/incremental-mode.md](references/incremental-mode.md).

---

## Error handling

| Error                                           | Impact    | Action                                                              |
| ----------------------------------------------- | --------- | ------------------------------------------------------------------- |
| PyMuPDF extraction exception on a specific page | One file  | Log partial result for that page, continue with remaining pages. Do NOT mark as FAILED |
| PyMuPDF cannot open file (encrypted, corrupted) | One file  | Log as FAILED in manifest with error message. Continue to next file |
| Read tool fails on a PNG page                   | One page  | Log warning. Use PyMuPDF text for that page instead                 |
| python-docx/pptx exception                      | One file  | Log as FAILED in manifest. Continue                                 |
| pip install fails                               | All files | Stop and ask user to install manually                               |

**Principle**: Never let a single file failure block the entire pipeline. Log the error, continue, report at the end.

**Full error table (13 entries including tree builder errors)**: see [references/error-handling.md](references/error-handling.md).

---

## Validation rules

- Every file in the source folder MUST appear in the manifest (100% coverage)
- Every OK/PARTIAL file MUST have a corresponding .md in `_parsed/`
- The manifest MUST be saved after each file (crash resilient)
- FAILED files MUST have an error message in the manifest
- The inventory MUST be regenerated on every run (not stale)
- Source paths in manifest MUST be absolute paths
- Output paths in manifest MUST be relative to project root
- .md files MUST start with the metadata header comment
- Every file with `tree_status ∈ {OK, DEGRADED, FORCED_CHUNKED}` MUST have a corresponding `.tree.json`
- Every `.tree.json` MUST have a corresponding `.md` (1:1 coupling)
- The mtime of `.tree.json` MUST be ≥ mtime of the source file (otherwise: stale, regenerate next run)
- Every node MUST have `start_page` and `end_page` in `[1, page_count]`
- Every node MUST have `end_page >= start_page`
- Every node `preview` MUST be ≤ `preview_chars` configured
- Every `node_id` MUST be unique within the tree
- Every node `level` MUST be ≥ 1

---

## Performance expectations

| Folder size | Full scan   | Incremental (5 changes) |
| ----------- | ----------- | ----------------------- |
| 10 files    | ~30 seconds | ~5 seconds              |
| 50 files    | ~3 minutes  | ~15 seconds             |
| 100 files   | ~6 minutes  | ~20 seconds             |

PyMuPDF text extraction handles ~90% of PDFs in seconds (zero tokens). Smart MIXED routing reduces Read tool usage by 70-90%. Token budget: ~700 tokens/Read tool page; 88% reduction vs naive routing (~137K tokens for a 126-file data room vs ~1.1M). Tree builder: ~120 ms, 0 tokens per eligible doc; ~2.5 s overhead for a 200-file data room with 20 eligible docs.
