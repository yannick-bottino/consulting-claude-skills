---
name: project-lint
description: >
  Use when auditing an existing project folder for structural compliance with
  project-init guidelines (pilote de session + substrat de mémoire 3 couches).
  Trigger phrases: "vérifie le dossier projet", "le dossier est-il conforme", "audit projet",
  "check project setup", "lint projet", "est-ce que la structure est correcte", onboarding d'un
  nouveau membre sur un projet existant, ou après des modifications structurelles du dossier.
---

# project-lint

## Objectif

Vérifier la conformité d'un dossier projet (créé via `project-init`), lister les écarts
avec niveaux de sévérité, proposer les corrections, les appliquer après confirmation.

Ne pas modifier `/project-init` ni `/project-memory` -- ce skill est leur
complément ponctuel d'audit.

> Périmètre : ce lint vérifie la **conformité du setup** (les bons fichiers sont là, bien
> formés). La **santé interne du substrat** (dérive d'index, intégrité Cold, frontmatters)
> est du ressort de `lint_memory` (dans `project-memory`). Ce skill **délègue** la
> partie profonde à `lint_memory` plutôt que de la réimplémenter.

## Phase 1 — Checks structurels

Exécuter les vérifications suivantes :

| # | Vérification | Critère | Sévérité si KO |
|---|---|---|---|
| 1 | CLAUDE.md présent | Fichier à la racine | critique |
| 2 | CLAUDE.md ≤ 200 lignes | Cible : 200 lignes max | majeur (201-300L) / critique (>300L) |
| 3 | `_memory/` présent | Dossier substrat à la racine | critique |
| 4 | Sous-dossiers substrat | `_memory/Décisions/`, `_memory/Synthèses/`, `_memory/Logs/` présents | critique |
| 5 | `_memory/context.md` présent | Fichier de métadonnées mission | majeur |
| 6 | `_memory/CLAUDE.md` présent | Règles de routage du substrat | majeur |
| 7 | Index présents | `_memory/_Index.md` + un `_Index.md` par sous-dossier | majeur |
| 8 | claude_tasks/TODO.md présent | Fichier dans claude_tasks/ | critique |
| 9 | Pas de MEMORY.md résiduel | Si un `MEMORY.md` plat existe à la racine → vestige de l'ancien setup à migrer vers le substrat | majeur |
| 10 | Section Équipe dans CLAUDE.md | Table `\| Username \| Prénom \|` présente avec ≥1 ligne remplie | majeur |
| 11 | Sections TODO.md | TODO / IN PROGRESS / DONE présentes | majeur |
| 12 | Attributions + @owner TODO.md | Tâches portant `[date | @auteur]` et un `@owner` | mineur |

> Check 9 (MEMORY.md résiduel) : le nouveau setup remplace le `MEMORY.md` plat par le substrat
> 3 couches. Un `MEMORY.md` présent signale un dossier initialisé avec l'ancien `cowork-init`.
> Proposer la migration de son contenu vers `Décisions/` (décisions actées) / `Synthèses/`
> (réflexions) avant suppression. Ne jamais supprimer son contenu sans l'avoir reversé.

## Phase 1bis — Santé du substrat (délégation)

Si `_memory/` est présent et structurellement valide, lancer `lint_memory quick` (skill
`project-memory`) et intégrer son rapport (dérive d'index auto-corrigée, conformité
frontmatter, intégrité Cold, liens cassés) à la sortie de la Phase 2.

## Phase 2 — Rapport d'écarts

Produire exactement ce format :

```
## Rapport de conformité — [nom du dossier]

✅ Conforme (X/12 vérifications structurelles)
🩺 Santé substrat : [résumé lint_memory : index OK/corrigés, N frontmatters à revoir...]
⚠️  Écarts détectés :

1. [critique] CLAUDE.md absent
   → Action : créer le setup via /project-init
2. [majeur] MEMORY.md résiduel détecté (ancien setup)
   → Action : migrer son contenu vers _memory/ (Décisions / Synthèses) puis supprimer
3. [mineur] 3 tâches TODO.md sans @owner
   → Lignes concernées : 12, 18, 24
```

Niveaux :
- `critique` — fonctionnement projet bloqué
- `majeur` — fonctionnement dégradé
- `mineur` — non-conformité cosmétique

## Phase 3 — Apply fixes

> Les messages entre guillemets ci-dessous sont des prompts à adresser à l'utilisateur.

1. Lister les actions concrètes avec fichiers et lignes concernées
2. Demander confirmation globale : "Je vais appliquer X corrections. Confirmes ?"
3. N'appliquer qu'après confirmation explicite
4. Appliquer atomiquement (une action = un fichier modifié)
5. Confirmer chaque modification : "✅ [action effectuée]"

**Cas CLAUDE.md > 200 lignes :**
Ne pas modifier CLAUDE.md directement. Proposer à la place :
> "CLAUDE.md fait X lignes (cible : 200). Veux-tu que je lance
> `/instructions-audit` pour un audit de gouvernance et un refactor ?"

Attendre confirmation. Si oui, lancer `/instructions-audit`.

**Cas MEMORY.md résiduel :**
Ne jamais supprimer le `MEMORY.md` sans avoir reversé son contenu. Proposer :
> "MEMORY.md (ancien setup) contient N entrées. Je peux migrer les décisions actées vers
> `_memory/Décisions/` et les réflexions vers `_memory/Synthèses/` via project-memory,
> puis supprimer le fichier. Confirmes ?"

**Cas dérive d'index / substrat :**
Déléguer à `lint_memory` (qui auto-corrige la dérive d'index de façon déterministe et signale le reste). Ne pas réécrire les fichiers du substrat à la main depuis ce skill.

## Erreurs fréquentes

- **Appliquer des fixes sur CLAUDE.md > 200 lignes directement** : toujours déléguer à `/instructions-audit`.
- **Supprimer un MEMORY.md résiduel sans migrer son contenu** : la migration précède toujours la suppression.
- **Réimplémenter le check de substrat** : déléguer à `lint_memory`, ne pas dupliquer.
- **Lancer le lint sur le mauvais dossier** : vérifier que le dossier cible est bien un projet (créé via `/project-init`), pas un référentiel de skills ou un dossier quelconque.
- **Confirmer un apply global sans relire la liste** : si des écarts `critique` sont présents, les signaler explicitement avant de demander confirmation globale.
