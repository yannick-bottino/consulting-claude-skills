# Benchmark — Data Sourcing Guide

## Source Priority

| Priority | Source type | Trust level | Notes |
|----------|-------------|-------------|-------|
| 1 | Client documents in `sources/` folder | Highest | Cite file name + page |
| 2 | Actor's official website | High | Note retrieval date |
| 3 | Annual reports, investor presentations | High | Cite year |
| 4 | Industry studies (Xerfi, Frost & Sullivan, sectoral observatories) | Medium-high | Cite study + year |
| 5 | Comparison / aggregator sites | Medium | Note retrieval date, flag if >6 months |
| 6 | Press articles | Medium | Multiple sources preferred |
| 7 | Analyst estimates | Low | Must be explicit: `[ESTIMATION]` |

---

## Step 1: Read Client Documents

At session start (Phase 0 → Phase 1 transition):

1. List all files in the current project's `sources/` folder
2. For each `.pdf`, `.docx`, `.xlsx` found → read and extract relevant benchmark data
3. Tag extracted data with the source document name and page number
4. Quote directly rather than paraphrase when possible

Key things to extract from client documents:
- Existing pricing data or tariff tables
- Already-identified competitors
- Market context and sizing data
- Client's own positioning and strategy signals

---

## Step 2: Web Search Per Actor

For each actor, run this search sequence in order. Stop when you have sufficient data for each dimension.

**Search 1 — Official pricing:**
```
"[Actor name]" tarifs abonnement [current year]
"[Actor name]" prix mensuel offre [market segment]
```

**Search 2 — Product/offer details:**
```
"[Actor name]" offre [market segment] conditions générales inclus
"[Actor name]" assurance entretien [market keyword]
```

**Search 3 — Target & positioning:**
```
"[Actor name]" [B2B OR B2C] segment cible messaging
"[Actor name]" qui est concerné pour qui
```

**Search 4 — Recent news & key figures:**
```
"[Actor name]" chiffres clés flotte [current year]
"[Actor name]" presse annonce [current year]
```

Always record: exact URL + date of retrieval for every data point used.

---

## Step 3: Web Scraping — Architecture à 3 niveaux

Le skill utilise le meilleur scraper disponible, par ordre de priorité.
La détection est automatique au démarrage (Phase 0 du skill).

### Niveau 1 — Jina Reader (défaut, zéro setup)

**Quand :** pages HTML statiques, articles, pages produit sans JS complexe.
**Comment :**
```bash
python3 scripts/scrape.py <url>
# → appel automatique à https://r.jina.ai/<url>
```
Ou directement via curl :
```bash
curl -s "https://r.jina.ai/https://www.carvio.com/abonnement"
```
Jina Reader retourne du Markdown propre. Gratuit, sans installation, sans API key.

**Limites :** ne rend pas le JavaScript — pricing interactif ou SPAs React non accessibles.

---

### Niveau 2 — Crawl4AI (upgrade local, recommandé pour JS)

**Quand :** pricing pages dynamiques, SPAs, boutons "calculer le prix", contenu chargé en JS.
**Installation (une seule fois) :**
```bash
bash scripts/setup-scraper.sh
```
**Usage depuis le skill :**
```bash
python3 scripts/scrape.py <url>
# → détecte Crawl4AI, retourne "Fit Markdown" (boilerplate supprimé)
```
Crawl4AI utilise Playwright sous le capot. Retourne du Markdown optimisé LLM.

**Vérifier que Crawl4AI est disponible :**
```bash
python3 scripts/scrape.py --check
# → "scraper=crawl4ai" si installé, "scraper=jina" sinon
```

---

### Niveau 3 — WebSearch natif Claude (fallback)

**Quand :** ni Crawl4AI ni Jina Reader disponibles (pas de connexion, rate limit).
Utiliser les outils WebSearch natifs de Claude pour obtenir des extraits.
Mentionner dans le rapport : `[Source : WebSearch — extrait partiel, vérifier directement]`

