# Standards de frontmatter

> Les 4 types de fichiers du substrat portent un frontmatter YAML standardisé. **Règle dure : ne jamais écrire un fichier dont le frontmatter est incomplet ou non conforme.** Si un champ obligatoire manque, le compléter avant d'écrire (refus d'écriture sinon). Les valeurs énumérées de `Domaine` et `Jalon` sont définies dans `config.example.md`.

## Décision (Cold)

```yaml
---
Type: Décision
Date: YYYY-MM-DD
Statut: Active | Révisée | Abrogée
Domaine: <une valeur de la liste config.example.md>
Auteur: <user>
Révise: <chemin-decision-precedente> | ""
Révisé par: <chemin-decision-suivante> | ""
---
```

Règles de cohérence :
- Une décision nouvellement créée est toujours `Statut: Active`, `Révise: ""` (ou le chemin de celle qu'elle révise), `Révisé par: ""`.
- Quand une décision est révisée : son `Statut` passe à `Révisée` et son `Révisé par` pointe vers la nouvelle. La nouvelle porte `Révise: <chemin de l'ancienne>`.
- Quand une décision est abrogée : son `Statut` passe à `Abrogée`. Pas de `Révisé par` (pas de remplacement).
- `Révise` et `Révisé par` sont des chemins relatifs au dossier `Décisions/` (ex : `2026-06-15-perimetre-mission.md`).

## Synthèse (Warm)

```yaml
---
Type: Synthèse
Date: YYYY-MM-DD
Jalon: <une valeur de la liste config.example.md>
Auteur: <agent ou user>
---
```

## Log (Hot)

```yaml
---
Type: Log
Date: YYYY-MM-DD
Agent: <nom-agent>
Skill: <nom-skill>
Action: <slug-action>
---
```

## Index

```yaml
---
Type: Index
Scope: top | leaf
Description: <description courte>
Dernière mise à jour: YYYY-MM-DD
---
```

`Scope: top` pour le `_memory/_Index.md` racine, `Scope: leaf` pour les `_Index.md` de `Décisions/`, `Synthèses/`, `Logs/`.

## Validation avant écriture

Avant tout Write d'un fichier de mémoire :
1. Le `Type` correspond au dossier cible (Décision -> `Décisions/`, etc.).
2. Tous les champs obligatoires du type sont présents et non vides (sauf `Révise`/`Révisé par` qui acceptent `""`).
3. Les champs énumérés (`Statut`, `Domaine`, `Jalon`, `Scope`) prennent une valeur autorisée.
4. La `Date` est au format `YYYY-MM-DD`.

Si une vérification échoue, corriger le frontmatter avant d'écrire. Ne jamais persister un fichier non conforme : il polluerait le substrat et fausserait les index.
