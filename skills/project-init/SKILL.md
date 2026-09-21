---
name: project-init
description: >
  Point d'entrée pour initialiser et reprendre la mémoire persistante partagée d'une
  mission de conseil, en Cowork ou en projet Claude Code. Crée le pilote de session
  (CLAUDE.md) et le suivi de tâches (claude_tasks/TODO.md), et délègue à project-memory
  le substrat de mémoire 3 couches (_memory/). Utiliser dès qu'on ouvre un nouveau projet et
  qu'on veut un suivi partagé, ou quand l'utilisateur dit : "initialise le projet", "crée la
  mémoire projet", "setup projet", "init projet", "mets en place le suivi", "on part de zéro
  sur ce dossier", "prépare le dossier pour bosser à plusieurs", "mémoire partagée", "session
  handoff". Déclencher aussi sur "reprenons" ou "on en était où" dans un dossier contenant déjà
  un CLAUDE.md : dans ce cas, ne pas réinitialiser mais lire l'existant et faire le point.
---

# Project Init -- Mémoire persistante partagée

## Objectif

Permettre à n'importe qui ouvrant une session sur un dossier projet de :
1. Savoir exactement où en est le projet (décisions, état de conviction, tâches)
2. Reprendre le travail sans perdre le contexte des sessions précédentes
3. Contribuer à la mémoire collective sans effort supplémentaire

Ce skill est le **point d'entrée** du cycle de vie d'un projet. Il s'appuie sur le **moteur** `project-memory` (substrat de mémoire 3 couches) pour toute la mémoire de fond, et conserve un pilote de session léger (`CLAUDE.md`) + un suivi de tâches (`TODO.md`).

> Architecture mémoire : la mémoire de fond (décisions, réflexions, traces) vit dans le substrat 3 couches géré par `project-memory` (`_memory/`). Ce skill ne crée PAS de `MEMORY.md` plat : le substrat le remplace, parce qu'une décision structurante doit avoir un foyer canonique unique (sinon elle dérive). Le `TODO.md` reste séparé : c'est l'axe "tâches / qui fait quoi", orthogonal à la mémoire.

---

## Deux modes de fonctionnement

### Mode INIT (première fois)
Déclenché quand le dossier ne contient pas encore de `CLAUDE.md`.

### Mode REPRISE
Déclenché quand le dossier contient déjà un `CLAUDE.md`.
Dans ce cas : lire CLAUDE.md + le substrat (`_memory/`) + TODO.md, faire une synthèse à l'utilisateur, et proposer de continuer.

---

## Mode INIT : étape par étape

### 1. Identifier l'utilisateur

Détecter automatiquement le nom système via `whoami` ou `$USER`.
- Si une correspondance `username -> prénom` existe déjà dans CLAUDE.md (section Équipe), l'utiliser directement.
- Sinon, proposer : "Je te détecte comme [username]. C'est sous quel prénom que tu veux apparaître dans la mémoire projet ?"
- Stocker la correspondance dans la section Équipe du CLAUDE.md pour les prochaines sessions.

Stocker le prénom comme `@NomUtilisateur` pour toute la session.

### 2. Comprendre le projet

Poser 2-3 questions courtes :
- C'est quoi ce projet / cette mission en une phrase ?
- Qui d'autre va travailler dessus ?
- Il y a des conventions ou des règles spécifiques à respecter ?

Ces réponses servent au remplissage du `CLAUDE.md`, du `context.md` du substrat, **et au tailoring éventuel de la taxonomie** (cf. étape 6).

### 3. Proposer l'analyse du dossier (optionnel)

Si le dossier contient des fichiers existants (PDF, DOCX, PPTX, XLSX...), proposer :

> 📂 **Analyse du dossier**
>
> Je peux analyser tous les documents présents dans ce dossier pour créer
> un index structuré (un miroir en Markdown de chaque fichier). Ça me
> permettra de mieux comprendre le contenu existant et de t'aider plus
> efficacement dans les prochaines sessions.
>
> **Ce que ça fait** : je lis chaque document et j'en crée une version
> Markdown légère dans un sous-dossier `_parsed/`.
>
> **Ce que ça coûte** : c'est gourmand en ressources. Pour un dossier
> de 20+ documents, ça peut consommer une part significative de ta
> capacité de session. Si ton dossier est petit (< 5 fichiers) ou si
> tu sais déjà ce qu'il contient, tu peux sauter cette étape.
>
> Tu veux que je lance l'analyse ?

