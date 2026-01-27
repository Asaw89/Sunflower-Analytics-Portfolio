"""
Upload data from local PostgreSQL (with genres) to XO database.
"""

import pandas as pd
from sqlalchemy import create_engine

# Local database (has genres)
LOCAL_URL = "postgresql://sunflower_user:zipmusic@xo.zipcode.rocks:9088/sunflower"
local_engine = create_engine(LOCAL_URL)

# XO database (destination)
XO_URL = "postgresql://sunflower_user:zipmusic@xo.zipcode.rocks:9088/sunflower"
xo_engine = create_engine(XO_URL)

tables = ["listen_events", "auth_events", "status_change_events", "page_view_events"]

print("Uploading from local PostgreSQL to XO...")

for table in tables:
    print(f"\n{table}...")

    # Read from local database
    df = pd.read_sql(f"SELECT * FROM {table}", local_engine)
    print(f"  Read {len(df):,} rows from local")

    # Upload to XO
    df.to_sql(table, xo_engine, if_exists="replace", index=False, chunksize=10000)
    print(f"  ✓ Uploaded to XO")

print("\nDone!")
