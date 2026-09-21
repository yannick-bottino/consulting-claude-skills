# TODO — Auto-optimisation Folder Analyzer

## Phase 1 : Baseline & Clustering — DONE

- [x] Installer les dependances Python (pymupdf, python-docx, python-pptx)
- [x] Creer `baseline.py` — executer le skill sur les 125 fichiers, collecter metriques
- [x] Executer le baseline, generer `_baseline/_metrics.json`
- [x] Creer le module de clustering (fingerprint structurel PyMuPDF)
- [x] Executer le clustering, generer `_baseline/_clusters.json`
- [x] Selectionner le subset representatif (~15 fichiers) a partir des clusters

## Phase 2 : Harness d'optimisation — DONE

- [x] Creer `config.py` avec les parametres optimisables
- [x] Creer `evaluate.py` — metriques proxy + spot-check LLM
- [x] Creer `optimize.py` — pipeline de parsing parametre par config.py
- [x] Creer `program.md` — instructions agent pour la boucle autoresearch
- [x] Initialiser `results.tsv` avec le header

## Phase 3 : Boucle d'optimisation — DONE (10/20 experiences)

- [x] Experience 1 : baseline sur subset (138,600 tokens)
- [x] Experiences 2-10 : iterations autonomes -> 99.5% reduction sur subset
- [x] Test sur dataset etendu avec docs d'un past engagement (126 fichiers)
- [x] Spot-check zero-token extractor vs Read tool sur TARGETCO VDD (437 pages)
- [x] Conception du Smart MIXED routing (images >= 3 AND words < 150)

## Phase 4 : Validation & Application — DONE

- [x] Quantifier impact Smart MIXED : 88% reduction totale (1,115,800 -> 137,200 tokens)
- [x] Appliquer les gains au SKILL.md (seuils + smart MIXED + suppression SCANNED/IMAGE-HEAVY)
- [x] Supprimer le harness
- [x] Valider le SKILL.md final

## 2026-05-13 — PageIndex tree integration

- [x] Spec: docs/2026-05-13-pageindex-tree-integration-design.md
- [x] Plan: docs/2026-05-13-pageindex-tree-integration-plan.md
- [x] tree_builder.py + 39 tests
- [x] examples/sample_tree.json, sample_index_with_trees.md
- [x] SKILL.md sections (Output, Principe LLM Wiki, Step 3, Step 6, Step 6.5, Incremental, Error handling, Validation, Performance)
- [ ] Real-world validation on M&A data room (next mission)
- [ ] Real-world validation on B Corp dossier with long DPEF report (next mission)
