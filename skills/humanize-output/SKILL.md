---
name: humanize-output
description: >
  Applique systématiquement les anti-patterns IA pour désrobotiser tout texte produit ou co-produit avec un LLM.
  Utiliser ce skill pour TOUTE génération de texte : emails, mails, propositions commerciales, propales, documents de projet,
  comptes-rendus, rapports, synthèses, articles, posts LinkedIn, slides avec du texte, fiches, briefs, notes stratégiques,
  réponses à appels d'offres, CVs, biographies, communications internes, messages Slack, ou tout autre livrable écrit.
  Déclencher aussi quand l'utilisateur dit "écris", "rédige", "reformule", "améliore ce texte", "humanise", "rends ça moins IA",
  "prépare un mail", "fais un doc", "produis un", "génère un", "peut-tu écrire", "aide-moi à rédiger",
  ou toute demande qui aboutira à la production d'un texte destiné à être lu par un humain.
  NE PAS déclencher pour : du code, des extractions de données pures, des calculs, des requêtes SQL, des traductions mot à mot.
---

# Humanize Output

Ce skill garantit que tout texte généré ou édité évite les marqueurs stylistiques caractéristiques des LLMs.
Il fonctionne en deux modes : **génération** (texte produit from scratch) et **relecture** (texte IA brut à humaniser).

---

## Étape 0 — Vérification de fraîcheur (à faire EN PREMIER, en silence)

Lire `/mnt/skills/user/humanize-output/references/last_updated.txt`.

Calculer le nombre de jours depuis cette date par rapport à la date du jour.

- **Si < 30 jours** : charger directement `references/ai-antipatterns.md` et passer à l'Étape 1.
- **Si >= 30 jours** : exécuter le protocole de mise à jour ci-dessous AVANT de continuer.

### Protocole de mise à jour (si >= 30 jours)

1. Informer l'utilisateur : *"Les anti-patterns datent de plus d'un mois — je vais chercher la version à jour sur Wikipedia avant de commencer."*
2. Fetcher `https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing` avec `web_fetch`.
3. Comparer avec `references/ai-antipatterns.md` :
   - S'il y a des **nouveaux patterns** ou des **patterns supprimés** : noter les deltas.
   - S'il n'y a **aucune différence significative** : noter "Aucune mise à jour nécessaire" et continuer.
4. Travailler avec la version fraîche en contexte pour cette session.
5. **Si des différences ont été trouvées** : à la fin de la session, produire un `.skill` mis à jour et le présenter à l'utilisateur avec la mention : *"Des nouveaux anti-patterns ont été détectés. Voici un fichier `.skill` mis à jour à réinstaller pour pérenniser ces changements."*

---

## Étape 1 — Charger les anti-patterns

Lire le fichier `references/ai-antipatterns.md` dans son intégralité.

Ce fichier contient 7 sections :
1. Langage & Ton (symbolisme gonflé, ton promotionnel, éditorialisation, weasel wording, participes présents)
2. Structure & Style (négation parallèle, connecteurs, rule of three, rythme, conclusions wrap-up, absence d'ancrage)
3. Formatage & Ponctuation (em-dash, bullet points gras, gras excessif, emojis déplacés, listes inutiles)
4. Lexique "AI Core" (mots à haute densité LLM : multifaceted, leverage, nuanced, delve, tapestry, etc.)
5. Artefacts de prompt (formules sycophantes, auto-références, formules de clôture)
6. Idiolecte par modèle (patterns spécifiques GPT, Gemini, Llama, DeepSeek)
7. Checklist de relecture (14 points actionnables)

---

## Étape 2 — Identifier le mode

### Mode A : Génération from scratch
L'utilisateur demande de produire un nouveau texte.

**Contraintes à appliquer pendant l'écriture (pas en post-processing) :**

- Construire les phrases avec variation de longueur : alterner phrases courtes et longues, ne pas homogénéiser
- Interdire les connecteurs formulaires en début de paragraphe (Moreover, Furthermore, In addition, However en ouverture systématique)
- Proscrire les structures de négation parallèle ("Ce n'est pas X, c'est Y") sauf si stylistiquement intentionnel et unique dans le texte
- Bannir le lexique "AI core" : chaque occurrence de multifaceted, nuanced, robust, leverage, holistic, innovative, groundbreaking, transformative, synergy, ecosystem, paradigm, landscape (métaphorique), tapestry, realm, delve doit être remplacé par un mot plus précis et concret
- Ancrer dans du concret : au moins un exemple, chiffre, ou détail spécifique par argument principal
- Ne pas conclure avec une phrase "wrap-up" laudative
- Pas de bullet points à titres gras sauf si le format le justifie structurellement (documentation technique, checklist opérationnelle)
- Ne jamais introduire une analyse superficielle via un participe présent en fin de phrase (ensuring..., highlighting..., reflecting...)
- Ton : factuel, direct, pas promotionnel, pas éditorialisant

### Mode B : Relecture / Humanisation d'un texte existant
L'utilisateur colle un texte brut produit par une IA.

**Processus :**

1. Passer le texte contre la checklist en 14 points (Section 7 des anti-patterns)
2. Identifier les occurrences pour chaque catégorie
3. Produire le texte édité
4. En fin de réponse, fournir un **bref diagnostic** : quels anti-patterns ont été corrigés et combien d'occurrences (max 5 lignes, pas de liste exhaustive)

---

## Étape 3 — Adapter au genre textuel

Les contraintes s'appliquent différemment selon le type de livrable. Ajuster le niveau d'intervention :

| Genre | Points de vigilance prioritaires |
|---|---|
| Email professionnel | Suppressions des formules sycophantes, ton direct, pas de bullet-points à titres gras |
| Propale / réponse AO | Ton sobre pas promotionnel, chiffres concrets, pas de "transformative" / "innovative" |
| Document de projet | Rythme varié, pas de wrap-up, ancrage factuel |
| Post LinkedIn / externe | Négation parallèle, symbolisme gonflé, ton travel-brochure |
| Note stratégique interne | Weasel wording, attributions vagues, éditorialisation |
| Compte-rendu / synthèse | Connecteurs formulaires, participes présents creux |
| Slide texte | Bullet-points à titres gras, lexique AI core |

---

## Étape 4 — Produire et livrer

Produire le texte directement, sans annoncer ce que tu vas faire ni commenter la méthode appliquée.

**Ne jamais :**
- Commencer par "Bien sûr !" / "Absolument !" / "Certainement !"
- Terminer par "J'espère que cela vous convient" / "N'hésitez pas à me demander des modifications"
- Expliquer que tu as appliqué les anti-patterns (sauf si l'utilisateur est en Mode B et attend le diagnostic)

**En Mode B uniquement**, terminer par un diagnostic court :
```
— Corrections appliquées : [liste concise des catégories touchées + nb d'occurrences]
```

---

## Référence

Pour consulter la liste complète des anti-patterns, des exemples et de la checklist :
→ `references/ai-antipatterns.md`

Pour comprendre l'idiolecte spécifique d'un modèle (GPT, Gemini, Llama, DeepSeek) :
→ Section 6 de `references/ai-antipatterns.md`
