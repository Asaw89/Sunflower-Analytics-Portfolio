"""
Tests for the data_loader module.
"""

import pandas as pd
import tempfile
import os
from pathlib import Path
from data_loader import add_region_column, load_csv_with_region, load_all_csvs, STATE_TO_REGION


def test_state_to_region_mapping():
    """Test that all 50 states are mapped to a region."""
    expected_states = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    }
    
    mapped_states = set(STATE_TO_REGION.keys())
    
    # Check that all expected states are mapped
    missing_states = expected_states - mapped_states
    if missing_states:
        print(f"Missing states in mapping: {missing_states}")
        return False
    
    # Check that all regions are valid
    expected_regions = {'Northeast', 'Southeast', 'Midwest', 'West'}
    regions = set(STATE_TO_REGION.values())
    
    if regions != expected_regions:
        print(f"Invalid regions found. Expected {expected_regions}, got {regions}")
        return False
    
    print("✓ All 50 states are mapped to valid regions")
    return True


def test_add_region_column():
    """Test adding region column to a dataframe."""
    df = pd.DataFrame({
        'userId': [1, 2, 3, 4],
        'state': ['CA', 'NY', 'TX', 'IL']
    })
    
    result_df = add_region_column(df)
    
    # Check that region column was added
    if 'region' not in result_df.columns:
        print("✗ Region column was not added")
        return False
    
    # Check that regions are correct
    expected_regions = ['West', 'Northeast', 'Southeast', 'Midwest']
    actual_regions = result_df['region'].tolist()
    
    if actual_regions != expected_regions:
        print(f"✗ Incorrect regions. Expected {expected_regions}, got {actual_regions}")
        return False
    
    print("✓ Region column added correctly")
    return True


def test_load_csv_with_region():
    """Test loading a CSV file with region mapping."""
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('userId,state,level\n')
        f.write('1,CA,paid\n')
        f.write('2,NY,free\n')
        temp_file = f.name
    
    try:
        df = load_csv_with_region(temp_file)
        
        # Check that region column exists
        if 'region' not in df.columns:
            print("✗ Region column was not added to loaded CSV")
            return False
        
        # Check data integrity
        if len(df) != 2:
            print(f"✗ Expected 2 rows, got {len(df)}")
            return False
        
        print("✓ CSV loaded and region column added successfully")
        return True
        
    finally:
        os.unlink(temp_file)


def test_load_all_csvs():
    """Test loading all CSV files from a directory."""
    # Create a temporary directory with CSV files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test CSV files
        csv1_path = Path(temp_dir) / 'test1.csv'
        csv2_path = Path(temp_dir) / 'test2.csv'
        
        csv1_path.write_text('userId,state\n1,CA\n2,NY\n')
        csv2_path.write_text('userId,state\n3,TX\n4,FL\n')
        
        # Load all CSVs
        dataframes = load_all_csvs(temp_dir)
        
        # Check that both files were loaded
        if len(dataframes) != 2:
            print(f"✗ Expected 2 dataframes, got {len(dataframes)}")
            return False
        
        # Check that both have region column
        for name, df in dataframes.items():
            if 'region' not in df.columns:
                print(f"✗ Region column missing in {name}")
                return False
        
        print("✓ All CSVs loaded successfully with region columns")
        return True


def run_all_tests():
    """Run all tests and report results."""
    print("Running data_loader tests...\n")
    
    tests = [
        test_state_to_region_mapping,
        test_add_region_column,
        test_load_csv_with_region,
        test_load_all_csvs
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} raised an exception: {str(e)}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed} passed, {failed} failed")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == '__main__':
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
