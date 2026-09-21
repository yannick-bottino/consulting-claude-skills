# Prompt — Phase 2 : Refactor CLAUDE.md

Tu es un expert en gouvernance de contexte pour agents IA.

Tu vas refactorer un fichier CLAUDE.md projet pour passer d'une version
obèse à une version lean, en extrayant le contenu non-critique vers les
bons fichiers annexes.

Référence officielle :
https://code.claude.com/docs/en/memory
(cible par défaut : ≤ 100 lignes par CLAUDE.md projet)

## Entrée 1 : le fichier actuel

[CONTENU DU CLAUDE.MD PROJET — injecté automatiquement par le skill]

## Entrée 2 : le rapport d'audit

[RAPPORT DE LA PHASE 1 — injecté automatiquement]

## Ce que je veux en retour

Produis exactement ces 7 livrables, dans cet ordre :

### 1. Architecture cible

Arborescence complète du système refactorisé :

```
mon-projet/
├── CLAUDE.md           (X lignes)
├── MEMORY.md
├── claude_tasks/
│   └── TODO.md
└── .claude/
    ├── rules/
    │   └── ...
    ├── skills/
    │   └── ...
    └── agents/
        └── ...
```

### 2. CLAUDE.md lean (version complète)

Contenu complet du nouveau CLAUDE.md, prêt à coller.
Structure suggérée (conserver la structure existante si le projet en a une établie) :

```
# [Nom du projet]

## WHY
[2-3 phrases max]

## WHAT
[Bullet list : composants principaux]

## HOW
[Workflow 3-5 étapes MAX, références vers rules/ et skills/]

## RÈGLES NON-NÉGOCIABLES
[5-10 règles, une ligne chacune]

## CONVENTIONS
[Nommage, langue, formats]
```

> Si le fichier source a une structure établie, la conserver. Réorganiser, ne pas réécrire.

Cible stricte : ≤ 100 lignes. Si dépassement → extraire davantage.

### 3. Fichiers annexes à créer

Pour chaque fichier : chemin complet + contenu complet prêt à coller.
3 à 6 fichiers max. Regrouper si nécessaire.
Jamais de placeholders ou "[à compléter]" dans les contenus.

### 4. Commandes shell

```bash
mkdir -p .claude/rules .claude/skills .claude/agents
# une commande par fichier à créer
```

### 5. Changelog

| Ancien emplacement (section/lignes) | Nouveau fichier | Raison |
|---|---|---|

### 6. Contenu supprimé

Liste des sections SUPPRIMÉES (pas déplacées) avec justification en 1 ligne.

### 7. Checklist post-refactor

- [ ] CLAUDE.md projet fait ≤ 100 lignes
- [ ] Lancer /memory dans Claude Code — vérifier que les fichiers chargent
- [ ] Tester une session : Claude résume-t-il correctement le projet ?
- [ ] Vérifier que les fichiers annexes sont accessibles depuis le projet
- [ ] [ajouter les vérifications spécifiques au projet]

Règle absolue : ne pas réécrire le contenu pour "améliorer" — réorganiser
seulement. Si une ligne est à garder, garde-la mot pour mot.
