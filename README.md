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
- Done: load_postgres.py loads page 0 (500 facilities x 102 columns) into Postgres table `provider_info_raw` and checks the row count against the JSON (500 = 500). Reruns are safe.
- Next: load all pages (14,686 rows), then move from `replace` to an upsert on (CCN, snapshot_month).

## load_postgres.py
Loads the first page of CMS Provider Info data (`data/raw/page_0.json`) into a Postgres table, `provider_info_raw`.
- Checks the JSON is a dict and counts the rows in `results` (500 on page 0), so I'm not guessing the shape.
- Turns `results` into a pandas DataFrame and prints the shape and columns (500 x 102).
- Uses a SQLAlchemy engine so pandas can talk to Postgres.
- Writes with `if_exists="replace"`: each run drops the old table and rewrites it, so reruns don't create duplicate rows. That's safe for one snapshot. Multiple months will need an upsert on (CCN, snapshot_month).
- Counts rows in `provider_info_raw` and compares them to the JSON count. A mismatch prints a warning.

## Run it
```
uv sync
uv run python ingest.py
docker run -it --rm -e POSTGRES_USER=root -e POSTGRES_PASSWORD=root -e POSTGRES_DB=ny_taxi \
  -v ny_taxi_postgres_data:/var/lib/postgresql -p 5433:5432 postgres:18
# in a second terminal, once Postgres is ready:
uv run python load_postgres.py
```
Port 5433 on the host because a local Postgres already uses 5432.

`zoomcamp/` holds course practice (Dockerfile + toy pipeline), separate from the CMS code.