# Search Module: Public Statistics & Population Data

> **Loaded by:** actor-research-prompt.md
> **Use for:** Phase 3b (target population analysis). Load only when `targets-analysis` is in the mission deliverables.
> **Locale-driven:** the statistical office comes from `mission-config.json -> locale.country`. Never assume France.

## 1. Statistical office by country

Resolve the office first, then build the queries from it. This table is data: add a row when a mission needs a new country.

| `locale.country` | Primary office | Open-data portal | Complementary sources |
|---|---|---|---|
| FR | INSEE | data.gouv.fr | DARES, ADEME, Banque de France |
| BE | Statbel | statbel.fgov.be | Banque nationale de Belgique |
| CH | OFS / BFS | opendata.swiss | SECO |
| DE | Destatis | govdata.de | Bundesbank |
| ES | INE | datos.gob.es | Banco de España |
| IT | ISTAT | dati.gov.it | Banca d'Italia |
| UK | ONS | data.gov.uk | Bank of England |
| NL | CBS | data.overheid.nl | DNB |
| US | Census Bureau / BLS | data.gov | Federal Reserve, BEA |
| EU-wide | Eurostat | data.europa.eu | ECB |
| *(other)* | national statistical office, found via a first search | national open-data portal | central bank |

When the country has no row here, search `"[country] national statistical office"` once, use it, and add the row to this table at the end of the mission.

## 2. Search queries

Substitute the resolved office and portal, and run in the country's own language plus English:

```text
site:{office_domain} {population_keyword} {current_year}
site:{portal_domain} {market_keyword} statistiques OR statistics
"{office_name}" "{demographic_filter}" households OR ménages OR population
"{complementary_source}" "{employment_keyword}" workforce OR actifs
```

## 3. MCP integration

If a national open-data MCP is configured in the environment, prefer its tools over web search: results are precise and directly citable. For France, FlowDataGouv exposes `search_datasets`, `query_resource_data`, `get_metrics`.

Without an MCP, fall back to site-scoped web search on the office and portal domains.

## 4. Funnel construction pattern

Build the population funnel top-down, whatever the country:

```text
Total population of {geography} -> [source: {office}, year]
  +-- Filter 1: [demographic] -> [X] [source]
     +-- Filter 2: [behavioural] -> [X] [source + assumption]
        +-- Filter 3: [economic] -> [X] [source + assumption]
           +-- ADDRESSABLE TARGET -> [X] [own calculation]
```

Each step carries a named source (or `[ESTIMATION]`), the percentage applied, and whether it is a fact or an assumption. A funnel step with no source is a fabricated market size.

## 5. Citation format

```text
[Source : {office} — {indicator_name}, {year}, via {access_method}]
```

Access methods: the portal domain, the office domain, or the MCP name.
