# CMS Nursing Home Pipeline

## What it is
This pipeline takes nursing home records from the CMS public data API and runs them through ingestion, standardization, and modeling into a facility table and a citation table. The goal is to answer questions like "which facilities keep getting severe citations?"

Why nursing homes: it's real, messy public healthcare data that CMS updates monthly. Senior care often doesn't get the same attention for improvement as other areas, and tracking citation patterns can show which facilities need to improve so residents get better care.

## Data sources
- CMS Provider Info API (https://data.cms.gov/provider-data/api/1/datastore/query/4pq5-n9py/0)
- CMS Health Deficiencies API (planned)

## Grain
One row per facility (CCN) per snapshot month. Why snapshots: CMS releases new data every month. Each run loads that month as its own snapshot using an upsert on (CCN, snapshot_month), so rerunning the same month replaces only that month's rows instead of creating duplicates. Older months stay in the table, so I can compare a facility's results across months.

## Status
- Done: ingest.py pages through the Provider Info API and saves each page as raw JSON.
- Next: check that rows pulled match the API's total count, then load into Postgres (needs Docker, blocked until macOS update).