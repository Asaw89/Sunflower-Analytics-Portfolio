"""
Data Pipeline Example for Zip Listen Analytics

This script demonstrates how to use Pandas for advanced data analysis
beyond the basic API endpoints. This can be used for batch processing,
report generation, or feeding data into Tableau.

Requirements:
- pandas
- sqlalchemy
- psycopg2-binary
"""

import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import datetime, timedelta


# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://sunflower_user:zipmusic@xo.zipcode.rocks:9088/sunflower",
)

# Create engine
engine = create_engine(DATABASE_URL)


def load_data():
    """Load all data from database into pandas DataFrames"""
    print("Loading data from database...")

    listen_events = pd.read_sql_table("listen_events", engine)
    auth_events = pd.read_sql_table("auth_events", engine)
    status_change_events = pd.read_sql_table("status_change_events", engine)

    print(f"Loaded {len(listen_events)} listen events")
    print(f"Loaded {len(auth_events)} auth events")
    print(f"Loaded {len(status_change_events)} status change events")

    return listen_events, auth_events, status_change_events


def analyze_listening_patterns(listen_events):
    """Analyze listening patterns by time of day and day of week"""
    print("\n=== Listening Pattern Analysis ===")

    # Convert timestamp to datetime
    listen_events["timestamp"] = pd.to_datetime(listen_events["timestamp"])

    # Extract time features
    listen_events["hour"] = listen_events["timestamp"].dt.hour
    listen_events["day_of_week"] = listen_events["timestamp"].dt.day_name()

    # Peak listening hours
    hourly_streams = listen_events.groupby("hour").size()
    peak_hour = hourly_streams.idxmax()
    print(f"Peak listening hour: {peak_hour}:00 ({hourly_streams[peak_hour]} streams)")

    # Most active day
    daily_streams = listen_events.groupby("day_of_week").size()
    print(f"\nStreams by day of week:")
    print(daily_streams)

    return listen_events


def analyze_user_engagement(listen_events):
    """Analyze user engagement metrics"""
    print("\n=== User Engagement Analysis ===")

    # Average session duration by user
    user_stats = (
        listen_events.groupby("userId")
        .agg({"duration": ["sum", "mean", "count"], "song": "count"})
        .round(2)
    )

    user_stats.columns = [
        "total_duration",
        "avg_duration",
        "duration_count",
        "stream_count",
    ]

    print(f"Average streams per user: {user_stats['stream_count'].mean():.2f}")
    print(
        f"Average listening time per user: {user_stats['total_duration'].mean():.2f} seconds"
    )
    print(
        f"Most engaged user: {user_stats['stream_count'].idxmax()} ({user_stats['stream_count'].max()} streams)"
    )

    return user_stats


def analyze_genre_preferences(listen_events):
    """Analyze genre preferences by subscription level"""
    print("\n=== Genre Preference Analysis ===")

    # Genre distribution by subscription level
    genre_by_level = (
        listen_events.groupby(["level", "genre"]).size().unstack(fill_value=0)
    )

    print("\nGenre distribution by subscription level:")
    print(genre_by_level)

    # Calculate percentage
    genre_pct = (genre_by_level.T / genre_by_level.sum(axis=1)).T * 100
    print("\nGenre preferences (%):")
    print(genre_pct.round(2))

    return genre_by_level


def analyze_conversion_funnel(auth_events, status_change_events):
    """Analyze user conversion from free to paid"""
    print("\n=== Conversion Funnel Analysis ===")

    # Successful authentications
    successful_auths = auth_events[auth_events["success"] == True]
    unique_users = successful_auths["userId"].nunique()

    # Users who became paid subscribers
    paid_users = status_change_events[status_change_events["level"] == "paid"][
        "userId"
    ].nunique()

    conversion_rate = (paid_users / unique_users) * 100 if unique_users > 0 else 0

    print(f"Total authenticated users: {unique_users}")
    print(f"Paid subscribers: {paid_users}")
    print(f"Conversion rate: {conversion_rate:.2f}%")

    return conversion_rate


def generate_regional_report(listen_events):
    """Generate comprehensive regional report"""
    print("\n=== Regional Report ===")

    import sys

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from app.utils.regions import STATE_TO_REGION

    # Map states to regions
    listen_events["region"] = listen_events["state"].map(STATE_TO_REGION)

    # Regional statistics
    regional_stats = (
        listen_events.groupby("region")
        .agg(
            {
                "userId": "nunique",
                "song": "count",
                "duration": "sum",
                "genre": lambda x: x.mode()[0] if len(x) > 0 else None,
            }
        )
        .round(2)
    )

    regional_stats.columns = [
        "unique_users",
        "total_streams",
        "total_duration_seconds",
        "most_popular_genre",
    ]

    # Calculate average streams per user
    regional_stats["avg_streams_per_user"] = (
        regional_stats["total_streams"] / regional_stats["unique_users"]
    ).round(2)

    print(regional_stats)

    return regional_stats


def export_for_tableau(listen_events, auth_events, status_change_events):
    """Export processed data for Tableau"""
    print("\n=== Exporting Data for Tableau ===")

    import sys

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from app.utils.regions import STATE_TO_REGION

    # Add region to all dataframes
    listen_events["region"] = listen_events["state"].map(STATE_TO_REGION)
    auth_events["region"] = auth_events["state"].map(STATE_TO_REGION)
    status_change_events["region"] = status_change_events["state"].map(STATE_TO_REGION)

    # Export to CSV
    listen_events.to_csv("tableau_listen_events.csv", index=False)
    auth_events.to_csv("tableau_auth_events.csv", index=False)
    status_change_events.to_csv("tableau_status_events.csv", index=False)

    print("Exported data to:")
    print("  - tableau_listen_events.csv")
    print("  - tableau_auth_events.csv")
    print("  - tableau_status_events.csv")


def main():
    """Main pipeline execution"""
    print("=" * 60)
    print("Zip Listen Analytics - Data Pipeline Example")
    print("=" * 60)

    try:
        # Load data
        listen_events, auth_events, status_change_events = load_data()

        # Run analyses
        listen_events = analyze_listening_patterns(listen_events)
        user_stats = analyze_user_engagement(listen_events)
        genre_prefs = analyze_genre_preferences(listen_events)
        conversion_rate = analyze_conversion_funnel(auth_events, status_change_events)
        regional_report = generate_regional_report(listen_events)

        # Export for Tableau
        export_for_tableau(listen_events, auth_events, status_change_events)

        print("\n" + "=" * 60)
        print("Pipeline completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure the database is running:")
        print("  docker compose up -d db")


if __name__ == "__main__":
    main()
