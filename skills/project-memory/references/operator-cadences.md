# Routines de maintenance : le modèle à 3 cadences

> Détail des routines `lint_memory` et `operator_run`. Hérité de la philosophie operator du vault Obsidian de Yannick (`AI-OS-operator` / `AI-OS-lint`, eux-mêmes adaptés de `os-operator` BenAI), calé sur le rythme d'une mission de conseil. À lire pour exécuter ou programmer une routine.

## Principe directeur (règles dures, héritées)

- **Une invocation = un run = un rapport = stop.** Pas de boucle, pas de question en cours de run.
- **Sortie 100 % locale, dans `_memory/`** (logs + cascade d'index). Aucune notification externe par défaut.
- **Propositions, jamais d'action structurante silencieuse.** Une routine ne crée/révise/abroge jamais une décision, ni n'écrit une synthèse de fond, sans validation humaine. Elle écrit ses constats et ses suggestions dans un log, sous une section « Propositions (validation humaine requise) ».
- **Idle-timeout** : une étape qui n'avance pas -> l'abandonner, la logguer, continuer le run.
- **Failure handling** : une étape qui échoue -> la logguer, continuer le run (ne pas tout interrompre).
- **Freshness** : re-scanner les fichiers à chaque run, ne jamais se fier au dernier log ni à l'index pour décider quoi lire.

## Les 3 cadences

`dreams` et `jalon` sont la **même opération profonde** ; elles ne diffèrent que par le déclencheur (calendaire régulier vs événement jalon). On n'implémente donc qu'une passe légère (`hebdo`) et une passe profonde (réutilisée par `dreams` et `jalon`).

| Cadence | Profondeur | Déclencheur | Sortie |
|---|---|---|---|
| `hebdo` | Légère (heartbeat) | Planifié auto (Cowork), hebdomadaire | Log court de propositions |
| `dreams` | Profonde | Planifié auto (Cowork), mensuel | Synthèse + log |
| `jalon` | Profonde (= `dreams`) | Événementiel : proposé par `hebdo`, ou manuel | Synthèse de jalon + log |

### Cadence `hebdo` (heartbeat léger)

Déclencheurs : `operator_run hebdo`, "lance le heartbeat", planification hebdomadaire.

Séquence (ordre strict) :
1. **`lint_memory full`** : capturer les compteurs (index corrigés, frontmatters non conformes, incohérences Cold, contradictions, logs à purger).
2. **Check de conviction rapide** : lire les décisions `Active` + la dernière synthèse. Repérer les signaux de décision possiblement périmée (signal récent contradictoire dans les logs) et les contradictions inter-décisions.
3. **Détection de proximité de jalon** (cf. section dédiée ci-dessous).
4. **Générer le log** (`log_action`, action=heartbeat) : résumé en 1 phrase, résultats du lint, et section « Propositions (validation humaine requise) » incluant, le cas échéant, « jalon X proche/atteint -> lancer `operator_run dreams` ? ».
5. **Cascade d'index** (faite par `log_action`).

### Cadence `dreams` (re-lecture froide profonde)

Déclencheurs : `operator_run dreams`, "lance le dreams", planification mensuelle.

Re-lecture froide complète, pour faire émerger ce qui n'apparaît pas en vision hebdo.

1. **Sources** : toutes les décisions `Active`, toutes les synthèses, les logs depuis la dernière synthèse.
2. **Produire une synthèse** (`create_synthesis`, jalon `autre` si hors jalon nommé, ou le jalon courant) avec les sections : État des convictions · Tensions structurantes · Décisions implicites détectées (workflows changés sans décision formelle) · Connexions inattendues (cross-domaine) · Fils à tirer.
3. **Propositions à valider** (NE PAS exécuter sans validation) : décisions implicites à formaliser (`create_decision` à proposer), décisions périmées à réviser/abroger, jalon atteint sans synthèse.
4. **Purge éventuelle** : si des logs dépassent le seuil de `config.example.md`, proposer `purge_logs` avec agrégation préalable.
5. **Log de run** (`log_action`, action=dreams) + cascade d'index.

### Cadence `jalon` (profonde, déclenchée par un jalon)

Identique à `dreams`, mais déclenchée par l'arrivée à un jalon clé (proposée par le `hebdo` ou lancée manuellement). La synthèse produite porte le `Jalon` correspondant (cf. `config.example.md`), pas `autre`.

Déclencheurs : `operator_run jalon=<nom>`, "on arrive au pré-restitution, lance la synthèse de jalon".

## Détection de proximité de jalon (passe `hebdo`)

Signaux concrets vérifiés à chaque run hebdo. Tout signal positif -> **proposer** (jamais déclencher silencieusement) un `operator_run dreams`/`jalon` dans la section Propositions du log :

1. Une tâche de restitution/livrable proche du `done` ou datée prochainement dans `claude_tasks/TODO.md`.
2. Une rafale récente de décisions dans les domaines `livrable` ou `arbitrage-client`.
3. Une date de jalon de `context.md` (`Jalons datés`) qui approche (fenêtre ~7 jours).
4. Un jalon configuré (cf. `config.example.md`) sans synthèse correspondante alors que le contexte suggère qu'il est atteint.

## Scheduling

| Contexte | Scheduling autonome |
|---|---|
| **Cowork** | Oui. `project-init` (via ce skill) propose à l'init de planifier `hebdo` (hebdomadaire) + `dreams` (mensuel) via le mécanisme de routines Cowork. `jalon` reste événementiel, non planifié au calendrier. |
| **Claude Code (local)** | Hors scope pour l'instant. Les routines restent disponibles en on-demand (manuel). Le scheduling local sera câblé ultérieurement (app desktop). Raison : un cron cloud n'a pas accès au dossier local. |

Principe HITL : démarrer en manuel quelques cycles pour valider la valeur, puis basculer en planifié seulement après accord humain. Aucune routine activée sans cette validation.
