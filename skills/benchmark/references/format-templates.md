# Benchmark — Output Format Templates

This file defines the exact Markdown output formats the skill produces.

Templates 1 to 4, 6 and 7 are Markdown deliverables. Template 5 is the mission config. The scorecard output format (Template 8) lives with its scoring criteria in `references/scorecard.md`: it is not duplicated here.

From schema v3, every comparative table below is a **pivot of `comparables[]`**, not a place to type figures. Pivot, then format. The columns come from `comparability.periods` and the units from `comparability.metrics`.

Illustrative values in these templates come from a vehicle rental mission. Replace them with the mission's own vocabulary: column labels follow the configured dimensions and the segment axis, never a sector borrowed from another market.

---

## Template 1: Per-Actor Analysis

```markdown
## [ACTOR NAME]

**Catégorie :** [Leaser / LCD / Abonnement / Plateforme / ...]
**Statut :** [B2B only / B2B+B2C / B2C only]
**Tagline :** "[tagline officielle ou description courte]"

> « [QUOTE — grande accroche marketing depuis le site officiel — ou [N/D — aucune citation identifiée]] »

**Chiffres clés :** [CA, nombre de véhicules/clients, présence géographique — toujours sourcés]

---

| Dimension | Description | Contenu inclus | Cibles & Tone of Voice | Pricing |
|-----------|-------------|----------------|----------------------|---------|
| [Dim 1 label] | [Description de l'offre] | [Ce qui est inclus] | [Qui, comment] | [Prix, conditions] |
| [Dim 2 label] | ... | ... | ... | ... |
| [Dim 3 label] | ... | ... | ... | ... |
| [Dim 4 label] | ... | ... | ... | ... |

> **À retenir :** [1 phrase de synthèse — ce qui différencie fondamentalement cet acteur]

### INSIGHTS

- ✅ **[Différenciant positif #1]** : [explication concise]
- ✅ **[Différenciant positif #2]** : [explication concise]
- ⚠️ **[Point de vigilance]** : [explication concise]

### Catalogue d'offres *(nature `offer` uniquement — libellé résolu via `projections.catalog.label`)*

| Catégorie | Modèles exemples | 1 mois | 3 mois | 6 mois | 12 mois | Km inclus |
|-----------|-----------------|--------|--------|--------|---------|-----------|
| Économique | [Clio, 208] | [X€] | [X€] | [X€] | [X€] | [500km/mois] |
| Compact / Citadine | [C3, Polo] | [X€] | [X€] | [X€] | [X€] | [500km/mois] |
| SUV | [2008, T-Cross] | [N/D] | [N/D] | [N/D] | [N/D] | [N/D] |

*Prix TTC relevés le [date]. [N/D — non affiché publiquement] si prix non disponible en ligne.*

### Comparatif publié par l'acteur *(nature `offer` uniquement, si l'acteur en publie un)*

| Critère | LMD [Acteur] | LCD | Achat | LLD |
|---------|:-----------:|:---:|:-----:|:---:|
| Sans engagement long terme | ✅ | ✅ | ❌ | ❌ |
| Assurance incluse | [✅/❌] | ❌ | ❌ | ✅ |
| Entretien inclus | [✅/❌] | ❌ | ❌ | ✅ |
| Flexibilité durée | ✅ | ✅ | ❌ | ❌ |
| Véhicule récent garanti | [✅/❌] | ❌ | ❌ | ✅ |

*[N/D — non publié par cet acteur] si le tableau n'est pas disponible*

### Services optionnels *(nature `offer` uniquement)*

| Service | Prix |
|---------|------|
| Pneus hiver | [Inclus / X€/mois / [N/D]] |
| Livraison/restitution à domicile | [Inclus / X€ forfait / [N/D]] |
| Km supplémentaires | [X€/km / [N/D]] |
| Assurance complémentaire | [X€/mois / [N/D]] |

**Sources :**
- [Description du point sourcé] : [URL] (consulté le [date])
- [Document client] : `sources/[filename]`, p.[X]
```

**Notes d'utilisation :**

