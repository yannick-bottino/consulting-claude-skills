---
name: deck-slop
description: >
  Quality gate and build rules for slide decks that must not read as AI-made.
  Use when the user says "fais un deck", "fais des slides", "construis la prez",
  "build the deck", "slide deck", "board deck", "mes slides font IA", "ça fait
  trop IA", "audit my deck", "check the deck before I present", "revue de slides",
  "de-slop the deck", "rends ce deck plus humain", or produces a PPTX, Keynote,
  Google Slides, Gamma, Copilot or ChatGPT deck that will be shown to a client,
  a comité, or a board. Two modes: BUILD (rules applied while generating the
  deck) and AUDIT (scorecard of the tells found, slide by slide). Detects first,
  fixes only when asked. Never invents a number, a source or a case.
---

# Deck slop

Un deck sur trois environ trahit son outil avant la deuxième slide. Ce skill sert à l'éviter quand tu construis le deck, et à le dire quand tu le relis.

Le guide d'origine, *Remove the AI slop from your decks* (Analyst Academy, Paul Moss, novembre 2026), compare cent slides produites par dix-sept outils IA à cent slides réelles de vingt-trois cabinets, banques et instituts. Il en sort cinq marqueurs forts, et trente et un correctifs. Les règles ici sont reformulées, la source n'est pas recopiée : voir `references/methode-et-limites.md`.

## Ce qui est diagnostique, et ce qui ne l'est pas

Confondre les deux est l'erreur principale. Un deck réel utilise souvent plus qu'un deck IA les icônes en cercle, l'accent color, les mots en gras, les cartes flottantes et les règles de type par défaut. Signaler ces points comme « fait IA » est faux.

| Rang | Signaux | Ce qu'on en fait |
|---|---|---|
| Diagnostique | 1. Quelque chose au-dessus du titre (surtitre, eyebrow en capitales, fil d'Ariane, pastille). 2. Bandeau de bas de slide ou encadré « key takeaway ». 3. Bande de couleur pleine hauteur sur un bord. | À corriger systématiquement, ce sont eux qui donnent le deck |
| Diagnostique | Bourrages de production : texte qui chevauche, déborde de son cadre ou de la slide, gabarit resté en placeholder, mot coupé par un retour à la ligne, chiffre du titre qui contredit le graphique | À corriger, et à vérifier slide par slide à la main |
| Moyen | Phrases de même forme (titres à deux-points, pivots en tiret cadratin), listes en trois par habitude, mots creux (*unlock, elevate, delve, leverage, seamless*), gravité gonflée, centrage de tout | À corriger, l'effet est réel mais plus faible |
| Faible | Cases arrondies à liseré coloré, barre d'accent au-dessus ou sous le titre, sous-titre en phrase entière sur la couverture, poids visuel uniforme, police par défaut, ombres et cartes flottantes, accent partout, palettes par défaut, pastilles et badges, tuiles de chiffres façon dashboard, grille de trois icônes, images abstraites, murs de puces | Correctif recommandé, jamais présenté comme une preuve de deck IA |
| Non mesuré | Même gabarit sur toutes les slides, fin en « perspectives » | Correctif recommandé, aucune donnée de comparaison |

Le détail des trente et un marqueurs, avec le correctif et le test de chaque, est dans `references/tells.md`. Le contexte de mesure et ses limites, dont la liste des marqueurs où les decks réels font pire que les decks IA, est dans `references/methode-et-limites.md`.

## Mode BUILD, construire un deck

Appliquer dans cet ordre, l'ordre compte.

1. **Le récit avant les slides.** Écrire tous les titres en phrases complètes, dans l'ordre, et les montrer avant de construire quoi que ce soit. Si les titres lus à la suite racontent l'argument, le deck est bon. Si un titre est un label (« Overview », « Key insights », « Prochaines étapes », « Contexte »), il n'apporte rien et sera le premier défaut visible.
2. **La matière avant la forme.** Le deck n'utilise que les chiffres, sources, audiences et objectifs fournis. Ce qui manque s'écrit `[DATA NEEDED: ...]` ou `[SOURCE NEEDED: ...]`, jamais une estimation plausible.
3. **Une idée par slide, un élément dominant.** Un chiffre, un graphique ou une phrase gagne, le titre est nettement plus gros que le corps, tout le reste est démotionné.
4. **La structure de la slide.** Le titre d'abord, rien au-dessus. Pas de bandeau bas, pas de bande latérale, pas de barre d'accent. Corps aligné à gauche, centrage réservé à un chiffre seul ou une citation courte.
5. **La forme.** Une police, regular et gras seulement, trois ou quatre tailles utilisées pareil partout. Une palette choisie : un fond, un texte, un gris, un accent qui ne sert qu'à désigner ce qui compte. Pas de dégradé, pas de lueur, pas de glassmorphism, pas d'ombre, pas de carte, pas de pastille.
6. **Le graphique.** Titre en phrase qui dit ce que le graphique prouve, grille minimale, contexte en gris, accent sur le point à voir, une annotation courte sur ce qu'il faut regarder.
7. **La sortie.** Terminer sur la décision ou la demande, avec une échéance. Pas de slide « enjeux et perspectives ».

Les règles complètes, avec les interdits de vocabulaire en français et en anglais, sont dans `references/tells.md`. Le prompt à coller dans l'outil est dans `references/prompt-a-collers.md`.

## Mode AUDIT, relire un deck

Pour un deck existant, ou pour s'auto-contrôler avant de livrer.

1. **Passer la checklist** `references/checklist.md`, slide par slide, en commençant par les signaux diagnostiques.
2. **Rendre un tableau** : numéro de slide, marqueur, ce qui est exactement en cause (citation ou description de la zone), rang du signal, correctif proposé. Rien d'autre.
3. **Ne pas éditer** le deck ni le texte sans demande explicite (« corrige », « applique »). Le skill détecte, l'humain décide.
4. **Un passage propre est un résultat normal.** Si le deck ne déclenche rien, l'écrire en une ligne. Ne jamais inventer un défaut pour justifier la relecture.
5. **Ce que tu ne peux pas voir, tu le dis.** Si l'outil ne rend pas les pixels, écrire que les contrôles visuels ne sont pas vérifiés et faire quand même l'audit du texte et de la structure. Les bourrages de production ne se voient qu'à l'image.

## Règles non négociables

- Aucun chiffre, aucune citation, aucun exemple, aucune source inventés. Un trou se déclare.
- Aucun tiret cadratin, ni dans le deck, ni dans le compte rendu d'audit.
- Le mot juste plutôt que le mot qui sonne : nommer le produit, l'équipe, la date, le lieu, le chiffre.
- Pas de groupe de trois par réflexe, pas de « ce n'est pas X, c'est Y », pas d'« experts disent ».
- Ne pas signaler un marqueur faible comme s'il était diagnostique : la comparaison montre que les decks réels font souvent pire.

## Sources

Distillé de *Remove the AI slop from your decks*, Paul Moss, Analyst Academy, novembre 2026 (`theanalystacademy.com`). Comparaison 100 slides IA contre 100 slides réelles. Les marqueurs d'écriture 13 à 17 reprennent la grille publique de Wikipédia, *Signs of AI writing*. Voir `references/methode-et-limites.md` pour la méthode, les limites et les crédits complets.
