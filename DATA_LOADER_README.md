# Data Loader

Python module for loading CSV files with automatic US region mapping.

## Features

- Reads all CSV files from a configurable data directory using pandas
- Automatically adds a 'region' column mapping US states to regions:
  - **Northeast**: CT, ME, MA, NH, RI, VT, NJ, NY, PA
  - **Southeast**: DE, FL, GA, MD, NC, SC, VA, WV, AL, KY, MS, TN, AR, LA, TX, OK
  - **Midwest**: IL, IN, MI, OH, WI, IA, KS, MN, MO, NE, ND, SD
  - **West**: AZ, CO, ID, MT, NV, NM, UT, WY, AK, CA, HI, OR, WA

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Load all CSV files from a data directory

```python
from data_loader import load_all_csvs

# Load all CSV files from the 'data' directory (default)
dataframes = load_all_csvs('data')

# Or specify a custom directory
dataframes = load_all_csvs('/path/to/your/csv/files')

# Access individual dataframes
for name, df in dataframes.items():
    print(f"Loaded {name}: {df.shape}")
```

### Load a single CSV file

```python
from data_loader import load_csv_with_region

# Load a single CSV file with region mapping
df = load_csv_with_region('path/to/your/file.csv')
```

### Add region column to existing dataframe

```python
from data_loader import add_region_column
import pandas as pd

# Load your own dataframe
df = pd.read_csv('your_file.csv')

# Add region column (assumes a 'state' column exists)
df = add_region_column(df, state_column='state')
```

## Command Line Usage

Run the script directly to load and display summary information:

```bash
# Load from default 'data' directory
python data_loader.py

# Load from custom directory
python data_loader.py /path/to/csv/files
```

## CSV File Requirements

Your CSV files should contain a column with US state abbreviations (default column name: 'state').
The module will automatically add a 'region' column based on this mapping.

Example CSV structure:
```csv
userId,state,level
1001,CA,paid
1002,NY,free
1003,TX,paid
```

## Testing

Run the test suite:

```bash
python test_data_loader.py
```

## Requirements

- Python 3.7+
- pandas 2.0.0+
