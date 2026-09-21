# Folder Analyzer Optimizer

## Projet

Optimisation du skill `folder-analyzer-optimizer` pour reduire la consommation de tokens de Claude lors du parsing de dossiers documentaires, a qualite constante.

## Objectif actuel

Construire un harness d'auto-optimisation inspire du pattern autoresearch (Karpathy) :
- Boucle autonome qui itere sur les parametres du pipeline de parsing
- Mesure tokens consommes + qualite du parsing sur un dataset de reference
- Keep/discard chaque experience, log dans results.tsv
- Max 20 experiences

## Dataset de reference

`Base documentaire/` — 125 fichiers :
- 109 PDFs (majoritairement attestations thermiques RT2012/RE2020)
- 12 XLSX
- 2 PPTX
- 1 DOCX
- 1 .msg

## Approche

**Hybride : template detection + boucle d'optimisation** (approche C du design)

### Phase 1 : Baseline & Clustering
- Parser les 125 fichiers avec le skill actuel, instrumenter tokens + qualite
- Clusterer les PDFs par template (fingerprint structurel via PyMuPDF, 0 tokens)

### Phase 2 : Boucle autoresearch (max 20 iterations)
- Agent modifie `config.py` (seuils, DPI, routing, template detection, format output)
- Execute `optimize.py` sur un subset representatif (~15 fichiers)
- Mesure delta tokens vs baseline, verifie qualite (proxy metrics + spot-check LLM)
- Keep/discard, log dans results.tsv

### Phase 3 : Validation & Cleanup
- Run complet sur 125 fichiers avec la meilleure config
- Spot-check LLM sur 10%
- Appliquer gains au SKILL.md
- Supprimer tout le harness d'optimisation

## Spec detaillee

`docs/2026-03-31-autoresearch-optimization-design.md`

## Contraintes

- Le harness est temporaire — supprime apres optimisation
- Qualite = mix metriques proxy (0 tokens) + spot-check LLM (echantillon)
- Le SKILL.md existant n'est pas modifie pendant l'optimisation, seulement a la fin
- `program.md` = edite par l'humain. `config.py` = edite par l'agent. Rien d'autre

## Stack technique

- Python 3 : pymupdf, python-docx, python-pptx
- Metriques proxy : word count, table count, heading count (0 tokens)
- Clustering : fingerprint structurel PyMuPDF + similarite (0 tokens)
