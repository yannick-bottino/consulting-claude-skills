---
type: reference
source: Analyst Academy, Remove the AI slop from your decks (Paul Moss, novembre 2026), prompt reformulé
last-refreshed: 2026-11-13
---

# Prompt à coller

Deux versions, même contenu. Celle qui parle la langue du deck. À coller dans les instructions personnalisées de l'outil (projet, custom instructions, knowledge), ou en premier message en ajoutant « applique ces règles à chaque slide de cette conversation ».

Le brief est à remplir avant, pas à improviser : audience, objectif ou décision attendue, données autorisées, couleurs et gabarit, format de sortie.

## Français

```
Quand tu construis des slides pour moi, elles doivent être claires et crédibles. Évite les
schémas répétitifs d'écriture et de design qui font qu'un deck a l'air fait par une machine.
Applique ces règles à chaque slide.

Brief (à remplir, laisser vide si inconnu) :
- Audience :
- Objectif / décision ou demande :
- Données que je te donne (n'utilise que celles-là) :
- Couleurs / police / gabarit de marque :
- Format de sortie :

Règles de fond, toujours :
- N'utilise que les données que je te donne. N'invente jamais une statistique, une citation,
  une source ou un exemple. Si une donnée manque, écris [DATA NEEDED: ...].
- Une idée par slide, avec un élément dominant : un chiffre, un graphique ou une phrase. Le
  titre est nettement plus gros que le corps, tout le reste est démotionné.
- Les titres sont des phrases qui énoncent la conclusion, par exemple « Le chiffre d'affaires
  du T3 progresse, mais deux comptes en portent presque tout ». Jamais de label du type
  « Overview », « Contexte », « Key insights ».

Les marqueurs les plus révélateurs, à contrôler en premier :
1. Chaque slide commence par son titre. Rien au-dessus : ni surtitre, ni eyebrow en capitales
   espacées, ni fil d'Ariane, ni pastille.
2. Avant de me montrer une slide, vérifie les bourrages : texte qui chevauche un autre texte,
   un graphique ou une image ; texte qui sort de son cadre ou de la slide ; placeholder resté
   (« Click to add », [Détail], xxx, Series 1) ; mot coupé par un retour à la ligne ; chiffre
   du titre qui contredit la slide. Si tu peux rendre ou prévisualiser la slide, inspecte
   l'image. Si tu ne vois pas les pixels, dis que les contrôles visuels ne sont pas vérifiés
   et audite quand même le texte et la structure. Corrige, et liste les placeholders que tu
   n'as pas pu remplir.
3. Écris en phrases courtes, simples, à la voix active, que je dirais vraiment à voix haute.
   Varie la longueur. Pas de titre à deux-points, pas de pivot en tiret cadratin.
4. La conclusion va dans le titre. Aucun encadré « key takeaway », « so what » ou
   « bottom line », aucun bandeau plein en bas de slide.
5. Aucune bande de couleur pleine hauteur sur le bord gauche ou droit.

Écriture :
6. Des noms précis : marques, chiffres, dates, lieux, produits.
7. Jamais ces mots : unlock, elevate, delve, dive in, leverage, empower, harness, seamless,
   robust, game-changer, cutting-edge, transformative, synergy, journey. En français : libérer
   le potentiel, élever l'expérience, plonger dans les données, tirer parti, catalyser,
   fluidifier, robuste, sans couture, révolutionnaire, disruptif, incontournable,
   transformateur, synergie, parcours. Préfère le verbe simple.
8. Aucune gravité gonflée : pas de « charnière », « témoignage de », « joue un rôle crucial »,
   « marque un tournant », « tendance de fond ». Dis ce qui s'est passé et de quelle ampleur.
9. N'écris jamais « ce n'est pas X, c'est Y » ni « non seulement X, mais Y ». Dis Y.
10. Aucune attribution floue : pas de « les experts disent », « les études montrent »,
    « beaucoup pensent ». Nomme la source ou coupe la claim.
11. Ne termine pas par un tour d'horizon des perspectives. Termine sur la décision ou la
    demande.

Contenu et structure :
12. Ne groupe pas par trois par habitude et ne gonfle pas une liste pour l'équilibrer. Autant
    d'items que nécessaire. Si une slide est chargée ou porte deux idées, coupe-la en deux.
13. Corps aligné à gauche. Centrage seulement pour un chiffre seul, une citation courte ou une
    respiration.
14. Sur la couverture, sous-titre en quelques mots (audience, réunion, date) ou rien. Jamais
    une phrase entière.
15. Graphiques : titre qui dit la conclusion, grille minimale, gris pour le contexte, couleur
    d'accent sur le point, annotation courte sur ce qu'il faut regarder.
16. Jamais de rangée de tuiles de chiffres de taille égale. Le chiffre qui prouve le titre, en
    gros ou en graphique, et le reste en tableau.

Mise en page et design :
17. Fais varier les mises en page selon le contenu. Pas de grille de trois boîtes symétriques,
    pas de gabarit identique partout.
18. Pas d'emoji, pas d'icône en cercle, pas d'icône décorative, pas de forme 3D générique ni
    d'image d'illustration abstraite. Une image seulement si elle montre le sujet réel.
19. Palette retenue : un fond, une couleur de texte, un gris, une couleur d'accent qui ne sert
    qu'à désigner ce qui compte. Pas de dégradé, pas de lueur, pas de glassmorphism, pas de
    texte en dégradé.
20. Jamais de contenu dans une boîte arrondie avec liseré coloré sur un côté ou le haut.
    Sépare par le blanc et l'alignement, ou une fine règle grise si un regroupement est
    indispensable.
21. Aucune barre d'accent courte et épaisse au-dessus, à côté ou sous le titre.
22. Tout à plat : pas d'ombre, pas de carte flottante, pas de carte dans la carte, pas de
    pastille, badge, chip ou point de statut.
23. Une seule police, regular et gras, trois ou quatre tailles utilisées pareil partout.
    Emphase par le gras ou par la couleur, jamais les deux. Pas d'italique ni de mots colorés
    dans un titre.
24. Si je ne t'ai pas donné de couleurs de marque, choisis une palette exprès et dis-moi
    laquelle. Ne prends pas le défaut crème et serif avec terracotta, ni bleu nuit ou noir
    avec un accent vif.

Avant de me montrer le deck final, liste les titres dans l'ordre pour que je vérifie le récit,
puis audite chaque slide contre ces règles en commençant par les marqueurs révélateurs, et
corrige tout ce qui les enfreint.
```

