# Template CLAUDE.md du substrat

> Ce fichier est le **modèle** du `CLAUDE.md` que `init_memory` dépose dans `<racine projet>/_memory/`. Il est lu par tout agent qui pénètre dans le dossier de mémoire. Substituer les `<placeholders>` à l'init, en **copiant les listes de domaines et de jalons depuis `config.example.md`** pour que le fichier soit autoportant.

---

## Contenu déposé (à instancier)

```markdown
# Mémoire mission : <id>

> Substrat de mémoire 3 couches. Lecture obligatoire avant toute modification d'un livrable de cette mission.

## Rituel d'entrée (obligatoire, dans cet ordre)

1. Lire `context.md` (métadonnées de la mission).
2. Lire `Décisions/_Index.md`, puis chaque décision au **statut Active**.
3. Avant d'écrire dans un livrable : vérifier qu'aucune modification ne contredit une décision Active.
   - Si conflit : STOP. Signaler à l'humain, proposer une révision (`revise_decision`) ou abrogation (`abrogate_decision`). Ne jamais écraser en silence.
   - Sinon : procéder, puis loguer l'action dans `Logs/`.

## Qu'est-ce qui va où

- **Décision structurante prise/validée par un humain** (golden data, ne doit jamais être écrasée) -> `Décisions/` (Cold, immuable). Domaines : <liste domaines copiée de config.example.md>.
- **Instantané de l'état de conviction à un jalon** -> `Synthèses/` (Warm). Jalons : <liste jalons copiée de config.example.md>.
- **Trace d'un run IA** (lu / modifié / sourcé / vérifié) -> `Logs/` (Hot, append-only).

## Règles dures

- Ne jamais éditer le corps d'une décision au statut Active. Seul flip de statut autorisé dans le frontmatter (via revise/abrogate). Réviser = nouveau fichier + flip de l'ancienne.
- Régénérer l'`_Index.md` du dossier touché après chaque écriture.
- Frontmatter conforme à `frontmatter-standards.md`, sinon ne pas écrire.

## Routines de maintenance

- À l'ouverture de session, un `lint_memory quick` est bienvenu (auto-corrige la dérive d'index).
- Aux jalons, un `operator_run` produit une synthèse de jalon (propositions, jamais d'action silencieuse).
- Cadences détaillées : voir le skill `project-memory` (`references/operator-cadences.md`).

## Métadonnées

- Scope : mission
- Identifiant : <id>
- Locale : <fr | en>
- Politique de purge des logs : <selon config.example.md>
```

---

## Notes d'instanciation

- Les listes `<liste domaines>` et `<liste jalons>` sont copiées depuis `config.example.md` au moment de l'init, pour que le `CLAUDE.md` du dossier soit autoportant (un agent qui entre n'a pas à aller chercher la config ailleurs).
- Le substrat se crée à la racine du dossier projet courant (`<racine projet>/_memory/`).
