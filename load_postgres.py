import json
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine

lp = json.load(open("data/raw/page_0.json", "r"))
if isinstance(lp, dict):
    lp_count = len(lp["results"])

df = pd.DataFrame(lp["results"])
print(df.shape, df.columns)

engine = create_engine("postgresql://root:root@localhost:5433/ny_taxi")

df.to_sql("provider_info_raw", engine, if_exists="replace", index=False)
count = pd.read_sql("SELECT COUNT(*) FROM provider_info_raw", engine)
if count.iloc[0, 0] != lp_count:
    print(f"Row count mismatch: DataFrame has {lp_count} rows, but the database has {count.iloc[0, 0]} rows.")
else:
    print(f"Successfully loaded {lp_count} rows into the database.")