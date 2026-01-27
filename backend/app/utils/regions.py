"""
US State to Region mapping utility
"""

# US State to Region mapping
STATE_TO_REGION = {
    # Northeast
    "CT": "Northeast", "ME": "Northeast", "MA": "Northeast", "NH": "Northeast",
    "RI": "Northeast", "VT": "Northeast", "NJ": "Northeast", "NY": "Northeast",
    "PA": "Northeast",
    
    # Southeast
    "DE": "Southeast", "FL": "Southeast", "GA": "Southeast", "MD": "Southeast",
    "NC": "Southeast", "SC": "Southeast", "VA": "Southeast", "WV": "Southeast",
    "AL": "Southeast", "KY": "Southeast", "MS": "Southeast", "TN": "Southeast",
    "AR": "Southeast", "LA": "Southeast", "TX": "Southeast",
    
    # Midwest
    "IL": "Midwest", "IN": "Midwest", "MI": "Midwest", "OH": "Midwest",
    "WI": "Midwest", "IA": "Midwest", "KS": "Midwest", "MN": "Midwest",
    "MO": "Midwest", "NE": "Midwest", "ND": "Midwest", "SD": "Midwest",
    
    # West
    "AZ": "West", "CO": "West", "ID": "West", "MT": "West", "NV": "West",
    "NM": "West", "UT": "West", "WY": "West", "AK": "West", "CA": "West",
    "HI": "West", "OR": "West", "WA": "West"
}


def get_region(state: str) -> str:
    """Get region for a given US state code"""
    return STATE_TO_REGION.get(state.upper(), "Unknown")
