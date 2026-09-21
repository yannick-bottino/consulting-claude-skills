---
name: file-naming-standard
description: >
  Applique automatiquement la convention de nommage de fichiers du cabinet AVANT de
  livrer tout fichier produit (xlsx, docx, pptx, pdf, csv, png, zip, ...) dans un
  chat ou une session Cowork. Format :
  "Client x Cabinet_Mission - Livrable_YYYYMMDD". À déclencher
  proactivement dès qu'un livrable est sur le point d'être présenté ou sauvegardé
  (juste avant present_files, ou avant écriture dans /mnt/user-data/outputs),
  même si l'utilisateur ne le demande pas. Détecte le client et la mission dans
  le CLAUDE.md, ou à défaut dans le contexte projet / la conversation, et ne les
  invente JAMAIS. Déclencheurs explicites : "nomme le fichier", "renomme avant
  livraison", "convention de nommage", "applique le naming standard",
  "file naming", "comment nommer ce livrable", "/file-naming-standard".
  Couvre les livrables internes (sans client) et les collisions de noms le même
  jour.
---

# file-naming-standard

## Objectif

Renommer tout fichier produit selon la convention du cabinet juste avant de le
livrer, pour que le destinataire reçoive un nom lisible, daté, traçable, et
ouvrable sans friction sur sa machine (Windows + SharePoint/OneDrive compris).

## La convention

Template exact :

```
<Client> x <Cabinet>_<Mission> - <Livrable>_YYYYMMDD.<ext>
```

Exemple :

```
Meridian Retail x Acme Consulting_Transformation IA - Diagnostic de maturité_20260616.pptx
```

### Configurer le nom du cabinet

`<Cabinet>` est le seul bloc propre a votre organisation. Le definir une fois :

- variable d'environnement `FIRM_NAME` (lue par `scripts/build_filename.py`), ou
- option `--firm "Mon Cabinet"` sur le script, ou
- une ligne dans le `CLAUDE.md` du projet : `Cabinet : Mon Cabinet`.

Sans configuration, le script ecrit `Firm`. Tout le reste de la convention est
independant de l'organisation.

Composants, dans l'ordre :

| Bloc | Séparateur qui suit | Note |
|------|---------------------|------|
| `<Client>` | ` x ` (espace-x-espace) | nom du client, lisible |
| `<Cabinet>` | `_` | nom du cabinet, littéral, toujours présent |
| `<Mission>` | ` - ` (espace-tiret-espace) | nom de la mission |
| `<Livrable>` | `_` | intitulé du livrable en cours |
| `YYYYMMDD` | `.` | date du jour de livraison |
| `<ext>` | — | extension d'origine, inchangée |

**Pourquoi ` - ` et pas ` : ` (séparateur Mission/Livrable).** Le `:` est un
caractère interdit dans les noms de fichiers sous Windows (`< > : " / \ | ? *`)
et il est rejeté/remplacé à la synchronisation SharePoint et OneDrive. Comme les
livrables partent quasi systématiquement chez des clients en environnement
Microsoft 365, le `:` rendrait le fichier inouvrable ou tronqué côté client. Le
` - ` est un trait d'union simple (pas un em-dash), lu de manière équivalente, et
légal sur tous les systèmes. C'est la seule entorse à la spec d'origine, et elle
est non négociable pour des raisons techniques.

## Règles de caractères

Avant assemblage, nettoyer chaque composant (Client, Mission, Livrable) :

- **Supprimer / remplacer par un espace** les caractères interdits :
  `< > : " / \ | ? *` et les caractères de contrôle.
- **Conserver les accents et les espaces** (livrables clients francophones :
  `maturité`, `Données ESG`). Ne pas forcer le kebab-case ni le snake_case.
- **Normaliser les espaces** : pas de double espace, pas d'espace en début/fin.
- **Pas de point ni d'espace en fin de nom** (Windows les tronque).
- **Longueur** : si le nom complet dépasse ~255 caractères, raccourcir
  l'intitulé du livrable (jamais le client ni la date).

Si un pipeline aval exige de l'ASCII strict (script fragile, ancien système),
proposer une variante sans accents, mais ce n'est pas le défaut.

## Détecter le client et la mission

Chercher dans cet ordre de priorité. **Ne jamais inventer une valeur.**

