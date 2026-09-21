# Design Spec: Auto-optimisation du Folder Analyzer (pattern autoresearch)

**Date**: 2026-03-31
**Auteur**: Yannick Bottino + Claude
**Statut**: Approuve
**Approche**: C — Hybride template detection + boucle d'optimisation

---

## Objectif

Reduire au maximum la consommation de tokens de Claude lors du parsing d'un dossier de documents, a qualite constante. Le dataset de reference est `Base documentaire/` (125 fichiers, dont 109 PDFs).

## Contraintes

- **20 experiences maximum** dans la boucle d'optimisation
- Le harness d'optimisation est **temporaire** — il sera supprime apres application des gains au SKILL.md
- Qualite mesuree par un **mix metriques proxy (0 tokens) + spot-check LLM (sur echantillon)**

---

## Architecture du harness (temporaire)

```
folder-analyzer-optimizer/
  SKILL.md                    # Skill existant (inchange pendant l'opti)
  program.md                  # Orchestrateur autoresearch (nouveau, temporaire)
  config.py                   # Parametres optimisables (nouveau, temporaire)
  baseline.py                 # Phase 1 : baseline + clustering (nouveau, temporaire)
  optimize.py                 # Phase 2 : boucle d'optimisation (nouveau, temporaire)
  evaluate.py                 # Metriques proxy + spot-check LLM (nouveau, temporaire)
  results.tsv                 # Log des experiences (non-tracke git)
  Base documentaire/          # Dataset de reference (existant)
  _baseline/                  # Outputs du run baseline (genere, temporaire)
    _parse_manifest.json
    _metrics.json             # Tokens, qualite, temps par fichier
    _clusters.json            # Templates detectes
  _optimized/                 # Outputs du meilleur run (genere, temporaire)
```

**Principe** : `program.md` = seul fichier edite par l'humain. `config.py` = seul fichier edite par l'agent.

---

## Phase 1 : Baseline & Clustering

### 1a. Baseline run

Executer le skill actuel sur les 125 fichiers. Metriques collectees (toutes a 0 tokens) :

| Metrique | Source |
|---|---|
| Classification PDF | PyMuPDF pre-analysis |
| Extractor utilise par fichier | Manifest |
| Word count du .md genere | `wc -w` sur l'output |
| Nombre de tableaux extraits | Regex sur le .md |
| Pages traitees via Read tool | Compteur pipeline |
| Tokens Read tool estimes | ~700 x nb pages Read tool |
| Temps d'extraction par fichier | Chrono Python |

Output : `_baseline/_metrics.json`

### 1b. Template clustering (0 tokens)

Pour chaque PDF, extraire un fingerprint structurel via PyMuPDF :
- Nombre de pages
- Dimensions des pages (A4 portrait vs paysage)
- Nombre d'images par page
- Positions des blocs de texte (bounding boxes via `page.get_text("dict")`)
- Premiers mots de chaque page (entetes de formulaire)

Clustering hierarchique par similarite de fingerprints.

Output : `_baseline/_clusters.json` avec par cluster :
- `id` : nom du template
- `count` : nombre de membres
- `representative` : fichier de reference (meilleur score qualite baseline)
- `members` : liste des fichiers du cluster

---

## Phase 2 : Boucle d'optimisation (max 20 experiences)

### Parametres optimisables (`config.py`)

```python
# Seuils de classification PDF
THRESHOLD_TEXT_HEAVY_MIN_AVG_WORDS = 150
THRESHOLD_TEXT_HEAVY_MAX_AVG_IMAGES = 1
THRESHOLD_TEXT_HEAVY_MAX_TOTAL_IMAGES = 5
THRESHOLD_IMAGE_HEAVY_MIN_AVG_IMAGES = 3
THRESHOLD_IMAGE_HEAVY_MAX_TOTAL_IMAGES = 15
THRESHOLD_IMAGE_HEAVY_MAX_AVG_WORDS = 80
THRESHOLD_SCANNED_MAX_AVG_WORDS = 10
THRESHOLD_SCANNED_MAX_TOTAL_WORDS = 50

# Read tool settings
DPI_FOR_PNG = 150
MAX_PAGES_PER_CHUNK = 20

# Template detection
TEMPLATE_ENABLED = True
SIMILARITY_THRESHOLD = 0.85
TEMPLATE_PARSE_MODE = "differential"  # "full" | "differential" | "skip_body"

# Output format
METADATA_HEADER = True
INCLUDE_PAGE_BREAKS = True
IMAGE_DESCRIPTION_DEPTH = "detailed"  # "detailed" | "summary" | "caption_only"
TABLE_FORMAT = "gfm"  # "gfm" | "compact" | "csv_inline"
```

### Subset representatif (~15 fichiers)

Selection automatique apres clustering :
- 1 representant par cluster (les plus gros clusters)
- 1 PDF text-heavy pur
- 1 PDF image-heavy
- 1 PDF MIXED
- 1 DOCX, 1 PPTX, 1 XLSX

### Boucle (calque autoresearch)

```
LOOP (max 20 iterations):
  1. Lire l'etat git (branch autoresearch/<tag>)
  2. Modifier config.py avec une hypothese experimentale
  3. git commit
  4. Executer optimize.py sur le subset (~15 fichiers) > run.log
  5. Lire resultats : grep "total_tokens|quality_score" run.log
  6. Si crash : tail -50 run.log, tenter fix, sinon skip
  7. Logger dans results.tsv :
     commit | total_tokens | quality_score | delta_vs_baseline | status | description
  8. Si total_tokens < meilleur ET quality_score >= seuil : KEEP
  9. Sinon : DISCARD (git reset)
```

### Exemples d'experiences

| # | Hypothese | Parametre modifie |
|---|---|---|
| 1 | Baseline sur subset | — |
| 2 | Baisser DPI 150 -> 100 | DPI_FOR_PNG = 100 |
| 3 | Relever seuil text-heavy | THRESHOLD_TEXT_HEAVY_MIN_AVG_WORDS = 100 |
| 4 | Activer parsing differentiel par template | TEMPLATE_ENABLED = True |
| 5 | Reduire profondeur description images | IMAGE_DESCRIPTION_DEPTH = "caption_only" |
| 6 | Combo DPI bas + template + caption_only | Multi |
| 7 | Format tableaux compact | TABLE_FORMAT = "compact" |

---

## Phase 3 : Evaluation

### Metriques proxy (chaque run, 0 tokens)

| Metrique | Seuil qualite |
|---|---|
| Word coverage ratio (words_opt / words_baseline) | >= 0.90 |
| Table count ratio | >= 0.95 |
| Heading count ratio | >= 0.90 |
| Zero-content files (< 10 mots) | 0 regressions |

### LLM spot-check (tous les 5 runs)

Sur 3 fichiers au hasard parmi les keep candidats :
- Claude lit le PDF original (Read tool) + le .md optimise
- Score de fidelite 1-5 (contenu, structure, donnees chiffrees)
- Score moyen < 3.5 : discard malgre proxy metrics

### Validation finale (apres les 20 experiences)

1. Identifier la meilleure config
2. Run complet sur les 125 fichiers
3. Spot-check LLM sur 10% (~12 fichiers)
4. Si OK : appliquer les gains au SKILL.md

---

## Cleanup post-optimisation

Apres application des gains au SKILL.md :
- Supprimer : program.md, config.py, baseline.py, optimize.py, evaluate.py
- Supprimer : _baseline/, _optimized/, results.tsv
- Le skill livre est propre : SKILL.md optimise + examples/
