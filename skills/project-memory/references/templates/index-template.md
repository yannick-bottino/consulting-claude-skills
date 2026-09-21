---
Type: Index
Scope: leaf
Description: <description courte du dossier>
Dernière mise à jour: YYYY-MM-DD
---

# Index : <nom du dossier>

| Note | Date | Statut / Jalon | Domaine / Action |
|---|---|---|---|
| [<slug>](<slug>.md) | YYYY-MM-DD | <Active / jalon / -> | <domaine ou action> |

> Régénéré après chaque écriture dans le dossier. Pour `Décisions/`, la colonne Statut montre Active / Révisée / Abrogée. Pour `Synthèses/`, le Jalon. Pour `Logs/`, un tiret.

## Variante racine (`_memory/_Index.md`, Scope: top)

Le `_Index.md` racine agrège les trois sous-dossiers :

```
## Décisions (Cold)
<décisions Active en tête, puis Révisée/Abrogée>

## Synthèses (Warm)
<synthèses par jalon, ordre chronologique>

## Logs (Hot)
<derniers logs, ordre antéchronologique>
```
