---
name: deliverable-panel-review
description: |
  Revue critique multi-perspective de livrables de conseil. Simule un panel de 3 à 7 parties prenantes (CEO, CSR Manager, CMO, banquier, etc.) qui relisent indépendamment un document, puis synthétise consensus, divergences et compromis actionnables. Utiliser ce skill quand l'utilisateur veut stress-tester un livrable avant livraison client, simuler la réaction d'un COMEX, obtenir un avis croisé multi-angle, ou pressure-tester une recommandation stratégique. Aussi déclencher sur : "panel review", "revue croisée", "stress-test ce doc", "qu'en penserait le CEO", "simule la réaction de...", "deliverable review", "cross-review", ou "/deliverable-panel-review".
---

# Deliverable Panel Review

Simule un comité de relecture composé de parties prenantes aux intérêts divergents. Chaque relecteur produit un avis indépendant. La synthèse identifie consensus, divergences, et propose des arbitrages argumentés.

---

## Étape 1 : Cadrage (obligatoire avant tout lancement)

Poser ces questions à l'utilisateur avec AskUserQuestion. Ne pas lancer d'agents avant d'avoir les réponses.

### 1.1 Fichier(s) à reviewer

> Quel(s) fichier(s) dois-je reviewer ? (chemin ou description)

Si le fichier est un Word, PDF, HTML, ou Markdown : le lire intégralement. Si c'est un ensemble de fichiers (fiches + synthèse), lire tout ce qui est nécessaire pour que chaque relecteur ait une vue complète.

### 1.2 Rôles du panel

Proposer un preset adapté au type de livrable détecté (voir la bibliothèque ci-dessous), puis demander confirmation :

> Pour un [type de livrable détecté], je suggère ce panel :
> - [Rôle 1] : [pourquoi ce rôle apporte une perspective utile]
> - [Rôle 2] : ...
> - ...
>
> Tu veux modifier, ajouter ou retirer des rôles ?

L'utilisateur peut accepter, modifier, ou fournir ses propres rôles. Minimum 3, maximum 7.

### 1.3 Contexte d'audience

> Qui va lire ce document ? Dans quel cadre ? (ex: "le CEO d'AMI pour décider s'il lance un green loan", "le board pour valider la roadmap")

Ce contexte est injecté dans chaque brief de relecteur.

### 1.4 Points d'attention spécifiques (optionnel)

> Y a-t-il des points spécifiques que tu veux que le panel challenge ? (ex: "la tonalité envers les concurrents", "le réalisme des coûts", "le risque si ça fuite")

---

## Étape 2 : Construction des briefs

La langue des briefs et des avis s'adapte à la langue du document reviewé. Document en français = briefs et avis en français. Document en anglais = tout en anglais.

Chaque relecteur reçoit un brief structuré :

```
Tu es [RÔLE] chez [ORGANISATION]. Tu reçois [TYPE DE DOCUMENT] produit par [AUTEUR].
Contexte : [CONTEXTE D'AUDIENCE — réponse étape 1.3]
[Points d'attention spécifiques si fournis — réponse étape 1.4]

[CONTENU INTÉGRAL DU DOCUMENT]

Consignes de review :
[6 questions spécifiques au rôle — voir bibliothèque]

Produis un avis structuré de 300 à 500 mots avec des recommandations concrètes numérotées.
Ne résume pas le document. Va droit aux constats et recommandations.
```

Le contenu intégral du document est injecté dans chaque brief. Ne jamais résumer pour économiser du contexte. Les relecteurs travaillent sur le même matériau.

---

## Étape 3 : Lancement des agents (en parallèle)

Lancer TOUS les agents relecteurs dans un seul message, avec `run_in_background: true`. Ne pas les séquencer : l'indépendance des avis est le point central du dispositif.

Informer l'utilisateur :

> [N] relecteurs lancés en parallèle : [liste des rôles]. Je transmets la synthèse dès qu'ils ont tous terminé.

---

## Étape 4 : Synthèse

Quand tous les agents ont terminé, produire la synthèse avec ces sections exactes :

### A. Consensus

Points où la majorité des relecteurs convergent. Format tableau :

| Point | Agents d'accord | Action recommandée |
|-------|----------------|-------------------|

### B. Divergences

Points où les relecteurs s'opposent. Pour chaque divergence :

**Tension :** [description]
| Relecteur | Position |
|-----------|---------|

**Arbitrage :** [trancher et expliquer pourquoi, ne pas laisser en suspens]

### C. Signaux faibles

Points soulevés par un seul relecteur mais pertinents. Un angle que seul le terrain voit est souvent le plus précieux.

### D. Recommandations finales

Liste numérotée, priorisée. Pour chaque item : quoi changer, pourquoi, quel relecteur l'a déclenché.

La synthèse ne copie-colle pas les avis. La valeur est dans la mise en tension et l'arbitrage.

---

## Bibliothèque de rôles

### Rôles génériques

