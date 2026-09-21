# General Template

Ce template est le format standard pour tout type de reunion professionnelle. Il est concu pour etre lisible, actionnable et autonome (comprehensible sans avoir assiste a la reunion).

## Structure du document

Le document suit exactement cette structure, dans cet ordre :

```
# Titre de la reunion - Date

---

## Objectif de la reunion

Une phrase.

## Principales conclusions

- **Mot-cle :** Description concise.
- **Mot-cle :** Description concise.
- (3 a 5 items)

## Sujets abordes

### Sous-theme 1

- Points structures avec labels en gras
- Sous-points avec details

### Sous-theme 2

(...)

## Prochaines etapes

- **Nom de la personne :**
  - Action 1.
  - Action 2.
- **Nom de la personne :**
  - Action 1.

## Action Items

- **Action courte et autonome**
- **Action courte et autonome**
```

## Instructions par section

### Titre

Reprends le titre du transcript tel quel. Si le transcript contient un statut entre crochets (ex: `[CONFIRMED]`), conserve-le. Ajoute la date si elle n'est pas dans le titre.

### Tableau de metadonnees (docx uniquement)

En format docx, ajoute un tableau de metadonnees immediatement apres le titre, avec les champs suivants :
- **Date** : date de la reunion
- **Duree** : duree du transcript ou de la reunion
- **Participants** : liste des participants avec leur affiliation (Nom Prenom, Entreprise/Role)
- **Enregistrement** : source et duree si mentionnes (ex: "Fathom, 59 min")

Ce tableau donne un contexte immediat au lecteur. En markdown, ces informations sont integrees sous le titre en texte simple.

### Objectif de la reunion

Une seule phrase qui repond a la question : "Pourquoi cette reunion a-t-elle eu lieu ?". Ce n'est pas un resume, c'est le but. Distille-le a partir de l'introduction ou du contexte general.

Exemples de bons objectifs :
- "Lancer le projet d'ESG VDD pour le processus de sortie de Valority."
- "Passer en revue l'avancement de la due diligence ESG et s'aligner sur les sujets cles de gouvernance."
- "Demonstrer un processus de due diligence pilote par l'IA et partager des outils de productivite."

### Principales conclusions

C'est la section "executive summary". Quelqu'un qui ne lit QUE cette section doit comprendre les 3 a 5 choses les plus importantes qui se sont passees dans cette reunion.

Chaque item suit le format : `- **Label court :** Description en 1-2 phrases.`

Le label en gras est le sujet/theme (pas une phrase complete). La description qui suit doit etre factuelle et specifique, pas vague. Inclure les chiffres cles si pertinent.

Criteres de selection : ce qui entre ici, c'est ce qui aurait un impact sur la suite du projet si on le ratait. Les decisions, les alignements strategiques, les risques identifies, les changements de perimetre.

### Sujets abordes

C'est le coeur du document. Le transcript est reorganise en sous-sections thematiques (pas chronologiques).

Chaque sous-section (`###`) couvre un sujet distinct discute pendant la reunion. A l'interieur, utilise une hierarchie de bullet points avec des labels en gras pour structurer :

- **Niveau 1** : Le point principal (contexte, constat, decision)
  - **Niveau 2** : Details, justification, donnees
    - **Niveau 3** : Sous-details si necessaire

Labels courants a utiliser en gras :
- "Statut :" pour decrire ou en est quelque chose
- "Action :" pour ce qui doit etre fait
- "Justification :" pour expliquer pourquoi une decision a ete prise
- "Decision :" pour un arbitrage qui a ete fait
- "Recommandation :" pour une suggestion validee ou a valider
- "Perimetre :" pour les limites d'un sujet
- "Risque :" pour un risque identifie
- "Impact :" pour les consequences d'une decision

Quand un sujet a ete discute a plusieurs moments du call, consolide tout dans la meme sous-section. L'objectif est qu'un lecteur qui cherche un sujet specifique le trouve en un seul endroit.

### Prochaines etapes

Groupe par personne responsable (ou par entite si les noms individuels ne sont pas clairs). Chaque personne a son nom en gras, suivi de ses actions.

Les actions doivent etre specifiques et actionnables : pas "suivre le sujet X", mais "envoyer le document Y a Z avant le [date]".

Si une date ou un delai a ete mentionne, inclus-le.

### Action Items

Version ultra-condensee des prochaines etapes, formatee pour etre copiee directement dans un outil de suivi (Asana, Notion, Todoist, etc.).

Chaque item est :
- Court (une ligne)
- Autonome (comprehensible sans le reste du document)
- A l'imperatif
- En gras
- Prefixe par le responsable entre crochets : `[Nom/Entite]`
- Inclut la deadline si mentionnee

Ces action items sont dans la meme langue que le reste du document.

## Synthese email (si demandee)

Si l'utilisateur demande une version email, produis un corps de mail court et actionnable :

**Structure :**
1. Phrase d'accroche renvoyant au document complet en PJ
2. 5 a 7 points numerotes, uniquement les sujets necessitant une action ou une decision
3. Phrase de cloture sobre

**Regles :**
- Chaque point : sujet + statut/decision + responsable ou deadline
- Pas de mise en forme lourde (pas de gras, pas de sous-listes, pas de headers)
- Les sujets secondaires ou purement informatifs sont renvoyes au document joint
- Le ton est professionnel mais direct, pas de formules de politesse excessives
- Respecter la langue et l'orthographe (accents inclus)

**Bon exemple :**
```
Bonjour a tous,

Vous trouverez en PJ le compte-rendu detaille de notre point du [date]. Ci-dessous les sujets cles qui demandent une action rapide.

1. [Sujet] : [statut/decision]. [Responsable] [deadline].
2. [Sujet] : [statut/decision]. [Responsable] [deadline].
(...)

Le detail complet ([liste sujets secondaires]) est dans le document joint.

Bonne reception,
[Nom]
```