Si oui, lancer le skill `/folder-analyzer-optimizer` sur le dossier courant.
Si non, passer à l'étape suivante.

### 4. Créer le pilote de session et le suivi de tâches

Créer à la racine du dossier projet :

#### CLAUDE.md

Le **pilote de comportement** de Claude pour toutes les sessions futures. **Moins de 200 lignes** en toutes circonstances (règle absolue).

```markdown
# [Nom du projet]

> [Description en une phrase]

## Règles de session

1. **À chaque ouverture de session** : lire ce fichier, puis le substrat de mémoire (`_memory/` -- voir son propre CLAUDE.md), puis claude_tasks/TODO.md. Faire une synthèse rapide à l'utilisateur de l'état du projet.

2. **Mémoire de fond -- substrat 3 couches (`_memory/`)** : toute la mémoire structurante passe par le moteur `project-memory`. Détection par langage naturel :
   - décision actée ("on a décidé que...", "on retient...", "on acte...") → `create_decision` (couche Cold, golden data immuable)
   - état de conviction / réflexion à un jalon → `create_synthesis` (couche Warm)
   - trace d'un run IA (ce qui a été lu/modifié/sourcé) → `log_action` (couche Hot)
   - **AVANT de réécrire un livrable** : `read_active_decisions` d'abord, ne jamais écraser une décision Active en silence.

3. **Tâches -- claude_tasks/TODO.md** : quand une tâche apparaît, change de statut, ou se termine, mettre à jour le TODO sans demander. Chaque tâche porte un `@owner` (qui la prend) en plus de l'attribution `[date | @auteur]`.
   - "il faut qu'on...", "pense à...", "à faire :" → ajout dans TODO
   - "c'est fait", "j'ai terminé..." → passage en DONE
   - "où on en est ?", "recap" → synthèse de l'état courant

4. **Routines de maintenance** : à l'ouverture de session, un `lint_memory quick` est bienvenu (auto-corrige la dérive d'index). Aux jalons, un `operator_run` produit une synthèse (propositions, jamais d'action silencieuse). Cf. `project-memory`.

5. **Attribution** : toute écriture dans le substrat ou le TODO porte la date et le `@NomUtilisateur`.

6. **Self-pruning du CLAUDE.md** : ce fichier ne dépasse JAMAIS 200 lignes. Si un ajout le ferait dépasser : fusionner les entrées redondantes, supprimer l'obsolète, déplacer le détail vers le substrat.

## Équipe

| Username système | Prénom |
|---|---|
| [rempli automatiquement à la première session de chaque membre] |

## Structure du dossier

- `CLAUDE.md` -- ce fichier (règles et contexte projet)
- `_memory/` -- substrat de mémoire 3 couches (Décisions / Synthèses / Logs), géré par project-memory
- `claude_tasks/TODO.md` -- suivi des tâches (avec @owner)
- `_parsed/` -- index Markdown des documents (si analyse lancée)
- [ajouter ici les sous-dossiers spécifiques au projet]

## Contexte projet

[Remplir avec les réponses de l'étape 2 : description, équipe, conventions]

## Comportements spécifiques

[Ajouter ici au fil du temps les "do / don't" appris en session]
```

#### claude_tasks/TODO.md

```markdown
# Suivi des tâches -- [Nom du projet]

> Ce fichier est maintenu automatiquement par Claude.
> Format : - [statut] [date | @auteur] (@owner) Description
> Statuts : [ ] = à faire, [~] = en cours, [x] = terminé
> @owner = la personne responsable de la tâche (permet de voir où en est chacun
> tout en gardant une source unique ; filtrer par @owner pour une vue par personne).

---

## TODO
_(aucune tâche pour le moment)_

## IN PROGRESS
_(aucune tâche pour le moment)_

## DONE
_(aucune tâche terminée)_
```

### 5. Bâtir le substrat de mémoire

