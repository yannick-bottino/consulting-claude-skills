# Doctrine de mémoire à 3 couches

> Référentiel générique du substrat de mémoire. Aucune terminologie de domaine en dur : le scope (`mission`) et les types de décisions, jalons et politiques de purge sont définis dans `config.example.md`.

## Principe

Toute mémoire de travail se range dans l'une de trois couches, selon sa volatilité et son statut de vérité. La couche détermine sa durée de vie, sa mutabilité, et qui l'écrit.

| Couche | Dossier | Nature | Mutabilité | Producteur | Durée de vie |
|---|---|---|---|---|---|
| **Cold** | `Décisions/` | Décisions structurantes (golden data) | Immuable | Humain ou validé humain | Permanente |
| **Warm** | `Synthèses/` | État de la pensée aux jalons | Permanent évolutif | Agent (aux jalons) ou humain | Permanente, annotable |
| **Hot** | `Logs/` | Trace des actions IA | Append-only | Agent | Purge configurable |

## Règle de routage (qu'est-ce qui va où)

À toute information à persister, poser la question dans cet ordre :

1. **Est-ce une décision structurante prise ou validée par un humain** (un choix qui engage l'analyse et qu'une régénération IA ne doit jamais écraser) ? Alors c'est une **Décision** (Cold). Exemples génériques : un choix d'hypothèse, l'arbitrage entre options, une exclusion de périmètre, une validation humaine d'un livrable partiel, une décision actée avec le client.
2. **Sinon, est-ce un instantané de l'état de conviction à un moment-clé** (un jalon du cycle de vie de la mission) ? Alors c'est une **Synthèse** (Warm).
3. **Sinon, est-ce la trace d'une action IA** (ce qui a été lu, modifié, sourcé, vérifié lors d'un run) ? Alors c'est un **Log** (Hot).

En cas de doute entre Cold et Warm : si l'information doit survivre intacte à toutes les régénérations futures, c'est Cold. Si elle est un état susceptible d'évoluer, c'est Warm.

> Pourquoi cette séparation plutôt qu'un seul fichier de notes : un journal plat mélange ce qui est gravé (une décision) avec ce qui bouge (une réflexion) et ce qui est jetable (une note de run). Quand l'IA régénère un livrable, elle a besoin de savoir précisément ce qu'elle n'a pas le droit d'écraser. Le foyer canonique unique d'une décision (Cold) est ce qui rend cette garantie possible.

## Cold : `Décisions/` (immuable)

- Une décision = un fichier `YYYY-MM-DD-<slug-decision>.md`.
- **Le corps d'une décision au statut Active n'est jamais modifié.** Le seul Edit in-place autorisé est le flip de statut dans le frontmatter (Active -> Révisée/Abrogée), exécuté par revise/abrogate. Tout autre Edit d'une décision Active est une corruption.
- Réviser = créer une nouvelle décision Active + passer l'ancienne en `Révisée` (lien `Révisé par` dans le frontmatter de l'ancienne, lien `Révise` dans le frontmatter de la nouvelle).
- Abroger = passer l'ancienne en `Abrogée` (sans remplacement).
- Canevas : Contexte / Options envisagées / Décision retenue / Conséquences (cf. `templates/decision-template.md`).
- Les domaines de décision propres à la mission sont listés dans `config.example.md`.

## Warm : `Synthèses/` (permanent évolutif)

- Une synthèse = un fichier `YYYY-MM-DD-<slug-jalon>.md`.
- Permanent évolutif : peut être annotée ou complétée plus tard (contrairement à une décision Cold).
- Canevas : Contexte du jalon / État de la conviction / Points ouverts / Risques à creuser / Prochains jalons (cf. `templates/synthesis-template.md`).
- Produite par l'agent aux jalons configurés (cf. `config.example.md`), ou à la demande humaine.

## Hot : `Logs/` (append-only)

- Un log = un fichier `YYYY-MM-DD-<slug-action>.md`.
- Append-only : jamais modifié après écriture. Un nouveau fichier par action.
- Canevas : Action / Inputs lus / Décisions actives consultées / Modifications apportées / Sources mobilisées / Checks effectués / Sortie (cf. `templates/log-template.md`).
- Politique de purge définie dans `config.example.md`. Avant purge, agrégation préalable des logs anciens en une synthèse Warm.

## Structure de dossier créée par le skill

```
<racine projet>/
 ├── CLAUDE.md              ← pilote de session (déposé par project-init)
 ├── claude_tasks/TODO.md   ← tâches (project-init)
 ├── _memory/
 │   ├── CLAUDE.md          ← règles de routage du substrat (cf. claude-md-per-scope.md)
 │   ├── _Index.md          ← index global du dossier mémoire
 │   ├── context.md         ← métadonnées de la mission (schéma dans config.example.md)
 │   ├── Décisions/         ← Cold, immuable
 │   │   ├── _Index.md
 │   │   └── YYYY-MM-DD-<slug>.md
 │   ├── Synthèses/         ← Warm, jalonné
 │   │   ├── _Index.md
 │   │   └── YYYY-MM-DD-<slug-jalon>.md
 │   └── Logs/              ← Hot, append-only
 │       ├── _Index.md
 │       └── YYYY-MM-DD-<slug-action>.md
 └── (livrables, sources/...)
```

## Cascade d'index

Chaque dossier (`Décisions/`, `Synthèses/`, `Logs/`) porte son propre `_Index.md`. Le `_memory/_Index.md` racine agrège les trois. **Après chaque écriture dans un dossier, son `_Index.md` est régénéré.** Voir `templates/index-template.md`.
