---
name: deck-slop-build
description: >
  Builds a slide deck, or writes the paste-in prompt for an external deck tool,
  under rules that keep it from reading as AI-made: titles first, data only from
  the brief, strongest tells avoided. Use when the user says "fais un deck",
  "fais des slides", "construis la prez", "prépare le deck pour le comité",
  "build the deck", "make the slides", "board deck", "prompt pour Gamma",
  "instructions pour Copilot", "custom instructions for my slide tool", or asks
  for a PPTX, Keynote, Google Slides, Gamma, Copilot or ChatGPT deck that will
  be shown to a client, a comité or a board. Never invents a number, a source or
  a case. To audit an existing deck, use deck-slop.
---

# Deck slop build

Construit un deck, ou rédige le prompt à coller dans l'outil de slides, avec les règles qui l'empêchent de trahir son outil IA.

## Étapes

```
Avancement :
- [ ] 1. Remplir le brief
- [ ] 2. Choisir la sortie
- [ ] 3. Écrire les titres
- [ ] 4. Construire et contrôler
```

### 1. Remplir le brief
Audience, décision ou demande attendue, données autorisées, couleurs et gabarit de marque, format de sortie. Ne rien supposer : chaque champ manquant est demandé à l'utilisateur ou laissé vide. Une donnée manquante dans le deck s'écrit `[DATA NEEDED: ...]` ou `[SOURCE NEEDED: ...]`.

### 2. Choisir la sortie
Si l'utilisateur construit dans un autre outil (Gamma, Copilot, ChatGPT), lui rendre le prompt de `references/prompt-a-coller.md`, dans la langue du deck, le brief rempli à la place du bloc vide, et s'arrêter là. Sans couleurs de marque, la règle 24 du prompt laisse l'outil choisir. Sinon, continuer.

### 3. Écrire les titres
Écrire tous les titres dans l'ordre, en phrases complètes qui disent la conclusion de chaque slide. Les montrer avant toute slide.

### 4. Construire et contrôler
Construire en appliquant chaque règle de `references/prompt-a-coller.md`, version de la langue du deck. Avant de livrer, repasser les cinq marqueurs révélateurs (règles 1 à 5 du prompt) sur chaque slide. Sans les pixels, écrire que les contrôles visuels ne sont pas vérifiés. Lister les placeholders restés vides.

## Points de contrôle humains
- Après l'étape 3 : attendre la validation des titres avant de construire.
- Avant l'étape 4, sans couleurs de marque : proposer 5 palettes (fond, texte, gris, accent), hors défauts crème et terracotta ou bleu nuit à accent vif, et attendre le choix.

## Auto-amélioration
Ce skill n'est jamais fini.
- Quand l'utilisateur corrige une slide ou une règle, mettre à jour `references/prompt-a-coller.md` (ou ce SKILL.md), dans les deux langues, pour que la correction tienne.
- Quand une correction est une règle ferme (« toujours », « jamais »), l'ajouter ici comme règle permanente.
- Quand l'utilisateur juge un deck ou un prompt bon, l'enregistrer dans `references/examples/` (créer le dossier la première fois).
- Après chaque ajout, refaire le test de suppression et couper ce qui ne change plus le comportement.

## Routage
| Étape | Référence |
|---|---|
| 2 et 4 | `references/prompt-a-coller.md` |
