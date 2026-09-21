# Search Module: Financial Data (KPIs, Revenue, Fleet)

> **Loaded by:** actor-research-prompt.md
> **Use for:** Every actor — always load this module alongside official-website.md.
> **Critical rule:** Official website scraping will NOT surface financial data. WebSearch is REQUIRED for this module.

## Search Queries

1. `"{actor_name}" chiffre d'affaires {current_year - 1} OR {current_year}`
2. `"{actor_name}" resultat net societe.com OR infogreffe`
3. `"{actor_name}" flotte vehicules OR nombre clients {current_year}`
4. `"{actor_name}" levee de fonds OR financement OR investissement`
5. `site:societe.com "{actor_name}"`
6. `site:pappers.fr "{actor_name}"`

## Source Priority

| Source | Trust | Notes |
|--------|-------|-------|
| societe.com / pappers.fr | High | Official registry data, verify SIREN |
| Annual report / investor deck | High | Cite year + page |
| Press release (official) | Medium-High | Verify date |
| Tech press (Maddyness, JDN) | Medium | Cross-reference |
| LinkedIn company page | Low | Headcount proxy only |

## What to Extract

| Field | Marker if missing |
|-------|-------------------|
| Revenue (CA) | `[N/D — donnees financieres non publiques]` |
| Net result | `[N/D]` — often unavailable for non-listed |
| Fleet size / customer count | `[ESTIMATION]` if from press |
| Headcount | LinkedIn proxy OK with `[ESTIMATION]` |
| Geographic presence | Official site usually has this |
| Recent fundraising | Press articles |

## Validation Criteria

- Financial figures must include year and source
- Never mix fiscal years without noting it
- Revenue from societe.com = last published accounts (may be N-2)
- Mark `[Donnees : YYYY — a verifier]` if >18 months old
