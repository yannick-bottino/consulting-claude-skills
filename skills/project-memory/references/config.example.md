# Configuration de référence (instanciation du substrat de mémoire)

> Tout le métier vit ici, jamais dans le `SKILL.md` ni dans `memory-structure.md`. Le skill `project-memory` reste générique ; cette config l'instancie pour une mission de conseil. Copier ce fichier en `config.md` et l'adapter à votre organisation.
>
> Défaut fixe (ci-dessous). Le tailoring est proposé par `project-init` à partir du contexte de mission découvert à l'init. Sans ajustement, le défaut est conservé (cohérence inter-missions).

## Domaines de décision (Cold)

Valeurs autorisées du champ `Domaine` du frontmatter Décision :

| Domaine | Usage |
|---|---|
| `cadrage` | Périmètre, objectifs, exclusions de scope |
| `méthodo` | Approche, framework, méthode d'analyse retenue |
| `hypothèse` | Hypothèse de travail actée (engage l'analyse) |
| `livrable` | Validation humaine d'un livrable ou d'une section |
| `arbitrage-client` | Décision prise avec ou par le client |
| `autre` | Décision structurante hors taxonomie ci-dessus |

## Jalons (Warm)

Valeurs autorisées du champ `Jalon` du frontmatter Synthèse :

- `kickoff` (lancement de la mission)
- `cadrage-validé` (périmètre et objectifs actés)
- `mi-parcours`
- `pré-restitution`
- `restitution` (livraison au client)
- `clôture` (bilan de fin de mission)
- `autre`

## Schéma `context.md`

Métadonnées initialisées par `init_memory`. Champs :

```yaml
---
Scope: mission
Identifiant: <slug>
Client: <nom client>
Mission: <intitulé de la mission>
Équipe: <noms / rôles>
Date début: YYYY-MM-DD
Jalons datés: <optionnel — jalon=YYYY-MM-DD, séparés par virgule>
Locale: fr | en
---
```

Corps libre sous le frontmatter : description courte de la mission, état au moment de l'init.

Le champ `Jalons datés` est optionnel mais utile : il alimente la détection de proximité de jalon de la routine `hebdo` (cf. `operator-cadences.md`). Exemple : `Jalons datés: pré-restitution=2026-07-10, restitution=2026-07-18`.

## Politique de purge des logs (Hot)

| Scope | Seuil de purge | Agrégation préalable |
|---|---|---|
| `mission` | 90 jours rolling | Agréger les logs au-delà du seuil en une synthèse Warm avant purge |

La purge n'est jamais destructrice sans agrégation : on condense d'abord les logs anciens dans une synthèse Warm, puis on supprime les fichiers de log au-delà du seuil.

## Locale

- Défaut : `fr`.
- Les titres standardisés des fichiers (`Décisions`, `Synthèses`, `Logs`, en-têtes de templates) restent en FR dans le substrat (langue de travail interne), indépendamment de la locale des livrables. La locale `en` est portée par les livrables, pas par la grammaire du `_memory/`.

## Racine physique

- Le substrat se crée à la racine du dossier projet courant : `<racine projet>/_memory/`.
- `<racine projet>` est le dossier de la mission (celui où `project-init` a déposé le `CLAUDE.md`).
