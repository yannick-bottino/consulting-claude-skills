---
type: reference
source: Analyst Academy, Remove the AI slop from your decks (Paul Moss, novembre 2026)
last-refreshed: 2026-11-13
---

# Les 31 marqueurs, leur rang et leur correctif

Numérotation conservée de la source, pour pouvoir s'y référer. Le rang vient de la comparaison de 94 slides IA (la source en annonce 100) contre 100 slides réelles (voir `methode-et-limites.md`). `pire chez le réel` veut dire qu'un deck authentique fait ça plus souvent qu'un deck IA : ce n'est pas un signe de deck IA, même si le correctif reste bon.

## Structure

| N° | Marqueur | Rang | Correctif | Test |
|---|---|---|---|---|
| 1 | Titres génériques (« Overview », « Key insights », « Contexte », « Prochaines étapes ») | pire chez le réel (30 % IA, 43 % réel) | Un titre qui dit ce que la slide prouve, en phrase complète : « Le chiffre d'affaires du T3 progresse, mais deux comptes en portent presque tout » | Lire les titres seuls. Si l'argument ne ressort pas, réécrire les titres |
| 5 | Grille symétrique de trois boîtes ou trois icônes | faible (11 % IA, 8 % réel ; trois boîtes seules : 6 % contre 3 %) | Mise en page asymétrique qui suit le contenu : un gros élément, deux petits, ou un graphique sur deux tiers avec une annotation | Si une seule chose compte, elle est plus grosse. Si quatre points existent, il y en a quatre |
| 7 | Mur de puces uniforme, cinq à sept par slide, chacune amorcée par deux mots en gras et deux-points | faible (21 % IA, 17 % réel ; amorces en gras 17 % contre 30 % réel) | Une idée par slide. Sept puces font trois slides. Varier le rythme : un chiffre, puis un graphique, puis une liste courte | Le nombre de puces suit le contenu, pas un quota |
| 9 | Tout est centré | moyen (6 % IA, 0 % réel) | Corps aligné à gauche, grille et marges constantes, centrage réservé à un chiffre seul, une citation courte, une respiration | Rien de long n'est centré |
| 10 | Même gabarit sur toutes les slides | non mesuré | Tourner sur un petit jeu de gabarits selon ce que la slide doit faire : grande phrase, graphique, comparaison. La cohérence vient des polices, des couleurs et des marges | Deux slides consécutives ne sont pas identiques par défaut |
| 11 | Chart junk, diagrammes décoratifs | pire chez le réel (39 % IA, 49 % réel sur les slides avec graphique) | Titre qui dit la conclusion, puis le graphique, puis une annotation sur le point à voir. Gris pour le contexte, accent sur le point. Un schéma seulement si le processus fonctionne vraiment comme ça | Chaque graphique a une annotation, chaque grille superflue est retirée |
| 15 | Fin « enjeux et perspectives » | non mesuré | Finir sur la décision ou la demande, avec une échéance. « Valider un recrutement d'analyste avant vendredi » est une fin. « Les perspectives sont prometteuses » est un haussement d'épaules | La dernière slide demande quelque chose |
| 21 | Sous-titre en phrase entière sur la couverture | non mesuré | Sous-titre court (audience, réunion, date), ou rien. Si le titre dit le point, il n'y a rien à ajouter | Le sous-titre tient en quelques mots |
| 28 | Rangée de tuiles de chiffres façon dashboard | faible (9 % IA, 7 % réel) | Le chiffre qui prouve le titre, en gros ou en graphique. Le reste en tableau ou en annexe | Un seul chiffre gagne sur la slide |
| 29 | Bourrages de production : chevauchement, débordement, placeholder resté (« Click to add title », « [Détail] », « xxx », « Series 1 »), mot coupé, chiffre du titre qui contredit le graphique | **fort** (30 % IA, 7 % réel, 12 des 17 outils) | Regarder chaque slide en grand avant diffusion. Corriger chaque chevauchement, remplacer chaque placeholder, vérifier la concordance des chiffres | Aucun placeholder, aucun débordement, chiffres concordants |
| 30 | Encadré « key takeaway », « so what » ou bandeau plein en bas de slide | **fort** (18 % IA, 3 % réel) | Mettre la conclusion dans le titre, là où l'œil arrive. S'il faut encore une ligne de conclusion, texte simple dans le corps, sans cadre ni fond ni label | Aucun bandeau bas, aucune boîte de conclusion |

