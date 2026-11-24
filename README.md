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
- Done: ingest.py pages through the Provider Info API, saves each page as raw JSON, and checks rows pulled against the API's own count (14,686 rows, match).
- Done: Python environment managed with uv (dependencies locked in uv.lock).
- Done: Postgres 18 running in Docker with a named volume, so data survives container restarts. Connected with pgcli.
- Next: load the raw pages into Postgres (Zoomcamp Module 1).

## Run it
```
uv sync
uv run python ingest.py
docker run -it --rm -e POSTGRES_USER=root -e POSTGRES_PASSWORD=root -e POSTGRES_DB=ny_taxi \
  -v ny_taxi_postgres_data:/var/lib/postgresql -p 5433:5432 postgres:18
```
Port 5433 on the host because a local Postgres already uses 5432.

`zoomcamp/` holds course practice (Dockerfile + toy pipeline), separate from the CMS code.