Invoquer le moteur **`project-memory`**, opération `init_memory` :
- `id` = slug du projet
- `locale` = `fr` par défaut (ou la langue de travail)
- `context_meta` = les éléments de l'étape 2 (client, mission, équipe, date début)

Le moteur crée `_memory/` (3 couches + `context.md` + `_memory/CLAUDE.md` autoportant + cascade d'index). Ne pas réimplémenter cette logique ici : c'est la responsabilité du moteur.

### 6. Proposer le tailoring de la taxonomie (si mission atypique)

La taxonomie par défaut (`config.example.md` : domaines `cadrage/méthodo/hypothèse/livrable/arbitrage-client/autre`, jalons `kickoff/cadrage-validé/mi-parcours/pré-restitution/restitution/clôture/autre`) couvre la plupart des missions. Si le contexte découvert à l'étape 2 révèle une mission atypique (ESG DD, data strategy, brand, etc.), **proposer** d'ajuster les domaines/jalons à la mission. Sinon, conserver le défaut (cohérence inter-missions).

### 7. Proposer la programmation des routines (Cowork uniquement)

**Si le contexte est Cowork** : `project-memory` propose (via `AskUserQuestion`) de planifier les routines autonomes : `hebdo` (heartbeat hebdomadaire) + `dreams` (re-lecture profonde mensuelle). `jalon` reste événementiel. Cf. `project-memory/references/operator-cadences.md`.

**Si le contexte est Claude Code local** : ne pas proposer de scheduling autonome (les routines restent disponibles en on-demand). Le scheduling local sera câblé ultérieurement.

### 8. Confirmer

Afficher un récapitulatif :
> Projet initialisé. Voici ce qui a été créé :
> - `CLAUDE.md` : règles de session et contexte projet ([X] lignes)
> - `_memory/` : substrat de mémoire 3 couches (Décisions / Synthèses / Logs)
> - `claude_tasks/TODO.md` : suivi des tâches (vide)
>
> À partir de maintenant, je maintiens la mémoire (décisions, synthèses, logs) et les tâches au
> fil de notre travail. Tes collègues retrouveront tout le contexte en ouvrant une session ici.

---

## Mode REPRISE

Quand le dossier contient déjà un `CLAUDE.md` :

1. Identifier l'utilisateur : `whoami`, chercher la correspondance dans la section Équipe du CLAUDE.md. Si nouveau username, demander le prénom et l'ajouter à la table.
2. Lire `CLAUDE.md` (règles et contexte).
3. Lire le substrat via `project-memory` : `read_context`, `read_active_decisions` (décisions Active), `read_synthesis` (dernière synthèse de jalon).
4. Lire `claude_tasks/TODO.md` (tâches en cours et à faire).
5. Synthétiser à l'utilisateur :
   - Décisions actives clés
   - État de conviction (dernière synthèse)
   - Tâches en cours et à faire (avec @owner)
   - Toute info critique du CLAUDE.md
6. Optionnel : proposer un `lint_memory quick` pour rafraîchir les index.
7. Demander : "On reprend où ? Dis-moi sur quoi tu veux avancer."

---

## Gestion des conflits (multi-utilisateurs)

Le dossier peut être partagé (OneDrive, workspace Cowork) et plusieurs personnes peuvent travailler en parallèle :

- **Append-only** sur le TODO et la couche Hot du substrat : ne jamais réécrire le contenu existant, toujours ajouter.
- **Attribution systématique** : chaque ligne porte `[date | @auteur]`.
- **Déplacement de tâches** : quand on déplace une tâche de TODO vers IN PROGRESS ou DONE, on la retire de la section source et on l'ajoute dans la section cible. C'est la seule opération qui modifie des lignes existantes du TODO.
- **TODO en un seul fichier** : le besoin "savoir où en est chaque personne" est couvert par le champ `@owner` (vue consolidée filtrable), pas par un fichier par consultant. Ne pas fragmenter le TODO tant que des collisions OneDrive ne le justifient pas concrètement.
- En cas de conflit OneDrive détecté (contenu incohérent ou lignes dupliquées), signaler à l'utilisateur et proposer de résoudre manuellement.
