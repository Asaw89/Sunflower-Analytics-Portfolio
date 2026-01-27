"""
Data Cleaning & Validation Script for Sunflower Analytics
Checks CSV files for common data quality issues.
"""

import pandas as pd
from pathlib import Path
from data_loader import STATE_TO_REGION

# Valid values
VALID_STATES = set(STATE_TO_REGION.keys())
VALID_LEVELS = {"free", "paid"}


def check_missing(df, columns):
    """Check for missing values in specified columns."""
    issues = {}
    for col in columns:
        if col in df.columns:
            missing = df[col].isna().sum() + (df[col] == "").sum()
            if missing > 0:
                issues[col] = missing
    return issues


def check_duplicates(df):
    """Count duplicate rows."""
    return df.duplicated().sum()


def check_invalid_states(df, state_col="state"):
    """Find states not in our region mapping."""
    if state_col not in df.columns:
        return [], 0

    states_in_data = df[state_col].dropna().unique()
    invalid = [s for s in states_in_data if s not in VALID_STATES]
    invalid_count = df[~df[state_col].isin(VALID_STATES)].shape[0]
    return invalid, invalid_count


def check_invalid_levels(df, level_col="level"):
    """Find level values that aren't 'free' or 'paid'."""
    if level_col not in df.columns:
        return [], 0

    levels_in_data = df[level_col].dropna().unique()
    invalid = [l for l in levels_in_data if l not in VALID_LEVELS]
    invalid_count = df[~df[level_col].isin(VALID_LEVELS)].shape[0]
    return invalid, invalid_count


def check_duration_outliers(df, duration_col="duration", max_seconds=3600):
    """Find songs with unrealistic duration (default: over 1 hour)."""
    if duration_col not in df.columns:
        return 0, 0

    too_long = (df[duration_col] > max_seconds).sum()
    too_short = (df[duration_col] <= 0).sum()
    return too_long, too_short


def analyze_file(file_path, file_type):
    """Run all checks on a single file."""
    print(f"\n{'=' * 60}")
    print(f"  {file_path}")
    print(f"{'=' * 60}")

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"  ERROR reading file: {e}")
        return None

    print(f"  Total rows: {len(df):,}")
    print(f"  Columns: {list(df.columns)}")

    issues_found = False

    # Check duplicates
    dupes = check_duplicates(df)
    if dupes > 0:
        print(f"\n  ⚠️  Duplicate rows: {dupes:,}")
        issues_found = True
    else:
        print(f"\n  ✓ No duplicate rows")

    # Check missing values based on file type
    if file_type == "listen":
        missing = check_missing(df, ["artist", "song", "userId", "state", "duration"])
    elif file_type == "auth":
        missing = check_missing(df, ["userId", "state", "success"])
    elif file_type == "status":
        missing = check_missing(df, ["userId", "state", "level"])
    else:  # page_view
        missing = check_missing(df, ["userId", "state", "page"])

    if missing:
        print(f"\n  ⚠️  Missing values:")
        for col, count in missing.items():
            print(f"      {col}: {count:,} rows")
        issues_found = True
    else:
        print(f"  ✓ No missing values in key columns")

    # Check invalid states
    invalid_states, invalid_state_count = check_invalid_states(df)
    if invalid_states:
        print(f"\n  ⚠️  Invalid states: {invalid_states}")
        print(f"      Affects {invalid_state_count:,} rows")
        issues_found = True
    else:
        print(f"  ✓ All states are valid")

    # Check invalid levels
    invalid_levels, invalid_level_count = check_invalid_levels(df)
    if invalid_levels:
        print(f"\n  ⚠️  Invalid levels: {invalid_levels}")
        print(f"      Affects {invalid_level_count:,} rows")
        issues_found = True
    else:
        if "level" in df.columns:
            print(f"  ✓ All levels are valid (free/paid)")

    # Check duration (only for listen_events)
    if file_type == "listen":
        too_long, too_short = check_duration_outliers(df)
        if too_long > 0:
            print(f"\n  ⚠️  Duration > 1 hour: {too_long:,} rows")
            issues_found = True
        if too_short > 0:
            print(f"\n  ⚠️  Duration <= 0: {too_short:,} rows")
            issues_found = True
        if too_long == 0 and too_short == 0:
            print(f"  ✓ All durations look reasonable")

    # Summary
    if not issues_found:
        print(f"\n  ✅ File looks clean!")

    return df


def main():
    print("\n" + "=" * 60)
    print("  SUNFLOWER ANALYTICS - DATA QUALITY CHECK")
    print("=" * 60)

    data_dir = Path("data")

    files = {
        "listen_events.csv": "listen",
        "auth_events.csv": "auth",
        "status_change_events.csv": "status",
        "page_view_events.csv": "page_view",
    }

    for filename, file_type in files.items():
        file_path = data_dir / filename
        if file_path.exists():
            analyze_file(file_path, file_type)
        else:
            print(f"\n⚠️  File not found: {file_path}")

    print("\n" + "=" * 60)
    print("  DONE!")
    print("=" * 60)
    print("\nNext steps:")
    print("  - Review issues above")
    print("  - Decide: drop bad rows, fill defaults, or fix source data")
    print("  - Run clean_data.py (coming soon) to apply fixes")


if __name__ == "__main__":
    main()