---

### Quel niveau utiliser ?

| Type de page | Niveau recommandé |
|-------------|------------------|
| Page produit statique, article de presse | Jina Reader (niveau 1) |
| Simulateur de prix React/Vue | Crawl4AI (niveau 2) |
| Page avec formulaire "calculer mon tarif" | Crawl4AI (niveau 2) |
| Résultats de recherche, agrégateurs | Jina Reader (niveau 1) |
| Page bloquant les crawlers | Crawl4AI (niveau 2, gère mieux les user-agents) |
| Page accessible uniquement après login | WebSearch natif + mention N/D |

---

## Step 4: Source Citation Format

**In Markdown actor files**, always end with a Sources block:

```markdown
**Sources :**
- Prix mensuel observés : https://example.com/tarifs (consulté le 2026-03-15)
- Contenu du service (assurance incluse) : https://example.com/offre (consulté le 2026-03-15)
- Chiffres clés flotte : Rapport annuel 2025, p. 12
- Document client : `sources/etude-comparative.pdf`, p. 8
```

**In benchmark.json**, use the structured sources array (see output-schemas.md).

---

## Step 5: Missing Data Protocol

| Situation | Action | Marker |
|-----------|--------|--------|
| Data not found after 2+ searches | Mark and continue | `[N/D — non disponible publiquement]` |
| Data found but >12 months old | Use with date note | `[Données : MM/YYYY — à vérifier]` |
| Data estimated from secondary source | Mark with hypothesis | `[ESTIMATION — hypothèse : X, source : Y]` |
| Actor has no public pricing (B2B only / sur devis) | Explain context | `[N/D — offre uniquement sur devis B2B]` |
| Conflicting data between sources | Note conflict, use most recent | `[Sources divergentes : X€ selon A, Y€ selon B — retenu : B (plus récent)]` |

**Systemic failure on a domain.** Two or more URLs of the same domain returning thin content or no usable content is not bad luck with URLs: it is a rendering or consent problem on that site. Do not conclude the data is absent from that actor. In order: try a different entry point, check whether the scraper flagged `thin-content` (the page is JS-hydrated), nominate the page for capture and read the value from the screenshot, and if a consent overlay is the cause, add its handler to `scripts/consent.json` so every future mission benefits. Record what you tried in `data_quality.notes`.

**Never:**
- Cite a URL that a fetch did not return usable content for (rule S4). A search-engine snippet supports a value with `confidence: interpreted`, never a citation.
- Fill a cell with invented data to avoid `[N/D]`
- Average across sources without saying so
- Present a price from a comparison site as the actor's official price without verification

---

## Data Freshness Guidelines

| Data type | Acceptable age | Action if older |
|-----------|---------------|-----------------|
| Pricing / tariff | < 6 months | Re-search or mark `[à vérifier]` |
| Included services | < 12 months | Note date, flag if contract terms changed |
| Key figures (revenue, fleet size) | < 18 months (last annual report) | Use most recent report, note year |
| Market sizing | < 24 months | Acceptable with year citation |
| Strategic positioning | < 12 months | Note if company recently rebranded |

---

## Step 6: Statistiques publiques

L'office statistique et le portail open-data dépendent de `mission-config.json -> locale.country`.
Le tableau de résolution par pays et les patterns de requête vivent dans
`references/agent-prompts/search-modules/public-statistics.md`. Ne pas les dupliquer ici.

**Quand les utiliser :**
- Estimation de population adressable (Phase 3b)
- Chiffres de marché et parc installé
- Données socio-démographiques servant de base à une extrapolation

**MCP :** si un MCP open-data national est configuré, préférer ses outils au WebSearch
(résultats plus précis et directement citables). Pour la France, FlowDataGouv expose les
datasets data.gouv.fr et l'API INSEE. Sinon, WebSearch ciblée sur les domaines de l'office
et du portail.

**Format de citation :** défini dans `public-statistics.md` section 5.