- Adapter les labels de colonnes aux dimensions configurées en Phase 0
- Si une cellule du tableau est inconnue → `[N/D]` ou `[ESTIMATION — hypothèse: X]`
- "À retenir" = 1 seule phrase, synthétique, actionnable
- INSIGHTS : 2-3 max positifs, 1-2 max négatifs. Pas de liste exhaustive.
- Quote : chercher l'accroche hero / bannière sur le site officiel. Si non trouvée après 2 tentatives → `[N/D]`
- Véhicules & Pricing : adapter les catégories aux segments disponibles chez cet acteur

---

## Template 2: Executive Summary

```markdown
# Executive Summary — Benchmark [Marché] [Année]

## Contexte
[2-3 phrases : qui commande, quel marché, pourquoi ce benchmark maintenant]

## Périmètre analysé
- **Acteurs analysés :** [liste avec catégorie entre parenthèses]
- **Scope :** [ex : durées 1/3/6/12 mois, véhicule référence Peugeot 308 équivalente, 500 km/mois]
- **Géographie :** [ex : France métropolitaine]
- **Date des données :** [MM/YYYY]

## Positionnement des acteurs

| Acteur | Catégorie | B2B/B2C | Prix repère | Différenciant clé |
|--------|-----------|---------|-------------|-------------------|
| [Acteur] | [Catégorie] | [Cible] | [Prix pivot] | [1 différenciant] |

*Note : roue concurrentielle → produite par le skill PPT à partir de `benchmark.json`*

## Faits marquants

1. **[Insight #1]** — [Donnée chiffrée + source]
2. **[Insight #2]** — [Donnée chiffrée + source]
3. **[Insight #3]** — [Donnée chiffrée + source]
4. **[Insight #4]** *(optionnel)*
5. **[Insight #5]** *(optionnel)*

## Recommandation stratégique
[3-5 phrases : positionnement recommandé pour le client commanditaire, leviers identifiés]
```

---

## Template 3: Comparison Synthesis

*Nature `offer`: the sections below apply as written and the file is `pricing-synthesis.md`. Nature `maturity`: replace the three sections with an actors x indicators x years matrix carrying the unit and the verification level of each cell, and name the file `maturity-synthesis.md`. Nature `generic`: build the matrix from `comparability.metrics` and name the file `comparison-synthesis.md`. In all three cases the table is a pivot of `comparables[]`.*

```markdown
# Synthèse Pricing — [Marché] [Année]

## Méthodologie de comparaison
- **Véhicule de référence :** [ex : Peugeot 308 / SUV compact / segment C]
- **Kilométrage de référence :** [ex : 500 km/mois]
- **Durées analysées :** [ex : 1 mois / 3 mois / 6 mois / 12 mois]
- **Périmètre :** [ex : France métropolitaine, offre B2C standard]

## Tableau comparatif tarifaire

| Acteur | 1 mois | 3 mois | 6 mois | 12 mois | Km inclus | Notes |
|--------|--------|--------|--------|---------|-----------|-------|
| [Acteur] | [X€] | [X€] | [X€] | [X€] | [X km] | [conditions particulières] |

*Prix TTC, relevés le [date]. [ESTIMATION] si non public.*

## Analyse de dégressivité

| Acteur | Écart 1m→12m | Remise effective |
|--------|-------------|-----------------|
| [Acteur] | -X% | [X€ économisés sur 12 mois] |

## Indice de transparence tarifaire

| Acteur | Indice (1-3) | Commentaire |
|--------|-------------|-------------|
| [Acteur] | [1/2/3] | [opaque/partiel/transparent] |

*Échelle : 1 = prix uniquement sur devis, 2 = prix indicatifs publiés, 3 = simulateur en ligne complet*
```

---

## Template 4: Cibles & Population Adressable

