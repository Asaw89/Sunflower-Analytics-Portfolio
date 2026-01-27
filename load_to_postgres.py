"""
Load CSV files into PostgreSQL database.
Run this after docker-compose up to populate the database with your actual data.
"""

import pandas as pd
from sqlalchemy import create_engine
from data_loader import STATE_TO_REGION

# Database connection - matches docker-compose.yml
DATABASE_URL = "postgresql://sunflower_user:zipmusic@xo.zipcode.rocks:9088/sunflower"


def add_region(df, state_column="state"):
    """Add region column based on state."""
    df = df.copy()
    df["region"] = df[state_column].map(STATE_TO_REGION)
    return df


def load_csvs_to_postgres():
    """Load all CSV files into PostgreSQL tables."""

    engine = create_engine(DATABASE_URL)

    files = {
        "listen_events": "data/listen_events.csv",
        "auth_events": "data/auth_events.csv",
        "status_change_events": "data/status_change_events.csv",
        "page_view_events": "data/page_view_events.csv",
    }

    for table_name, file_path in files.items():
        print(f"\nLoading {file_path}...")

        try:
            df = pd.read_csv(file_path)
            print(f"  Read {len(df):,} rows")

            if "state" in df.columns:
                df = add_region(df)
                print(f"  Added region column")

            df.to_sql(
                table_name, engine, if_exists="replace", index=False, chunksize=10000
            )
            print(f"  ✓ Loaded into '{table_name}' table")

        except FileNotFoundError:
            print(f"  ✗ File not found: {file_path}")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")

    print("\nDone!")


if __name__ == "__main__":
    print("Loading CSV data into PostgreSQL")
    load_csvs_to_postgres()
