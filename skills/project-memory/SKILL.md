---
name: project-memory
description: >
  Moteur de mémoire structurée à 3 couches (Cold / Warm / Hot) pour une mission de conseil.
  À utiliser dès qu'un agent ou un skill doit lire ou persister de la mémoire projet
  avant de modifier un livrable. Se déclenche pour : initialiser le substrat de mémoire d'un
  projet (init_memory, appelé par project-init), lire les décisions actives AVANT de
  réécrire un livrable, acter une décision structurante (cadrage, méthodo, hypothèse,
  arbitrage client), écrire une synthèse de jalon, logguer un run IA, ou lancer une passe de
  maintenance ("lint", "health-check de la mémoire", "operator run", "heartbeat", "dreams",
  "vérifie la mémoire du projet", "synthèse de jalon"). Lire les décisions actives EN PREMIER
  avant d'écraser toute saisie humaine. Utilise ce skill chaque fois que la mémoire d'un projet
  doit être lue, écrite ou maintenue, même si l'utilisateur ne nomme pas explicitement
  le "substrat" ou la "mémoire".
---

# project-memory

Substrat de mémoire structurée par mission, à 3 couches (Cold / Warm / Hot). Colonne vertébrale d'une mission de conseil : garantit que les décisions humaines (golden data) ne sont jamais écrasées par une régénération IA, mutualise la mémoire entre tous les agents/skills d'une mission, et rend la pensée auditable.

Ce skill est **LLM-driven** : tu exécutes chaque opération toi-même via Read / Write / Edit sur des fichiers `.md`. Il n'y a pas de moteur Python. La fiabilité du substrat dépend entièrement de ta discipline à suivre les gestes ci-dessous dans l'ordre.