**CEO / Directeur Général**
1. Le "so what" est-il clair en 2 minutes ?
2. Les données résistent-elles à un challenge en board ?
3. Les recommandations sont-elles les bonnes ? Manque-t-il un angle ?
4. La tonalité est-elle juste ?
5. Ce document est-il présentable en l'état ?
6. Qu'est-ce qui poserait problème si ça fuitait en externe ?

**Directeur Financier / CFO**
1. Les chiffres sont-ils cohérents entre eux ?
2. Les coûts et ROI sont-ils réalistes ?
3. Y a-t-il des engagements financiers implicites non chiffrés ?
4. Les hypothèses économiques sont-elles documentées ?
5. Quel risque financier de suivre ces recommandations ? De ne pas les suivre ?
6. Le document résiste-t-il à un comité d'investissement ?

**CMO / Directeur Marketing**
1. Quel risque réputationnel si ce document sort ?
2. Le narratif est-il utilisable en communication ?
3. Les comparaisons concurrentielles sont-elles formulées prudemment ?
4. Quels quick wins de communication en tirer ?
5. Le document est-il présentable au COMEX ?
6. L'identité de marque est-elle respectée ?

**Client final / Destinataire**
1. Est-ce que je comprends ce qu'on me dit et ce qu'on attend de moi ?
2. Les recommandations sont-elles actionnables avec mes moyens ?
3. Y a-t-il des affirmations que je contesterais ?
4. Le ton est-il adapté à ma position ?
5. Qu'est-ce que je ne trouve pas et que j'aurais voulu voir ?
6. Est-ce que ça justifie ce que j'ai payé ?

**Expert technique / Spécialiste métier**
1. Les données sont-elles techniquement correctes ?
2. La méthodologie est-elle rigoureuse ?
3. Y a-t-il des biais de comparabilité non déclarés ?
4. Manque-t-il des sujets dans le périmètre ?
5. Les recommandations sont-elles réalisables opérationnellement ?
6. Les sources sont-elles vérifiables ?

**Banquier / Investisseur**
1. Ce dossier passerait-il en comité de crédit ?
2. Les KPIs sont-ils mesurables et adossables à des covenants ?
3. Les données sont-elles vérifiables par un tiers ?
4. Quels sont les red flags ?
5. Quels quick wins rendraient ce dossier bancable en 6 mois ?
6. Le benchmark sectoriel est-il pertinent pour évaluer le risque ?

**DRH / Directeur des Ressources Humaines**
1. Les dimensions sociales et humaines sont-elles couvertes ?
2. Les données RH (effectifs, D&I, QVT) sont-elles correctes ?
3. Y a-t-il des risques sociaux ou légaux sous-estimés ?
4. Les recommandations sont-elles compatibles avec la culture d'entreprise ?
5. Quel impact sur l'attractivité employeur ?
6. Les interlocuteurs internes sont-ils bien identifiés ?

**Directeur des Opérations / Supply Chain**
1. Les données produit/supply chain sont-elles fidèles à la réalité terrain ?
2. Les recommandations sont-elles opérationnellement faisables ?
3. Les comparaisons avec les pairs sont-elles justes (même périmètre) ?
4. Manque-t-il des actions déjà en place mais non documentées ?
5. Quel impact sur les prochains cycles opérationnels ?
6. Qu'est-ce qui est faisable à court terme vs moyen terme ?

**Juriste / Risk Manager**
1. Y a-t-il des affirmations qui engagent la responsabilité du client ?
2. Les données concurrentielles sont-elles issues de sources publiques vérifiables ?
3. Y a-t-il des risques de diffamation ou de concurrence déloyale ?
4. Les recommandations sont-elles conformes à la réglementation en vigueur ?
5. Le document peut-il être produit en cas de contentieux ?
6. Les clauses de confidentialité sont-elles respectées ?

---

## Presets par type de livrable

| Type de livrable | Panel suggéré |
|-----------------|---------------|
| Benchmark / Diagnostic RSE | CEO, CSR Manager, CMO, Directeur Opérations, Banquier |
| Propale commerciale | Client final, Associé du cabinet, CFO client, Expert technique |
| Note stratégique interne | CEO, CFO, CMO, DRH, Directeur Opérations |
| Rapport d'audit / Due Diligence | Investisseur, CFO cible, Expert technique, Juriste, Risk Manager |
| Deck COMEX | CEO, CFO, CMO, DRH, Board member |
| Plan de transformation | CEO, DRH, Directeur Opérations, Expert technique, CFO |
| Rapport ESG / VDD | Investisseur, Expert technique, Juriste, CMO, CSR Manager |

Les presets sont des suggestions. L'utilisateur peut mixer, ajouter ou retirer des rôles.

---

## Règles

- **Indépendance** : les agents ne voient jamais les avis des autres. C'est non négociable.
- **Longueur** : 300 à 500 mots par relecteur. Substantiel sans noyer le signal.
- **Factualité** : les relecteurs réagissent au contenu du document. Ils ne fabriquent pas de données. S'ils pensent qu'une donnée manque, ils le signalent.
- **Arbitrage** : la synthèse ne cherche pas le consensus mou. Elle tranche et explique pourquoi.
- **Langue** : s'adapte à la langue du document reviewé.