```markdown
# Analyse Cibles & Population Adressable — [Marché] [Année]

## Méthodologie de sizing
[Décrire l'entonnoir de calcul : population de départ → filtres successifs → cible adressable]

## Entonnoir de population adressable

| Étape | Population | Source | Hypothèse |
|-------|------------|--------|-----------|
| Population totale [géographie] | [X M hab.] | [office statistique, année] | — |
| [Filtre 1 : démographique] | [X M] | [source nommée] | [X% de la pop] |
| [Filtre 2 : comportemental] | [X M] | [source] | [X%] |
| [Filtre 3 : économique] | [X M] | [source] | [X%] |
| **Cible adressable estimée** | **[X M]** | Calcul propre | — |

## Positionnement cibles par acteur

| Acteur | Segment primaire | Segment secondaire | Canal principal |
|--------|-----------------|-------------------|-----------------|
| [Acteur] | [Segment] | [Segment] | [Canal] |

## Frameworks messaging par acteur

| Acteur | Promesse principale | Ton & registre | Exemple de copy |
|--------|--------------------|--------------|--------------------|
| [Acteur] | [Bénéfice central mis en avant] | [Institutionnel / Casual / Expert / ...] | "[Citation ou accroche représentative]" |

*Sources : pages d'accueil, landing pages, campagnes publicitaires observées — citer URL + date*

## Populations non adressables — analyse des barrières

| Segment exclu | Raison d'exclusion | Taille estimée | Potentiel futur |
|---------------|-------------------|----------------|-----------------|
| [Segment] | [Prix / usage / awareness / ...] | [X M — ESTIMATION] | [Oui/Non + condition] |

## Sources utilisées
- [Office statistique] : [URL ou référence publication]
- [Source complémentaire] : [URL ou référence]
- [Autres sources sectorielles]
```

---

---

## Template 6: Market Landscape Map (market-landscape.md)

```markdown
# Cartographie du marché — [Marché] [Année]

## Matrice de positionnement

Colonnes = segments de `scope.segment_axis`, lignes = catégories d'acteurs. Marquer la colonne focus.

| | [Segment 1] | **[Segment focus]** ← Focus | [Segment 3] |
|---|:---:|:---:|:---:|
| **[Catégorie A]** | — | [Acteurs] | [Acteurs] |
| **[Catégorie B]** | [Acteurs] | [Acteurs] | — |
| **[Catégorie C]** | — | [Acteurs] | — |

## Acteurs inclus dans l'analyse

| Acteur | Catégorie | Périmètre | Raison d'inclusion |
|--------|-----------|-----------|-------------------|
| [Acteur] | [Cat.] | [LMD B2C] | [Concurrent direct du client sur son segment cible] |

## Acteurs exclus

| Acteur | Catégorie | Raison d'exclusion |
|--------|-----------|-------------------|
| [Acteur] | [Cat.] | [Hors périmètre B2C / pas d'offre LMD identifiée / données insuffisantes] |

**Sources :** [presse sectorielle, sites officiels des acteurs, étude de marché]
```

**Notes d'utilisation :**
- Construire depuis le champ de segment (`market_position.duration_segment` pour un benchmark commercial) et `category` de chaque acteur JSON
- Indiquer clairement quelle colonne est le "focus" de l'analyse
- Lister les acteurs exclus avec une raison concrète (pas juste "hors scope")
- Si le marché n'a pas d'axe de segmentation pertinent : une seule colonne, nommée d'après le marché, et le dire dans le fichier

---

## Template 7: Recommandation Stratégique (recommendation.md)

*Nature `offer` uniquement. Le cadre Standard/Singularité/Unicité est celui de cette nature, pas celui du skill : pour toute autre nature, la section 4 du profil donne le cadre à produire et ce template ne s'applique pas. Méthodologie : `references/recommendation-framework.md`.*

