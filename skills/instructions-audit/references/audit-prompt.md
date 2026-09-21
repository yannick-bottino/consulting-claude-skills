# Prompt — Phase 1 : Audit CLAUDE.md

Tu es un expert en gouvernance de contexte pour agents IA.

Je vais te donner le contenu actuel de mon fichier d'instructions système
pour mon agent IA (CLAUDE.md). Ton job : faire un audit ligne par ligne
et identifier ce qui doit rester dans le fichier principal vs ce qui
doit être extrait ailleurs.

Référence officielle Anthropic :
https://code.claude.com/docs/en/memory
(cible par défaut : ≤ 100 lignes par CLAUDE.md projet)

## Règles d'audit

Applique ce filtre à chaque ligne/section :

1. **Constitution** (reste dans CLAUDE.md) : règles de base du projet,
   workflow par défaut, conventions de nommage, principes non-négociables,
   structure du projet. Ce qui doit être chargé à CHAQUE session, pour
   CHAQUE tâche.

2. **Savoir métier** (extraire vers skills/) : procédures multi-étapes,
   playbooks, expertises pointues sur un domaine précis. Ce qui est
   utile ponctuellement, pas à chaque message.

3. **Règles transverses** (extraire vers rules/) : règles qui s'appliquent
   à un type de fichier ou un contexte précis. Utilise le path-scoping
   si pertinent.

4. **Définitions d'agents** (extraire vers agents/) : descriptions détaillées
   de sous-agents, mandats, interactions entre agents. Le fichier principal
   garde juste une référence courte.

5. **Historique / Apprentissages** (extraire vers MEMORY.md ou LEARNINGS.md) :
   décisions passées, incidents, apprentissages datés. Le contexte vient
   du code et du git, pas du fichier d'instructions.

6. **Instructions génériques** (supprimer) : "sois poli", "réponds en
   français", "fais du bon travail", meta-instructions sans valeur
   actionnable.

## Contenu à auditer

[CONTENU DU CLAUDE.MD PROJET — injecté automatiquement par le skill]

## Ce que je veux en retour

Produis exactement cette structure :

### 1. Diagnostic global
- Nombre de lignes total : X
- Estimation de tokens consommés par session : X (lignes × 4)
- Cible (≤ 100 lignes) : OUI / NON (écart : +X lignes)
- % de bloat estimé : X%
- Verdict : LEAN / ACCEPTABLE / OBÈSE / CRITIQUE

### 2. Analyse par section
Pour chaque section/bloc du fichier, donne :
- Nom de la section
- Nombre de lignes
- Catégorie (1 à 6 ci-dessus)
- Verdict : GARDER / EXTRAIRE VERS [fichier cible] / SUPPRIMER
- Justification en 1 phrase

### 3. Top 5 quick wins
Les 5 extractions qui vont faire le plus gagner de lignes, triées par
impact décroissant. Format :
- "Extraire [section] (X lignes) vers [fichier]. Gain : X lignes."

### 4. Risques détectés
Signaux de gouvernance cassée :
- Contradictions entre instructions
- Règles obsolètes (dates dépassées, références mortes)
- Duplications
- Zones ambiguës qui laissent l'agent deviner

### 5. Plan de refactor recommandé
Ordre des opérations, 5 étapes max. Chaque étape = une action concrète.

Sois direct, chirurgical. Pas de politesses. Chaque recommandation doit
citer la section ou les lignes concernées.
