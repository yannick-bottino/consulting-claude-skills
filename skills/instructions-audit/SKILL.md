---
name: instructions-audit
description: >
  Use when a project CLAUDE.md exceeds 100 lines, contains bloated or misplaced
  sections, or has governance issues. Trigger phrases: "audit CLAUDE.md",
  "mon CLAUDE.md est trop long", "refactor CLAUDE.md", "nettoie le CLAUDE.md",
  "gouvernance contexte projet", "lean CLAUDE.md", "CLAUDE.md est obèse".
  Applies to project CLAUDE.md files only — NOT to ~/.claude/CLAUDE.md global.
---

# instructions-audit

## Objectif

Auditer un CLAUDE.md projet pour détecter le bloat, identifier les sections à
extraire vers `rules/` ou `skills/`, et produire une version lean ≤ 100 lignes.

Deux phases séquentielles. Phase 2 ne démarre qu'après validation de Phase 1.

## Phase 1 — Audit (toujours exécutée)

Utiliser le prompt complet dans `references/audit-prompt.md`.

Injecter le contenu du CLAUDE.md cible dans le placeholder
`[CONTENU DU CLAUDE.MD PROJET — injecté automatiquement par le skill]`.

Produire un rapport structuré en 5 sections :
1. **Diagnostic global** — lignes, tokens estimés (lignes × 4), verdict
   LEAN (<80L) / ACCEPTABLE (80-100L) / OBÈSE (101-150L) / CRITIQUE (>150L)
2. **Analyse par section** — pour chaque bloc : catégorie parmi les 6 types,
   verdict GARDER / EXTRAIRE VERS [fichier] / SUPPRIMER, justification 1 phrase
3. **Top 5 quick wins** — extractions triées par lignes gagnées décroissant
4. **Risques détectés** — contradictions, obsolescences, duplications, ambiguïtés
5. **Plan de refactor** — 5 étapes max, ordre d'opérations

**Après le rapport : attendre validation explicite avant Phase 2.**
> "Voici le rapport d'audit. Tu valides ce plan avant que je génère la version lean ?"

Ne pas poser de questions de clarification. Produire le rapport avec les informations
disponibles, puis attendre la validation.

## Phase 2 — Refactor (après validation Phase 1)

Utiliser le prompt complet dans `references/refactor-prompt.md`.

Injecter : (1) contenu CLAUDE.md original, (2) rapport de Phase 1.

Produire exactement ces 7 livrables — aucun raccourci, aucun placeholder :
1. Architecture cible (arborescence)
2. CLAUDE.md lean complet, prêt à coller (≤ 100 lignes)
3. Fichiers annexes — 3 à 6 fichiers max, contenu complet pour chacun
4. Commandes shell pour créer la structure
5. Changelog — table 3 colonnes : ancien emplacement → nouveau fichier → raison
6. Contenu supprimé — liste avec justification 1 ligne par item
7. Checklist post-refactor (5-10 vérifications)

**Règle absolue :** Si le CLAUDE.md lean dépasse 100 lignes, extraire davantage
avant de livrer. Ne pas rationaliser un dépassement même de quelques lignes.

## Erreurs fréquentes

- **Sauter Phase 1** : ne jamais proposer un refactor sans avoir produit le rapport d'audit structuré en 5 sections.
- **Poser des questions avant le rapport** : produire Phase 1 avec les infos disponibles, pas de questions de clarification préalables.
- **Livrables Phase 2 incomplets** : les 7 livrables sont obligatoires. Fichiers annexes avec contenu complet — jamais de "[à compléter]" ou "[contenu ici]".
- **Dépasser 100 lignes** : la cible est 100 lignes, pas "environ 100". Si dépassement, re-extraire.
- **Imposer le template WHY/WHAT/HOW sur un projet avec une structure établie** : le template est une suggestion, pas une obligation. Si le CLAUDE.md source a une structure propre et cohérente, la conserver.

## Intégrations

Peut être invoqué directement par `/project-lint` lorsque CLAUDE.md dépasse la cible de lignes.