```markdown
# Synthèse de notre Recommandation Stratégique — [Client]

## Comment [Client] s'impose dans l'océan concurrentiel ?

### STANDARD DE MARCHÉ — Ce que [Client] DOIT proposer
*(Éléments attendus par tous les acteurs du marché — conditions nécessaires non suffisantes)*

- [Feature 1 — présent chez X/Y acteurs, source: actors/*.json]
- [Feature 2 — présent chez X/Y acteurs]
- [Feature 3]

### SINGULARITÉ [CLIENT] — Cœur de proposition
*(Ce qui distingue [Client] sur un terrain partagé avec d'autres acteurs)*

**[Différenciateur central en une phrase]**

- [Point 1 avec evidence : [Client] propose X vs [Concurrent] qui propose Y]
- [Point 2]
- **Avantage prix :** [Client] est ~X% moins cher que les concurrents pour les engagements 1-6 mois [source: pricing-synthesis.md]

### UNICITÉ [CLIENT] — Seule solution pour certaines cibles
*(Segments pour lesquels [Client] est la seule option viable — barrière structurelle)*

| Cible | Barrière des autres acteurs | Pourquoi [Client] gagne |
|-------|----------------------------|------------------------|
| [Segment] | [Barrière structurelle nommée] | [Raison unique et vérifiable] |

## Graphique comparatif prix — [Client] vs concurrents

| Acteur | 1 mois | 3 mois | 6 mois | 12 mois |
|--------|--------|--------|--------|---------|
| **[Client]** *(référence)* | **X€** | **X€** | **X€** | **X€** |
| [Concurrent 1] | X€ | X€ | X€ | X€ |
| [Concurrent 2] | X€ | X€ | X€ | X€ |

*Prix TTC, véhicule référence [modèle], [km]km/mois. Source : pricing-synthesis.md*

## Sources principales
- Benchmark pricing : `pricing-synthesis.md`
- Analyse cibles : `targets-analysis.md`
- Insights acteurs : `actors/*.md`
- Methodology : `references/recommendation-framework.md`
```

**Notes d'utilisation :**
- Lire `references/recommendation-framework.md` avant d'écrire cette section
- Standard : compter les features des actor JSONs — ne pas inférer sans données
- Singularité : nommer le concurrent rival sur chaque point
- Unicité : la barrière doit être structurelle (pas juste "préférence" ou "prix")
- Pricing chart : data source = `benchmark.json → recommendation.pricing_chart`

---

## Template 5: Fichier de configuration mission (mission-config.json)

Produit en Phase 0, utilisé comme référence pour toute la suite.

Le produit de référence, la devise et les périodes vivent dans `comparability`, jamais aussi dans `scope` : deux copies d'un même fait divergent.

`deliverables` pilote ce qui est produit **et** ce qui est scoré. Retirer une entrée retire la section correspondante du scorecard, ce qui est le comportement voulu. `screenshots` conditionne la passe de capture (Step 1.4).

```json
{
  "mission": {
    "name": "[Mission name slug]",
    "client": "[Client name]",
    "market": "[Market description]",
    "date": "YYYY-MM-DD",
    "consultant": "[optional]"
  },
  "benchmark_nature": "offer",
  "sector": "[free text from Q1, e.g. mobilite, assurance, textile]",
  "locale": {
    "output_language": "fr",
    "country": "FR",
    "currency": "EUR",
    "statistical_office": "INSEE"
  },
  "comparability": {
    "reference_product": "[l'offre ou le profil comparé]",
    "currency": "EUR",
    "periods": ["1m", "3m", "6m", "12m"],
    "scope": "[base TTC/HT, volume, géographie]",
    "metrics": [
      { "name": "price", "unit": "EUR/mois", "scope": null }
    ],
    "notes": null
  },
  "branding": {
    "skill": null,
    "tokens_file": null,
    "logo_path": null,
    "resolved": "neutral-fallback"
  },
  "scope": {
    "actors": ["Actor 1", "Actor 2"],
    "actors_excluded": [
      { "name": "Actor X", "reason": "hors périmètre géographique" }
    ],
    "actor_categories": {
      "Category A": ["Actor 1"],
      "Category B": ["Actor 2"]
    },
    "segment_axis": {
      "id": "[axis id, e.g. duree-engagement]",
      "label": "[axis label shown in the landscape map]",
      "segments": [
        { "id": "[segment id]", "label": "[segment label, e.g. 1-24 mois]" }
      ],
      "focus": "[segment id the mission focuses on]"
    },
    "geography": ["France métropolitaine"]
  },
  "dimensions": [
    { "id": "dim1", "label": "Offre, Conditions & Promesse", "description": "Durées, contrats, flexibilité" },
    { "id": "dim2", "label": "Contenu du service", "description": "Inclus/exclus, garanties" },
    { "id": "dim3", "label": "Cibles & Tone of Voice", "description": "B2B/B2C, messaging" },
    { "id": "dim4", "label": "Pricing & Choix", "description": "Grille tarifaire, transparence" }
  ],
  "deliverables": ["exec-summary", "actor-sheets", "pricing-synthesis", "market-landscape", "recommendation", "screenshots", "html-report"],
  "execution": {
    "batch_size": 3,
    "parallel_dispatch": true,
    "resume_enabled": true
  }
}
```
