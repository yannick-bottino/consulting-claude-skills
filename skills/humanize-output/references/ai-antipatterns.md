# AI Anti-Patterns — Context File for Humanizing AI Output

> Source principale : [Wikipedia — Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
> Complété par : analyses de Blake Stockton, Medium (Lindsey Norberg), OnlineWritingClub
> Usage : fichier de contexte à injecter dans tout prompt de production ou relecture de texte pour éviter les marqueurs stylistiques typiques des LLMs.

---

## Avertissement préliminaire

Ce fichier n'est pas une liste de mots interdits. Chaque marqueur ci-dessous est un **signal potentiel**, pas une preuve. Les LLMs sont entraînés sur de l'écriture humaine — certains humains écrivent naturellement de cette façon. L'accumulation de plusieurs signaux dans un même texte est ce qui trahit l'origine IA.

Ne pas s'appuyer uniquement sur des outils de détection automatique (GPTZero, etc.) : leur taux d'erreur est non négligeable.

---

## 1. Langage et Ton

### 1.1 Symbolisme gonflé / Importance exagérée
Les LLMs relient systématiquement un sujet à des enjeux plus larges, comme pour lui donner du poids artificiel.

**Mots et expressions à surveiller :**
- "stands as a testament to"
- "plays a vital / significant role"
- "underscores its importance"
- "watershed moment" / "key turning point"
- "deeply rooted"
- "profound heritage"
- "steadfast dedication"
- "solidifies", "continues to captivate", "leaves a lasting impact"
- "pivotal moment in the evolution of..."
- "marking a significant shift toward..."
- "part of a broader movement"

**Exemple typique :**
> *"The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain."*

**Correction :** Énoncer le fait directement, sans le charger de signification implicite.

---

### 1.2 Ton promotionnel (en particulier autour des cultures, lieux, organisations)
L'IA adopte souvent un registre de brochure touristique ou de communiqué de presse.

**Expressions à surveiller :**
- "rich cultural heritage / tapestry"
- "rich history"
- "breathtaking", "stunning natural beauty"
- "must-visit", "must-see"
- "enduring / lasting legacy"
- "vibrant community"

---

### 1.3 Éditorialisation — Opinions non sollicitées
L'IA commente et interprète là où un ton neutre est attendu.

**Expressions à surveiller :**
- "it's important to note / remember / consider"
- "it is worth noting that"
- "no discussion of this topic would be complete without"
- "in this article, we will explore"
- "as we can see"

---

### 1.4 Weasel wording — Attribution vague d'opinions
L'IA attribue des affirmations à des autorités floues pour paraître informée sans source précise.

**Expressions à surveiller :**
- "industry reports suggest"
- "observers have noted / cited"
- "some critics argue"
- "experts believe"
- "it is widely considered"
- "many have argued"

---

### 1.5 Analyses superficielles avec des participes présents
L'IA ajoute souvent une analyse en fin de phrase via un verbe en -ing, qui sonne creux.

**Exemples :**
> *"Consumers benefit from the flexibility to use their preferred mobile wallet, **improving convenience**."*

**Mots à surveiller en fin de proposition :**
- "ensuring..."
- "highlighting..."
- "emphasizing..."
- "reflecting..."
- "demonstrating..."
- "showcasing..."

---

## 2. Structure et Style

### 2.1 Parallélismes négatifs (Negation Pattern)
C'est l'un des marqueurs les plus caractéristiques. L'IA crée un contraste dramatique de type "Ce n'est pas X, c'est Y."

**Exemples :**
> *"It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere."*
> *"Mobile isn't just 'First' — it's Everything."*

Peut s'étaler sur deux phrases consécutives :
> *"He hailed from the esteemed Duse family, renowned for their theatrical legacy. Eugenio's life, however, took a path that intertwined both personal ambition and familial complexities."*

**Structures à surveiller :**
- "It's not X, it's Y"
- "Not just X, but Y"
- "Not only X but also Y"
- "This isn't merely X; it's Y"

---

### 2.2 Abus de connecteurs logiques
L'IA sur-utilise un petit répertoire de transitions pour simuler une cohérence argumentative.

**Transitions à surveiller :**
- "Moreover"
- "Furthermore"
- "In addition"
- "However"
- "On the other hand"
- "In contrast"
- "Notably"
- "It is worth noting that"

---

### 2.3 Rule of Three systématique
Les LLMs surexploitent les structures en trois parties ("le bon, le mauvais et le truand"). Quand presque chaque argument est articulé en triptyque, c'est un marqueur.

---

### 2.4 Uniformité rythmique
L'IA tend à produire des phrases et des paragraphes de longueur très homogène. L'absence de variation de rythme (phrases courtes de rupture, ellipses, accélérations) rend le texte plat.

---

### 2.5 Phrases de conclusion en mode essai
Les LLMs génèrent des conclusions "wrap-up" explicites et laudatives, souvent avec des jugements de valeur.

**Exemples :**
> *"In summary, this represents a significant achievement that will continue to shape the field for years to come."*
> *"This stands as a testament to the power of human creativity and innovation."*

---

### 2.6 Généralisations sans ancrage personnel
L'IA explique et généralise mais ne raconte jamais d'expérience concrète. Absence de détails spécifiques, d'anecdotes, de vécu.

---

## 3. Formatage et Ponctuation

### 3.1 Em-dash (tiret cadratin) — usage excessif et formulaire
Les humains utilisent l'em-dash, mais plus rarement que l'IA et dans des contextes différents. L'IA utilise le tiret cadratin là où un humain mettrait une virgule, une parenthèse, ou deux-points.

**Signal principal :** accumulation d'em-dashes à l'intérieur de phrases pour "puncher" des clauses ou créer des parallélismes.

Note : certains modèles récents (dont GPT) tentent de supprimer ce marqueur suite à sa notoriété.

---

### 3.2 Bullet points avec titres en gras
Structure quasi-inexistante dans l'écriture humaine hors documentation technique, mais omniprésente dans les sorties ChatGPT.

**Pattern typique :**
```
- **Scalabilité :** Le système est conçu pour s'adapter facilement à différents contextes d'usage.
```

Le titre en gras reformule souvent simplement ce que la phrase développe juste après — redondance sans valeur.

---

### 3.3 Gras excessif
L'IA applique le gras de façon prévisible et répétitive (noms de produits, sections, mots-clés), au lieu de le réserver à des moments où l'emphase a une vraie valeur éditoriale.

---

### 3.4 Emojis dans des contextes formels ou semi-formels
Signe d'un LLM qui cherche à paraître engagé ou accessible. À nuancer selon le genre de texte (les emojis peuvent être appropriés dans une newsletter, pas dans un rapport).

---

### 3.5 Listes systématiques là où la prose suffirait
L'IA a tendance à décomposer en liste ce qui serait plus naturellement écrit en prose. Cela fragmente la pensée et la rend moins fluide.

---

## 4. Lexique spécifique — Mots "AI Core"

Les LLMs reviennent systématiquement sur un vocabulaire caractéristique. La présence isolée de ces mots n'est pas un signal, mais leur densité dans un texte l'est.

**Substantifs / adjectifs fréquents :**
- "multifaceted"
- "nuanced"
- "holistic"
- "robust"
- "dynamic"
- "innovative" / "groundbreaking"
- "cutting-edge"
- "transformative"
- "synergy" / "synergies"
- "ecosystem"
- "paradigm"
- "landscape" (utilisé de façon métaphorique : "the AI landscape")
- "tapestry"
- "realm"
- "delve" / "delving into"

**Verbes et formules caractéristiques :**
- "foster" (ex : "foster a culture of innovation")
- "leverage" (omniprésent)
- "navigate" (ex : "navigate the complexities of")
- "embark on a journey"
- "unlock potential"
- "drive meaningful change"
- "at the intersection of"
- "in the age of"
- "as we move forward"

---

## 5. Communication destinée à l'utilisateur (artefacts de prompt)

Ces marqueurs trahissent que le texte n'a pas été relu après génération.

**Éléments à toujours supprimer :**
- Formules introductives sycophantes : *"Great question!", "Certainly!", "Absolutely!", "Of course!"*
- Auto-références : *"As an AI language model...", "As a large language model..."*
- Formules de clôture : *"I hope this helps!", "Feel free to ask if you need anything else!"*
- Méta-commentaires sur la tâche : *"I will now summarize...", "Let me break this down..."*
- Références à la date de coupure : *"As of my last knowledge update..."*
- Markdown résiduel dans un contexte de texte brut

---

## 6. Marqueurs avancés (idiolecte de modèle)

Chaque modèle et chaque version a un style reconnaissable ("idiolecte"). Ce qui est typique de GPT-4 ne l'est pas forcément de Gemini ou Mistral.

- **GPT (versions antérieures à GPT-5)** : em-dashes, négation parallèle, listes à titres gras, formules sycophantes en ouverture
- **Gemini** : tendance à des formulations trop exhaustives, énumérations très complètes
- **Llama 2** : préférence pour l'anglais américain même hors contexte, phrases de conclusion laudatives ("essay wrap-up")
- **DeepSeek** : formulations qui sur-organisent la réponse avec des hiérarchies lourdes

---

## 7. Checklist d'humanisation — Relecture rapide

Avant de finaliser un texte produit ou assisté par IA, passer sur ces points :

- [ ] Supprimer ou reformuler les marqueurs de symbolisme gonflé (section 1.1)
- [ ] Neutraliser le ton promotionnel (section 1.2)
- [ ] Retirer les opinions non sollicitées et commentaires inutiles (section 1.3)
- [ ] Sourcer ou supprimer les attributions vagues (section 1.4)
- [ ] Couper les participes présents en fin de phrase sans valeur analytique (section 1.5)
- [ ] Identifier et casser les structures de négation parallèle (section 2.1)
- [ ] Varier ou supprimer les connecteurs sur-utilisés (section 2.2)
- [ ] Injecter une variation de rythme : phrases courtes, ellipses, ruptures (section 2.4)
- [ ] Supprimer les conclusions en mode essai (section 2.5)
- [ ] Ancrer dans du concret : exemple précis, chiffre, anecdote (section 2.6)
- [ ] Remplacer les em-dashes formulaires par virgules ou parenthèses (section 3.1)
- [ ] Dégrader les bullet-points à titres gras en prose ou liste simple (section 3.2)
- [ ] Passer le lexique "AI core" au crible et remplacer par des mots plus précis (section 4)
- [ ] Supprimer tout artefact de prompt visible (section 5)

---

*Dernière mise à jour : mars 2026. Sources : Wikipedia:Signs of AI Writing, WikiProject AI Cleanup, Blake Stockton, Medium/Bootcamp, OnlineWritingClub.*
