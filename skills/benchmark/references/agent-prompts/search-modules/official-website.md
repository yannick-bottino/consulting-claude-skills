# Search Module: Official Website (Pricing & Offer Pages)

> **Loaded by:** actor-research-prompt.md
> **Use for:** Every actor — always load this module.

## Search Queries (adapt {actor_name} and {market})

1. `"{actor_name}" tarifs abonnement {current_year} site officiel`
2. `"{actor_name}" offres prix mensuel {market}`
3. `site:{actor_domain} tarifs OR prix OR abonnement OR offre`
4. `"{actor_name}" conditions generales {market}`

## Scraping Priority

1. **Pricing page** (`/tarifs`, `/prix`, `/abonnement`, `/offres`, `/nos-offres`)
2. **Product page** for reference vehicle/product
3. **Landing page** (homepage hero — often contains headline pricing)
4. **CGV/conditions page** (hidden fees, engagement, resiliation)

## What to Extract

| Field | Where to find it | Required |
|-------|------------------|----------|
| Monthly prices by duration | Pricing page, tariff table | YES |
| Km included | Pricing page, fine print | YES |
| Insurance level | Offer/service page | YES |
| Maintenance included | Offer/service page | YES |
| Cancellation terms | CGV, FAQ | YES |
| Tagline | Homepage hero | YES |
| Delivery/return | Offer page, FAQ | NICE-TO-HAVE |

## Validation Criteria

- Price must be in euros, with duration (e.g., "489 euros/mois sur 12 mois")
- Source URL must be the official domain, not an aggregator
- If pricing page shows a simulator (JS-rendered), use Crawl4AI scraper level
- If pricing is "sur devis" only, mark `transparency_index: 1` and note in data_quality

## Failure Fallback

After 2+ failed scrape attempts on official site:
1. Try alternative URL paths (`/plus`, `/pro`, `/entreprise`, specific product URLs)
2. Try WebSearch for cached or aggregator pricing
3. Mark `[N/D — non disponible publiquement]` only after all attempts fail