1. **CLAUDE.md** (racine du projet, ou emplacement standard cowork). Scanner,
   dans l'ordre :
   - des champs explicites : lignes commençant par `Client`, `Mission`,
     `Nom de mission`, `Projet`, `Compte` (avec `:` ou `=`) ;
   - le titre H1 du fichier (souvent `# <Client> - <Mission>` ou
     `# Projet <Client>`) ;
   - une section `## Contexte` / `## Contexte projet`.
2. **Contexte projet / conversation** si absent du CLAUDE.md : instructions du
   projet Claude, brief ou cahier des charges uploadé, premiers messages où
   l'utilisateur nomme le compte et la mission.
3. **Demander** si rien de fiable ne ressort, OU si plusieurs candidats sont
   plausibles (ne pas trancher seul) :
   > "Pour nommer le livrable : quel est le **client** et le nom de la
   > **mission** ? (je n'ai pas trouvé de valeur fiable dans le CLAUDE.md ni le
   > contexte)"

Le livrable (`<Livrable>`), lui, vient de la tâche en cours (ce que Claude est en
train de produire) : "Diagnostic de maturité", "Compte-rendu COMEX", "Modèle
LBO", etc. Le déduire de la demande ; si ambigu, proposer un intitulé court et
demander validation en une ligne.

## Cas particuliers

- **Livrable interne (pas de client externe).** `<Cabinet> x <Cabinet>` n'a pas de
  sens. Si le client est absent, vaut le nom du cabinet / "interne" / "internal" :
  produire `<Cabinet>_<Mission> - <Livrable>_YYYYMMDD.<ext>` (on retire le bloc
  `<Client> x `).
- **Collision le même jour.** La date seule ne distingue pas deux livrables
  produits le même jour : risque d'écrasement silencieux. Si un fichier de même
  nom existe déjà dans le dossier cible, suffixer `_v2`, `_v3`, ... avant
  l'extension. Ne PAS ajouter `_v1` au premier (rester fidèle à la spec).
- **Fichier déjà conforme.** Si le fichier porte déjà un nom respectant la
  convention (même client, mission, date du jour), ne pas le renommer en boucle.
- **Plusieurs livrables dans une même session.** Appliquer la convention à
  chacun, en faisant varier `<Livrable>` (et `_vN` si collision).

## Quand déclencher

Juste avant de rendre un fichier : avant `present_files`, ou avant d'écrire le
fichier final dans `/mnt/user-data/outputs` (chat) ou le dossier de livraison
(Cowork). Le renommage s'applique au nom final livré, pas aux fichiers de travail
intermédiaires en `/home/claude`. Appliquer proactivement, sans attendre une
demande explicite, dès qu'un livrable client ou interne est produit.

## Script helper (déterministe)

Pour un nommage déterministe (sanitisation, date, interne, collision gérés en
code plutôt qu'à la main), utiliser `scripts/build_filename.py` :

```bash
FIRM_NAME="Mon Cabinet" python scripts/build_filename.py \
  --client "Meridian Retail" \
  --mission "Transformation IA" \
  --deliverable "Diagnostic de maturité" \
  --ext pptx \
  [--date 20260616] \
  [--ascii] \
  [--collision-dir /mnt/user-data/outputs]
```

Le script imprime le nom final sur stdout. Sans `--date`, il prend la date du
jour. Sans client (ou client = nom du cabinet / "interne"), il bascule en mode interne.
Avec `--collision-dir`, il vérifie le dossier et suffixe `_vN` si besoin.

Le séparateur Mission/Livrable est défini une seule fois en tête du script
(`SEP_MISSION_LIVRABLE`) : pour revenir à un autre séparateur, le changer là.

Le script est un accélérateur. En l'absence d'exécution de code (chat simple),
appliquer la convention en suivant les règles ci-dessus à la main : le résultat
doit être identique.

## Erreurs fréquentes

- **Laisser un `:` (ou tout caractère interdit) dans le nom final** : le fichier
  devient inouvrable côté client Windows / SharePoint. Toujours nettoyer.
- **Inventer un nom de client ou de mission** introuvable : un mauvais nom de
  compte sur un livrable est une faute professionnelle. Demander plutôt que
  deviner.
- **Renommer les fichiers de travail intermédiaires** : la convention ne
  s'applique qu'au livrable final présenté à l'utilisateur.
- **Oublier le mode interne** et produire `<Cabinet> x <Cabinet>_...`.
- **Écraser un livrable du même jour** faute de gérer la collision.
- **Replier les accents en ASCII par défaut** : on les conserve, sauf besoin
  explicite d'un pipeline aval.