## Contenu et écriture

| N° | Marqueur | Rang | Correctif | Test |
|---|---|---|---|---|
| 4 | Vocabulaire creux : *unlock, elevate, delve, dive in, leverage, empower, harness, seamless, robust, game-changer, cutting-edge, transformative, synergy, journey* | moyen (15 % IA, 8 % réel) | Noms précis, verbes simples. Nommer le produit, l'équipe, le chiffre, la date, le lieu. « Ramener l'onboarding de trois semaines à une » bat « fluidifier le parcours d'onboarding » | Chaque mot creux remplacé par un fait |
| 8 | Faux chiffres : statistique sans source visible, nombres trop ronds, données inventées dans un graphique crédible | faible (80 % IA, 53 % réel sur les slides avec chiffres : aucune source visible) | Données réelles uniquement, avec une source qu'on peut nommer. Sinon `[DATA NEEDED: ...]`, et aller la chercher | Chaque nombre a une source nommable |
| 12 | Phrases de même forme : titres à deux-points, pivots en tiret cadratin partout, longueurs identiques | **fort** (40 % IA, 19 % réel) | Écrire comme on le dirait en réunion. Phrases courtes, certaines plus courtes, voix active. Lire à voix haute : si on ne le dirait pas à un collègue, réécrire | Aucun titre à deux-points, aucun pivot en tiret cadratin |
| 13 | Gravité gonflée : « moment charnière », « témoignage de », « joue un rôle crucial », « s'inscrit dans une tendance de fond » | moyen (3 % IA, 0 % réel) | Dire ce qui s'est passé et de quelle ampleur. « Ouverture de deux régions en mai » vaut mieux que « moment charnière de notre expansion » | Chaque fait a sa taille, aucun adjectif ne la remplace |
| 14 | Attributions floues : « les experts », « les études montrent », « beaucoup considèrent » | faible, non observé dans les deux sets (0 % et 0 %) | Nommer la source ou couper la claim. Un expert sans nom est une fausse statistique en costume | Aucune autorité anonyme |
| 16 | « Ce n'est pas X, c'est Y », « non seulement X, mais Y » | faible, rare des deux côtés (1 % IA, 1 % réel) | Supprimer la première moitié et dire Y. Vérifier ensuite que Y est spécifique : « c'est un état d'esprit » veut souvent dire que personne n'a encore défini ce que ça fait | Aucune négation posée pour l'effet |
| 17 | Groupes de trois par habitude | moyen (21 % IA, 11 % réel) | Autant d'items qu'il y en a. Deux raisons fortes battent deux raisons fortes plus une troisième de remplissage. Si un item sur trois est plus vague, il est là pour le rythme | Chaque liste a la longueur de son contenu |

## Visuel

