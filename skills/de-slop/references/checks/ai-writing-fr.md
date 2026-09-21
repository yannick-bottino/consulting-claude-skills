---
type: check
layer: 1-universal
status: active
last-refreshed: 2026-06-18
source: the stop-ai-slop skill (phrases.md). Complement francophone de ai-writing.md. Couvre les marqueurs specifiques a la prose FR qui n'ont pas d'equivalent direct dans les 24 patterns EN.
---

# Check: AI writing tells (FR)

Complement francophone du check `ai-writing.md`. Ce fichier couvre les marqueurs IA specifiques a la langue francaise : openers, jargon consulting, adverbes, formules de remplissage, meta-commentaire, fausse intimite, declaratifs vagues. Charger ce fichier en complement de `ai-writing.md` quand la langue de l'output est FR ou mixte.

Pour chaque occurrence, citer le passage exact et suggerer la correction. Les corrections mecaniques (openers, adverbes, remplissage, meta-commentaire) se regroupent en un seul item "nettoyer la mecanique FR". Les patterns de jugement (jargon contextuel, declaratifs) restent individuels.

Les patterns ci-dessous ne dupliquent pas les 24 patterns EN de `ai-writing.md`. Ils couvrent ce qui est propre au francais ou au registre consulting francophone.

## Patterns FR

**1. Openers de raclement de gorge.** Annonces qui retardent le point. Supprimer et enoncer le contenu directement.

Exemples a bannir :
- "Voici la chose :"
- "Voici ce que / pourquoi / comment [X]"
- "La verite inconfortable est que"
- "Il s'avere que"
- "Le vrai [X] est"
- "Permettez-moi d'etre clair"
- "Soyons honnetes"
- "Peut-on parler de"
- "Ce que je trouve interessant, c'est"
- "Le probleme cependant, c'est que"

Regle : toute construction "Voici ce que/pourquoi/comment" = remplissage. Couper et aller au point.

**2. Bequilles d'emphase.** Formules qui intensifient sans ajouter de sens.

- "Point final." / "Full stop."
- "Laissez ca infuser." / "Let that sink in."
- "C'est important parce que" / "This matters because"
- "Ne vous y trompez pas" / "Make no mistake"
- "Voici pourquoi c'est important"
- "Et c'est la que tout change."
- "C'est exactement ca."

**3. Jargon consulting FR.** Remplacer par des termes concrets.

| Eviter | Utiliser a la place |
|---|---|
| "Naviguer" (les defis) | Gerer, traiter |
| "Decrypter" (une analyse) | Expliquer, examiner |
| "S'inscrire dans" | Faire partie de, contribuer a |
| "Paysage" (le contexte) | Situation, secteur, marche |
| "Game-changer" | Significatif, structurant |
| "Aller plus loin" / "Deep dive" | Approfondir, analyser |
| "Prendre du recul" | Reconsiderer |
| "Going forward" / "A l'avenir" | Ensuite, a partir de maintenant |
| "Circle back" / "Revenir sur" | Reprendre, revisiter |
| "Aligner" (les equipes) | Mettre d'accord, coordonner |
| "Embarquer" (les parties prenantes) | Convaincre, mobiliser |
| "Addresser" (un sujet) | Traiter, aborder |
| "Leviers" (sans precision) | [Nommer le levier precis] |
| "Enjeux" (sans precision) | [Nommer l'enjeu precis] |
| "Transformation" (sans verbe) | Ce qui change concretement |
| "Valeur ajoutee" | Ce que ca apporte precisement |
| "Approche holistique" | [Decrire ce qui est couvert] |
| "Au service de" | Pour, afin de |

**4. Adverbes FR a tuer.** Adverbes en -ment qui intensifient ou edulcorent sans rien ajouter :

- "vraiment", "simplement", "litteralement"
- "fondamentalement", "essentiellement", "intrinsequement"
- "inevitablement", "naturellement", "necessairement"
- "precisement" (sauf quand il precise reellement quelque chose)
- "clairement", "visiblement", "manifestement"

**5. Formules de remplissage FR.** Couper sans remplacer.

- "Au fond" / "En son coeur" / "At its core"
- "Dans le monde actuel" / "In today's [X]"
- "Il convient de noter que" / "It's worth noting"
- "Au bout du compte" / "At the end of the day"
- "En ce qui concerne" / "When it comes to"
- "Dans un monde ou" / "In a world where"
- "La realite est que" / "The reality is"
- "Force est de constater"
- "Il va de soi que"
- "Dans ce contexte" (sans precision)
- "A l'heure ou"
- "Plus que jamais"

**6. Meta-commentaire.** Apartes auto-referentiels. Le texte doit avancer, pas annoncer sa structure.

- "Spoiler :" / "Plot twist :"
- "Mais c'est un autre sujet"
- "La suite de ce document explique..."
- "Permettez-moi de vous guider..."
- "Dans cette section, nous allons..."
- "Comme nous le verrons..."
- "Je veux explorer..."

**7. Fausse intimite / sincerite fabriquee.**

- "Je vous le promets"
- "Sincerement" en ouverture ou fermeture
- "Croyez-moi"
- "Entre nous"

**8. Declaratifs vagues FR.** Phrases qui annoncent l'importance sans nommer la chose precise.

- "Les raisons sont structurelles"
- "Les implications sont significatives"
- "Les enjeux sont importants"
- "Les consequences sont reelles"
- "C'est le probleme le plus profond"

Regle : si une phrase dit que quelque chose est important/profond/structurel sans montrer la chose precise, couper ou remplacer par la chose precise.

## Grading

- Aligned: aucun des patterns 1 a 8 present.
- Drift: quelques occurrences douces (un adverbe isole, un "dans ce contexte" sans gravite). Pas de rupture.
- Misaligned: cluster de jargon consulting, openers en serie, meta-commentaire dans un livrable externe, ou declaratifs vagues empiles.