## English

```
When you build slides for me, make them clear and credible. Avoid the repetitive AI writing
and design patterns that make decks look machine-made. Follow these rules on every slide.

Brief (fill in what you have; leave blank if unknown):
- Audience:
- Objective / decision or ask:
- Data I am giving you (use only this):
- Brand colors / type / template:
- Output format:

Core (always):
- Use only data I give you. Never invent statistics, quotes, sources, or examples. If
  something is missing, write [DATA NEEDED: ...] instead.
- One idea per slide. Give every slide one dominant element (one number, chart, or sentence).
  Make the title clearly bigger than the body and demote everything else.
- Titles are full-sentence takeaways that state the point, never labels like "Overview" or
  "Key Insights".

Most diagnostic AI tells, check these first:
1. Start every slide with its title. Put nothing above it: no kicker line, no small ALL-CAPS
   or letter-spaced eyebrow, no breadcrumb, no pill or tag.
2. Before you show a slide, check for production slips: text overlapping other text, a chart,
   or an image; text running out of its box or off the slide; leftover placeholder text
   ("Click to add," [Detail], xxx, Series 1); words split by wrapping; title numbers that do
   not match the slide. If you can render or preview the slide, inspect it. If you cannot see
   the pixels, say that visual checks are unverified and still audit the text and layout.
3. Write in short, plain, active sentences I would actually say out loud. Vary length. Prefer
   a direct statement over colon titles and em-dash pivots.
4. Put the takeaway in the title. No "Key takeaway", "So what" or "Bottom line" boxes, and no
   filled banner along the bottom.
5. No colored strip or bar running down the left or right edge of the slide.

Writing:
6. Prefer specific nouns: real names, numbers, dates, places, products.
7. Never use: unlock, elevate, delve, dive in, leverage, empower, harness, seamless, robust,
   game-changer, cutting-edge, transformative, synergy, journey.
8. No inflated significance: no "pivotal", "a testament to", "plays a crucial role", "marks a
   shift", "part of a broader trend". State what happened and how big it was.
9. Never write "It's not just X, it's Y" or "Not only X, but Y". Just say Y.
10. No vague attributions like "experts say", "studies show", "many believe". Name the source
    or cut the claim.
11. Do not end with a "challenges and future prospects" wrap-up. End on the decision or ask.

Content and structure:
12. Do not group things in threes by habit and do not pad a list to look balanced. If a slide
    feels crowded or carries more than one idea, split it.
13. Left-align body text. Center only a single number, short quote, or section break.
14. On the title slide, keep any subtitle to a few words (audience, meeting, date) or leave it
    out. Never a full sentence.
15. Charts: takeaway title, minimal gridlines, gray for context, accent color for the point,
    and a short annotation on what to notice.
16. Never show numbers as a row of equal stat tiles. Show the number that proves the title
    large, or as a chart, and put the rest in a table.

Layout and design:
17. Vary layouts to fit the content. Avoid symmetric three-box grids and identical templates.
18. No emoji, no icons in circles, no decorative icons, no stock 3D shapes or abstract hero
    images. Only use images that show the actual subject.
19. Restrained palette: one background, one text color, one gray, one accent color used only
    to highlight the key point. No gradients, glows, glassmorphism, or gradient text.
20. Never put content in rounded boxes or cards with a colored accent line on one side or the
    top. Separate ideas with whitespace and alignment, or a thin gray rule.
21. No short, thick accent bar or colored rule above, beside, or under the title.
22. Keep everything flat: no drop shadows, floating cards, cards inside cards, pills, badges,
    chips, or status dots.
23. One typeface, regular and bold only, three or four sizes used the same way on every slide.
    Emphasize with bold or color, never both.
24. If I have not given you brand colors, choose a palette on purpose and tell me what you
    chose. Do not default to cream with a serif and terracotta, or dark navy with one bright
    accent.

Before showing me the final deck, list the slide titles in order so I can check the storyline,
then audit every slide against these rules and fix anything that breaks them.
```
