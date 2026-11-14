---
name: deck-slop
description: >
  Audits an existing slide deck for the tells that make it read as AI-made, slide
  by slide, strongest tells first, and returns a scorecard. Use when the user says
  "audit my deck", "check the deck before I present", "de-slop the deck", "does
  this deck look AI-made", "mes slides font IA", "ça fait trop IA", "revue de
  slides", "relis mon deck", "audite la prez", or shares a PPTX, Keynote, Google
  Slides, Gamma, Copilot or ChatGPT deck that will be shown to a client, a comité
  or a board. Detects only, fixes only when asked. Never invents a number, a
  source or a case. To build a deck under the same rules, use deck-slop-build.
---

# Deck slop

Relève, slide par slide, les marqueurs qui font qu'un deck trahit son outil IA, et les nomme avec leur rang de signal.

## Étapes

```
Avancement :
- [ ] 1. Cadrer ce qui est visible
- [ ] 2. Passer les marqueurs, forts d'abord
- [ ] 3. Rendre le tableau
```

### 1. Cadrer ce qui est visible
Dire en une ligne si les slides sont vues en image ou seulement en texte. Sans les pixels, écrire que les contrôles visuels (dont les bourrages du marqueur 29) ne sont pas vérifiés, puis auditer quand même le texte et la structure.

### 2. Passer les marqueurs, forts d'abord
Lire `references/tells.md` et le passer bloc par bloc, dans l'ordre du fichier, sur chaque slide. Un marqueur faible, plus fréquent chez le réel ou non mesuré ne se présente jamais comme un signe de deck IA.

### 3. Rendre le tableau
La ligne de cadrage de l'étape 1, puis le tableau, trié par rang puis par slide. Une ligne par marqueur trouvé : slide, numéro et nom du marqueur, ce qui est en cause (citation ou zone décrite), rang, correctif proposé. Rien d'autre. Si rien ne se déclenche, l'écrire en une ligne : un passage propre est un résultat normal. Aucun tiret cadratin dans le compte rendu.

## Points de contrôle humains
- Ne jamais éditer le deck ni son texte sans demande explicite (« corrige », « applique »). Sur demande, appliquer le correctif de `references/tells.md`, sans inventer de chiffre ni de source : un trou s'écrit `[DATA NEEDED: ...]`.
- Si l'utilisateur conteste un rang, demande la source ou ce que l'audit couvre : lire `references/methode-et-limites.md`.

## Auto-amélioration
Ce skill n'est jamais fini.
- Quand l'utilisateur corrige un relevé, mettre à jour `references/tells.md` (ou ce SKILL.md) pour que la correction tienne, pas seulement pour ce passage.
- Quand une correction est une règle ferme (« toujours », « jamais »), l'ajouter ici comme règle permanente.
- Quand l'utilisateur juge un audit bon, l'enregistrer dans `references/examples/` (créer le dossier la première fois).
- Ne jamais modifier un rang ou un chiffre de comparaison sans le PDF source.
- Après chaque ajout, refaire le test de suppression et couper ce qui ne change plus le comportement.

## Routage
| Étape | Référence |
|---|---|
| 2, et correctifs sur demande | `references/tells.md` |
| Rang contesté, source, limites | `references/methode-et-limites.md` |