| N° | Marqueur | Rang | Correctif | Test |
|---|---|---|---|---|
| 2 | Puces emoji, icônes en cercle, icônes décoratives | pire chez le réel (18 % IA, 34 % réel) | Retirer. Un visuel qui n'apprend rien que le texte ne dit pas est du papier peint. Utiliser la place pour un vrai graphique, une capture, une photo de la chose | Aucune icône ne répète le mot d'à côté |
| 3 | Dégradés violets lumineux, glassmorphism, texte en dégradé | faible (6 % IA, 8 % réel) | Palette retenue : un fond, une couleur de texte, un gris, un accent qui ne désigne que ce qui compte. Aplats, pas de lueur | Aucun dégradé, aucun verre dépoli |
| 6 | Blobs 3D, images génériques, cerveau lumineux, main de robot | faible (94 % IA, 57 % réel sur les slides avec image) | Montrer l'objet réel : le produit, la capture, le graphique, le lieu. S'il n'y a pas d'image pertinente, pas d'image | Chaque image a un rapport avec la claim |
| 18 | Boîte blanche arrondie avec un liseré coloré sur un côté ou le haut | faible en général (2 % IA, 0 % réel), très visible quand répété | Aucune boîte à liseré. Séparer par le blanc et l'alignement, ou une fine règle grise, ou une zone à angles droits sans bordure colorée | Supprimer la boîte : si la slide reste claire, c'était de la décoration |
| 19 | Quelque chose au-dessus du titre : surtitre en capitales espacées, kicker, fil d'Ariane, pastille | **fort, le premier de la comparaison** (46 % IA, 8 % réel) | Commencer par le titre et laisser le titre travailler. Si des repères de section sont vraiment utiles, les construire une fois dans le gabarit, petits, en casse de phrase, toujours au même endroit | Rien au-dessus du titre |
| 20 | Barre d'accent au-dessus ou règle colorée sous le titre | faible (12 % IA, 8 % réel) | L'enlever. La taille, le poids et la position du titre suffisent à dire où commencer à lire. Un élément fixe de charte est utilisé tel quel, pas remplacé par une barre | Aucune barre ajoutée par l'outil |
| 22 | Tout au même poids visuel | faible (16 % IA, 17 % réel) | Décider ce que l'œil doit voir d'abord, puis le rendre incontestablement dominant : plus gros, plus lourd, plus seul. Le titre nettement plus gros que le corps | Un élément gagne, deux ou trois maximum restent |
| 23 | Police par défaut partout, ou dix tailles différentes | pire chez le réel (17 % IA, 38 % réel) | Une seule police, regular et gras, trois ou quatre tailles utilisées pareil partout. Un seul mode d'emphase, gras ou couleur, jamais les deux sur le même mot. Pas d'italique ni de couleur sur les derniers mots d'un titre | Même hiérarchie de tailles sur toutes les slides |
| 24 | Cartes flottantes et ombres portées | pire chez le réel (7 % IA, 17 % réel) | À plat. Pas d'ombre, pas de flottement, pas de carte dans la carte. Un tableau simple à filets horizontaux fins suffit | Aucune ombre |
| 25 | Couleur d'accent partout | pire chez le réel (18 % IA, 51 % réel) | L'accent uniquement sur la chose qui compte sur cette slide : le chiffre clé ou la ligne qui prouve le titre. Sinon, gris | Si on ne sait pas dire pourquoi c'est accentué, c'est du gris |
| 26 | Palettes par défaut : crème et serif avec terracotta, bleu nuit et noir avec un accent vif | faible (7 % IA, 8 % réel) | Choisir la palette exprès : les couleurs de la marque, ou un jeu annoncé (fond, texte, gris, accent) sans improvisation | La palette a été décidée, pas héritée d'un défaut |
| 27 | Pastilles, badges, points de statut colorés | pire chez le réel (13 % IA, 18 % réel) | Écrire le mot. Si un statut compte, le mettre dans la cellule du tableau ou dans la phrase. Sinon, couper | Aucune pastille |
| 31 | Bande de couleur pleine hauteur sur le bord gauche ou droit | **fort** (17 % IA, 1 % réel, surtout deux outils) | Laisser le bord tranquille. Les marges encadrent déjà le contenu. Un élément de bord de charte est utilisé tel quel | Aucune bande latérale |

## Mots interdits, français et anglais

Anglais, liste de la source : unlock, elevate, delve, dive in, leverage, empower, harness, seamless, robust, game-changer, cutting-edge, transformative, synergy, journey (sauf voyage réel), « in today's fast-paced world », « let's explore ».

Français, même fonction : libérer le potentiel, élever l'expérience, plonger dans les données, exploiter tout le potentiel, tirer parti, catalyser, fluidifier, robuste, sans couture, révolutionnaire, disruptif, incontournable, transformateur, synergie, parcours (sauf parcours client réel), « dans un monde en constante évolution », « à l'ère du numérique », « force est de constater ».

Préférer le verbe simple qu'on dirait à voix haute, et le nom précis : le produit, l'équipe, la date, le lieu, le chiffre.