Ce skill est le **moteur** ; il est en général invoqué par `project-init` (à l'init) ou par un agent métier (en cours de mission). Le point d'entrée du cycle de vie d'un projet est `project-init`, pas ce skill.

## Règles dures (jamais d'exception)

1. **Immuabilité Cold.** Ne jamais éditer le **corps** d'une décision au statut `Active`. Le seul Edit in-place autorisé sur un fichier `Décisions/` est le flip de statut dans le frontmatter (Active -> Révisée ou Abrogée, avec mise à jour de `Révisé par`), exécuté exclusivement par `revise_decision` ou `abrogate_decision`. Tout autre Edit d'une décision Active est une corruption du substrat.
2. **Index après chaque écriture.** Après TOUTE écriture dans `Décisions/`, `Synthèses/` ou `Logs/`, régénérer immédiatement l'`_Index.md` du dossier touché, puis le `_memory/_Index.md` racine. C'est une étape à part entière, jamais omise.
3. **Frontmatter conforme avant Write.** Vérifier le frontmatter contre `references/frontmatter-standards.md` avant chaque Write. Champ obligatoire manquant ou valeur énumérée invalide : corriger d'abord, ne pas persister un fichier non conforme.
4. **Append-only Hot.** Un log = un nouveau fichier. Jamais d'Edit d'un log existant.

## Référentiels (lire au besoin, progressive disclosure)

- `references/memory-structure.md` : doctrine des 3 couches, règle de routage, structure de dossier.
- `references/frontmatter-standards.md` : les 4 frontmatters + règle de validation avant écriture.
- `references/templates/` : canevas de contenu (decision, synthesis, log, index).
- `references/claude-md-per-scope.md` : template du `CLAUDE.md` déposé dans chaque `_memory/`.
- `references/config.example.md` : domaines de décision, jalons, schéma `context.md`, politique de purge, locale. **À lire pour toute opération qui touche un `Domaine` ou un `Jalon`.**
- `references/operator-cadences.md` : détail des routines `lint_memory` / `operator_run` et du modèle à 3 cadences. **À lire avant d'exécuter ou de programmer une routine.**

Le SKILL.md reste générique : les valeurs métier (domaines, jalons) vivent dans `config.example.md`.

## Opérations

Chaque opération est une séquence de gestes ordonnés. Exécuter dans l'ordre, sans sauter d'étape.

### init_memory(id, locale, context_meta)
Crée la structure complète. Idempotent : si `_memory/` existe déjà, ne rien casser (compléter ce qui manque seulement).
1. Déterminer la racine : la racine du dossier projet courant (`<racine projet>/_memory/`).
2. Créer `_memory/` et les 3 sous-dossiers `Décisions/`, `Synthèses/`, `Logs/`.
3. Lire `references/config.example.md` pour le schéma `context.md`, les domaines et jalons.
4. Écrire `context.md` (frontmatter du schéma de `config.example.md` + corps : description courte). Substituer les `context_meta` fournis. Valider le frontmatter contre le schéma config (tous les champs présents, dates au format `YYYY-MM-DD`) avant Write.
5. Écrire `_memory/CLAUDE.md` depuis `references/claude-md-per-scope.md`, en substituant id / locale et en **copiant les listes de domaines et jalons** depuis config.example.md (le CLAUDE.md doit être autoportant).
6. Écrire un `_Index.md` vide (mais frontmatté) dans chacun des 3 sous-dossiers, puis le `_memory/_Index.md` racine (Scope: top).
7. **Proposer la programmation des routines de maintenance** : si le contexte est Cowork, poser l'`AskUserQuestion` de programmation (cf. `references/operator-cadences.md`, section Scheduling). Si Claude Code local : ne pas proposer de scheduling (les routines restent on-demand). Défaut si pas de réponse : maintenance manuelle, aucune routine programmée.

### read_context(id)
1. Read `context.md`. Retourner les métadonnées (frontmatter + corps) à l'agent appelant.

### read_active_decisions(id, domain=None)
**Appel obligatoire pour tout agent avant modification d'un livrable.** Chemin de sécurité : ne pas dépendre de l'`_Index.md` (qui peut être désynchronisé), scanner les fichiers directement.
1. Lister tous les fichiers `.md` de `Décisions/` (hors `_Index.md`). Read le frontmatter de chacun.
2. Filtrer ceux au statut `Active` (et par `domain` si fourni). Read le corps complet de chaque décision Active.
3. Retourner la liste structurée : slug, domaine, décision retenue, conséquences. C'est le contexte anti-écrasement.

### create_decision(id, slug, domain, content, options=None, consequences=None)
1. Lire `config.example.md` : vérifier que `domain` est une valeur autorisée.
2. Read `Décisions/_Index.md` : si une décision **Active** existe déjà sur le même `slug`, REFUSER et rediriger vers `revise_decision`.
3. Construire le fichier `YYYY-MM-DD-<slug>.md` depuis `templates/decision-template.md` : frontmatter `Statut: Active`, `Révise: ""`, `Révisé par: ""` ; corps Contexte / Options / Décision retenue / Conséquences (Décision et Conséquences obligatoires).
4. Valider le frontmatter (règle dure 3). Write le fichier.
5. **Régénérer `Décisions/_Index.md` puis `_memory/_Index.md`** (règle dure 2).
6. Logguer l'opération (`log_action`).

### revise_decision(id, old_decision_path, new_slug, new_content, ...)
Ne jamais éditer le corps de l'ancienne décision (règle dure 1).
1. Read l'ancienne décision (`old_decision_path`). **Si son statut n'est pas `Active` : REFUSER l'opération et expliquer l'état actuel.** Ne pas réviser une décision déjà `Révisée` ou `Abrogée`.
2. Créer la nouvelle décision (`YYYY-MM-DD-<new_slug>.md`, `Statut: Active`, `Révise: <old_decision_path>`). Write.
3. **Edit du frontmatter de l'ancienne uniquement** : `Statut: Active` -> `Révisée`, `Révisé par: <chemin de la nouvelle>`. Ne pas toucher au corps de l'ancienne.
4. Valider les deux frontmatters. Régénérer `Décisions/_Index.md` puis `_memory/_Index.md`.
5. Logguer l'opération (`log_action`).

### abrogate_decision(id, old_decision_path, reason)
1. Read l'ancienne décision. **Si son statut n'est pas `Active` : REFUSER et expliquer l'état actuel.**
2. **Edit du frontmatter uniquement** : `Statut` -> `Abrogée`. Pas de `Révisé par` (pas de remplacement). Ne pas toucher au corps.
3. Régénérer `Décisions/_Index.md` puis `_memory/_Index.md`.
4. Logguer l'opération avec `reason` (`log_action`).

### log_action(id, agent, skill, action_meta)
1. Construire `YYYY-MM-DD-<slug-action>.md` depuis `templates/log-template.md` (frontmatter Log + corps : Action / Inputs lus / Décisions actives consultées / Modifications / Sources / Checks / Sortie).
2. Valider le frontmatter. Write (nouveau fichier, append-only, règle dure 4).
3. Régénérer `Logs/_Index.md` puis `_memory/_Index.md`.

### create_synthesis(id, jalon, content)
1. Lire `config.example.md` : vérifier que `jalon` est autorisé.
2. Construire `YYYY-MM-DD-<slug-jalon>.md` depuis `templates/synthesis-template.md`. Valider le frontmatter. Write.
3. Régénérer `Synthèses/_Index.md` puis `_memory/_Index.md`.
4. Logguer l'opération (`log_action`).

### update_synthesis(id, synthesis_path, content_delta)
Une synthèse est Warm (permanent évolutif), donc l'Edit in-place est autorisé ici (contrairement aux décisions Cold).
1. Read la synthèse. Edit pour annoter/compléter avec `content_delta`. Mettre à jour la `Date` si pertinent.
2. Régénérer `Synthèses/_Index.md` puis `_memory/_Index.md`.
3. Logguer l'opération (`log_action`).

### read_synthesis(id, jalon=None)
1. Read `Synthèses/_Index.md`. Read la synthèse du `jalon` demandé, ou la plus récente si `jalon=None`. Retourner le contenu. Lecture seule.

### read_logs(id, limit=N, agent=None)
Lecture seule de la couche Hot, pour reconstituer la trace d'un run ou préparer une synthèse de jalon.
1. Read `Logs/_Index.md`. Read les N logs les plus récents (ou filtrés par `agent`). Retourner la liste structurée.

### purge_logs(id, threshold_days, aggregate_to=None)
1. Lire la politique de purge dans `config.example.md`.
2. Identifier les logs au-delà du seuil. **Avant suppression** : si `aggregate_to` est fourni (ou par défaut selon config), `create_synthesis`/`update_synthesis` pour condenser les logs anciens en une synthèse Warm.
3. Supprimer les fichiers de log au-delà du seuil. Régénérer `Logs/_Index.md` puis `_memory/_Index.md`.
4. Logguer la purge (`log_action`) : plage de dates supprimée, nombre de fichiers, chemin de la synthèse d'agrégation. Ce log est lui-même soumis à la purge future.

### rebuild_indexes(id)
Utilitaire de récupération : régénère tous les index à partir du contenu réel des dossiers.
1. Pour chaque sous-dossier, lister les fichiers `.md` (hors `_Index.md`), lire leur frontmatter, reconstruire l'`_Index.md` (cf. `templates/index-template.md`).
2. Reconstruire le `_memory/_Index.md` racine (Scope: top) en agrégeant les trois.

### lint_memory(id, mode=quick)
Health-check du substrat. **Corrige automatiquement la dérive d'index (déterministe, sûr) ; tout le reste est une PROPOSITION, jamais une action structurante silencieuse.**

Mode `quick` (défaut, ~30 s) :
1. **Dérive d'index** : pour chaque sous-dossier (`Décisions/`, `Synthèses/`, `Logs/`), comparer le compteur déclaré dans `_Index.md` au nombre réel de `.md` (hors `_Index.md`), et la liste indexée aux fichiers présents. Idem pour le `_memory/_Index.md` racine vs la somme des trois. **Écart -> corriger via `rebuild_indexes`** (c'est la seule auto-correction autorisée).
2. **Conformité frontmatter** : valider chaque fichier contre `references/frontmatter-standards.md` (champ obligatoire manquant, valeur énumérée invalide, date non `YYYY-MM-DD`). Non conforme -> signaler (ne pas réécrire le corps).
3. **Intégrité Cold** : pour chaque décision, vérifier la cohérence des liens de statut (`Révise` pointe vers un fichier existant ; une `Révisée`/`Abrogée` n'est pas restée `Active` ; `Révisé par` pointe vers une décision `Active`). Incohérence -> signaler.
4. **Liens cassés** : tout `[[cible]]` dont le fichier n'existe pas -> signaler.

Mode `full` (~quelques min) : quick +
5. **Décisions Active contradictoires** : repérer deux décisions `Active` du même `Domaine` qui se contredisent (signal de `revise_decision`/`abrogate_decision` à proposer).
6. **Logs au-delà du seuil de purge** (cf. `config.example.md`) non encore agrégés en synthèse -> proposer `purge_logs` avec agrégation.
7. **Décisions Active orphelines** : aucune synthèse ni log récent ne les mentionne (conviction possiblement périmée) -> proposer une revue.

Sortie : un rapport structuré (tableau : check / statut OK-Corrigé-À revoir / détail). Les corrections d'index appliquées sont listées. Tout le reste est une liste de propositions. Logguer le lint (`log_action`, action=lint).

### operator_run(id, cadence=hebdo)
Passe de maintenance autonome sur le `_memory/`. **Une invocation = un run = un rapport = stop.** Pas de question en cours de run, pas de boucle.

Trois cadences (`hebdo`, `dreams`, `jalon`), détaillées dans `references/operator-cadences.md`. **Lire ce référentiel avant d'exécuter.** En résumé :
- `hebdo` : heartbeat léger (lint full + check conviction + détection de proximité de jalon). Log court de propositions.
- `dreams` : re-lecture froide profonde, produit une synthèse + propositions. Cadence mensuelle.
- `jalon` : même passe profonde que `dreams`, déclenchée par l'arrivée à un jalon ; la synthèse porte le jalon correspondant.

Règle dure transverse : l'operator **propose**, l'humain dispose. Ne JAMAIS créer/réviser/abroger une décision ni écrire une synthèse de fond sans validation. Failure handling et idle-timeout : si une étape échoue ou n'avance pas, la logguer et continuer le run.

## Routines de maintenance & programmation (HITL)

`lint_memory` et `operator_run` peuvent tourner à la demande, ou être **programmés**. La programmation passe par une question explicite à l'humain (l'agent appelant, en contexte interactif, porte l'`AskUserQuestion` ; ce skill ne programme jamais rien seul).

**Quand poser la question** : à la fin de `init_memory` (création d'un nouveau projet) **en contexte Cowork uniquement**, et sur demande explicite ("programme une routine", "planifie un lint").

**Mécanisme et défauts** : voir `references/operator-cadences.md` (section Scheduling). En Cowork, proposer `hebdo` (hebdo) + `dreams` (mensuel) via le mécanisme de routines Cowork ; `jalon` reste événementiel. En Claude Code local, pas de scheduling autonome pour l'instant (routines on-demand).

**Principe** : les routines produisent des **propositions dans un log**, jamais des actions structurantes silencieuses. Sortie 100 % dans le `_memory/` du projet (logs + cascade d'index), aucune notification externe par défaut. Démarrer en manuel quelques cycles, basculer en planifié seulement après accord humain.

## Concurrence

En cas de sous-agents concurrents, sérialiser les écritures (un agent finit son opération, index compris, avant qu'un autre n'écrive dans le même dossier). Un garde-fou `.lock` déterministe par dossier `_memory/` peut être ajouté si une corruption d'index sous concurrence est observée ; il n'est pas dans le périmètre par défaut.

## Discipline côté consommateurs

La discipline "lire les décisions Active AVANT toute modification de livrable" est portée par les agents/skills consommateurs, pas par ce skill. Ici, `read_active_decisions` se contente de fournir le contexte ; c'est l'agent appelant qui doit l'invoquer en premier.

Convention de logging : les opérations qui écrivent dans `Décisions/` ou `Synthèses/`, ainsi que `purge_logs`, s'auto-logguent (dernière étape de leur séquence) pour l'auditabilité. Le logging de l'activité métier plus large (paragraphes touchés dans le livrable, sources mobilisées par une section) reste à la charge de l'agent appelant via `log_action`.
