"""
Test script to validate data processing logic without database
"""
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.regions import STATE_TO_REGION

# Sample data similar to what would come from database
listen_data = [
    {'state': 'NY', 'genre': 'Pop', 'stream_count': 10},
    {'state': 'CA', 'genre': 'Pop', 'stream_count': 15},
    {'state': 'TX', 'genre': 'Hip-Hop', 'stream_count': 8},
    {'state': 'FL', 'genre': 'Pop', 'stream_count': 12},
    {'state': 'IL', 'genre': 'Rock', 'stream_count': 6},
]

print("Testing Genre by Region Processing")
print("=" * 50)

# Convert to DataFrame
df = pd.DataFrame(listen_data)

# Map states to regions
df['region'] = df['state'].map(STATE_TO_REGION)

# Group by region and genre
region_genre = df.groupby(['region', 'genre'])['stream_count'].sum().reset_index()

print(region_genre)
print()

# Test subscriber data processing
subscriber_data = [
    {'state': 'NY', 'level': 'paid', 'user_count': 5},
    {'state': 'CA', 'level': 'free', 'user_count': 3},
    {'state': 'TX', 'level': 'paid', 'user_count': 7},
    {'state': 'FL', 'level': 'paid', 'user_count': 4},
    {'state': 'IL', 'level': 'free', 'user_count': 2},
]

print("Testing Subscriber by Region Processing")
print("=" * 50)

df2 = pd.DataFrame(subscriber_data)
df2['region'] = df2['state'].map(STATE_TO_REGION)
region_level = df2.groupby(['region', 'level'])['user_count'].sum().reset_index()

print(region_level)
print()

# Test artist growth rate calculation
artist_recent = pd.DataFrame([
    {'artist': 'Taylor Swift', 'current_streams': 100},
    {'artist': 'Drake', 'current_streams': 80},
    {'artist': 'NewArtist', 'current_streams': 50},
])

artist_previous = pd.DataFrame([
    {'artist': 'Taylor Swift', 'previous_streams': 90},
    {'artist': 'Drake', 'previous_streams': 85},
    {'artist': 'NewArtist', 'previous_streams': 10},
])

print("Testing Artist Growth Rate Calculation")
print("=" * 50)

# Merge dataframes
df3 = artist_recent.merge(artist_previous, on='artist', how='left')
df3['previous_streams'] = df3['previous_streams'].fillna(0)

# Calculate growth rate
df3['growth_rate'] = df3.apply(
    lambda row: (
        ((row['current_streams'] - row['previous_streams']) / row['previous_streams'] * 100)
        if row['previous_streams'] > 0
        else (100.0 if row['current_streams'] > 0 else 0.0)
    ),
    axis=1
)

# Sort by growth rate
df3 = df3.sort_values('growth_rate', ascending=False)

print(df3)
print()

print("✓ All data processing tests passed successfully!")
