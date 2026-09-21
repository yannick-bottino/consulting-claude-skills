# Search Module: Market Intelligence (Industry Reports & Aggregators)

> **Loaded by:** actor-research-prompt.md
> **Use for:** Supplement when official data is thin. Load for actors with low transparency.

## Search Queries

1. `"{market}" etude benchmark comparatif {current_year}`
2. `"{market}" xerfi OR frost sullivan OR {sector_keyword} france`
3. `"{actor_name}" avis comparatif VS {competitor_names}`
4. `"{market}" classement acteurs parts de marche`

## Source Priority

| Source | Trust | Cost |
|--------|-------|------|
| Xerfi / Frost & Sullivan | High | Paid — extract only public summaries |
| Sector observatories | Medium-High | Often free for headline stats |
| Comparison sites (LeLynx, LesFurets, etc.) | Medium | Note date, may be outdated |
| Blog posts / reviews | Low | Cross-reference only |

## What to Extract

- Market size and growth rate
- Market share estimates (rare but valuable)
- Competitive positioning (who leads on what)
- Trends and disruptions

## Validation Criteria

- Industry reports: cite publisher + year + page/section
- Aggregator data: always note retrieval date
- Market sizing: acceptable if <24 months old
- Never present blog opinions as facts
