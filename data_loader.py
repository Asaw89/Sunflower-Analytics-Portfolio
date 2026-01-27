"""
Data loader module for Zip Listen Analytics.
Reads CSV files and adds region mapping based on US states.
"""

import pandas as pd
from pathlib import Path

# US State to Region mapping
STATE_TO_REGION = {
    # Northeast
    "CT": "Northeast",
    "ME": "Northeast",
    "MA": "Northeast",
    "NH": "Northeast",
    "RI": "Northeast",
    "VT": "Northeast",
    "NJ": "Northeast",
    "NY": "Northeast",
    "PA": "Northeast",
    # Southeast
    "DE": "Southeast",
    "FL": "Southeast",
    "GA": "Southeast",
    "MD": "Southeast",
    "NC": "Southeast",
    "SC": "Southeast",
    "VA": "Southeast",
    "WV": "Southeast",
    "AL": "Southeast",
    "KY": "Southeast",
    "MS": "Southeast",
    "TN": "Southeast",
    "AR": "Southeast",
    "LA": "Southeast",
    "TX": "Southeast",
    "OK": "Southeast",
    # Midwest
    "IL": "Midwest",
    "IN": "Midwest",
    "MI": "Midwest",
    "OH": "Midwest",
    "WI": "Midwest",
    "IA": "Midwest",
    "KS": "Midwest",
    "MN": "Midwest",
    "MO": "Midwest",
    "NE": "Midwest",
    "ND": "Midwest",
    "SD": "Midwest",
    # West
    "AZ": "West",
    "CO": "West",
    "ID": "West",
    "MT": "West",
    "NV": "West",
    "NM": "West",
    "UT": "West",
    "WY": "West",
    "AK": "West",
    "CA": "West",
    "HI": "West",
    "OR": "West",
    "WA": "West",
}


def add_region_column(df, state_column="state"):
    """
    Add a 'region' column to the dataframe based on the state column.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataframe to add the region column to
    state_column : str, optional
        The name of the column containing state abbreviations (default: 'state')

    Returns:
    --------
    pandas.DataFrame
        The dataframe with the added 'region' column
    """
    if state_column not in df.columns:
        raise ValueError(f"Column '{state_column}' not found in dataframe")

    # Create a copy to avoid modifying the original dataframe
    df = df.copy()

    # Map states to regions
    df["region"] = df[state_column].map(STATE_TO_REGION)

    # Warn about unmapped states
    unmapped = df[df["region"].isna()][state_column].unique()
    if len(unmapped) > 0:
        print(f"Warning: Found unmapped states: {list(unmapped)}")

    return df


def load_csv_with_region(file_path, state_column="state"):
    """
    Load a CSV file and add a region column based on state.

    Parameters:
    -----------
    file_path : str or Path
        Path to the CSV file
    state_column : str, optional
        The name of the column containing state abbreviations (default: 'state')

    Returns:
    --------
    pandas.DataFrame
        The loaded dataframe with the added 'region' column
    """
    df = pd.read_csv(file_path)
    df = add_region_column(df, state_column)
    return df


def load_all_csvs(data_dir="data", state_column="state"):
    """
    Load all CSV files from the data directory and add region columns.

    Parameters:
    -----------
    data_dir : str or Path, optional
        Path to the directory containing CSV files (default: 'data')
    state_column : str, optional
        The name of the column containing state abbreviations (default: 'state')

    Returns:
    --------
    dict
        Dictionary mapping CSV filenames (without extension) to DataFrames
    """
    data_path = Path(data_dir)

    if not data_path.exists():
        raise FileNotFoundError(f"Data directory '{data_dir}' not found")

    csv_files = list(data_path.glob("*.csv"))

    if len(csv_files) == 0:
        raise FileNotFoundError(f"No CSV files found in '{data_dir}'")

    dataframes = {}

    for csv_file in csv_files:
        dataset_name = csv_file.stem  # filename without extension
        print(f"Loading {csv_file.name}...")

        try:
            df = load_csv_with_region(csv_file, state_column)
            dataframes[dataset_name] = df
            print(f"  Loaded {len(df)} rows with {len(df.columns)} columns")
        except Exception as e:
            print(f"  Error loading {csv_file.name}: {str(e)}")

    return dataframes


if __name__ == "__main__":
    # Example usage - requires a 'data' directory with CSV files
    import sys

    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    else:
        data_dir = "data"

    try:
        dataframes = load_all_csvs(data_dir)

        print("\nSummary:")
        print(f"Loaded {len(dataframes)} datasets")

        for name, df in dataframes.items():
            print(f"\n{name}:")
            print(f"  Shape: {df.shape}")
            print(f"  Columns: {list(df.columns)}")
            if "region" in df.columns:
                print(f"  Regions: {df['region'].value_counts().to_dict()}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(
            f"\nTo use this script, create a '{data_dir}' directory with CSV files containing a 'state' column."
        )
        print(f"Usage: python data_loader.py [data_directory]")
