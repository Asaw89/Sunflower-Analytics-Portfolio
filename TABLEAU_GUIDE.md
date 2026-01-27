# Tableau Integration Guide

This document explains how to connect Tableau to the Zip Listen Analytics PostgreSQL database for advanced visualizations.

## Prerequisites

- Tableau Desktop or Tableau Server
- Running Zip Listen Analytics Docker containers
- PostgreSQL database accessible

## Connection Steps

### 1. Start the Zip Listen Analytics Application

```bash
docker-compose up -d
```

### 2. Connect Tableau to PostgreSQL

1. Open Tableau Desktop
2. Click on "Connect" → "To a Server" → "PostgreSQL"
3. Enter the connection details:
   - **Server**: localhost (or your Docker host IP)
   - **Port**: 5432
   - **Database**: ziplistendb
   - **Username**: zipuser
   - **Password**: zippassword
   - **SSL**: Not required (for development)

### 3. Select Tables

After connecting, you'll see three main tables:
- `listen_events` - Music listening activity
- `auth_events` - User authentication events
- `status_change_events` - Subscription status changes

## Recommended Visualizations

### 1. Genre Heatmap by Region and Time

**Data Source**: `listen_events`

**Dimensions**:
- State (mapped to Region using calculated field)
- Genre
- Timestamp (Day/Week/Month)

**Measures**:
- Count of records

**Calculated Field - Region**:
```
CASE [State]
  WHEN "CT" THEN "Northeast"
  WHEN "ME" THEN "Northeast"
  WHEN "MA" THEN "Northeast"
  WHEN "NH" THEN "Northeast"
  WHEN "RI" THEN "Northeast"
  WHEN "VT" THEN "Northeast"
  WHEN "NJ" THEN "Northeast"
  WHEN "NY" THEN "Northeast"
  WHEN "PA" THEN "Northeast"
  
  WHEN "DE" THEN "Southeast"
  WHEN "FL" THEN "Southeast"
  WHEN "GA" THEN "Southeast"
  WHEN "MD" THEN "Southeast"
  WHEN "NC" THEN "Southeast"
  WHEN "SC" THEN "Southeast"
  WHEN "VA" THEN "Southeast"
  WHEN "WV" THEN "Southeast"
  WHEN "AL" THEN "Southeast"
  WHEN "KY" THEN "Southeast"
  WHEN "MS" THEN "Southeast"
  WHEN "TN" THEN "Southeast"
  WHEN "AR" THEN "Southeast"
  WHEN "LA" THEN "Southeast"
  WHEN "TX" THEN "Southeast"
  
  WHEN "IL" THEN "Midwest"
  WHEN "IN" THEN "Midwest"
  WHEN "MI" THEN "Midwest"
  WHEN "OH" THEN "Midwest"
  WHEN "WI" THEN "Midwest"
  WHEN "IA" THEN "Midwest"
  WHEN "KS" THEN "Midwest"
  WHEN "MN" THEN "Midwest"
  WHEN "MO" THEN "Midwest"
  WHEN "NE" THEN "Midwest"
  WHEN "ND" THEN "Midwest"
  WHEN "SD" THEN "Midwest"
  
  WHEN "AZ" THEN "West"
  WHEN "CO" THEN "West"
  WHEN "ID" THEN "West"
  WHEN "MT" THEN "West"
  WHEN "NV" THEN "West"
  WHEN "NM" THEN "West"
  WHEN "UT" THEN "West"
  WHEN "WY" THEN "West"
  WHEN "AK" THEN "West"
  WHEN "CA" THEN "West"
  WHEN "HI" THEN "West"
  WHEN "OR" THEN "West"
  WHEN "WA" THEN "West"
  
  ELSE "Unknown"
END
```

### 2. Revenue Analysis Dashboard

**Data Sources**: 
- `listen_events` (for activity)
- `status_change_events` (for subscription levels)

**Visualizations**:
- Map showing paid vs free users by state
- Trend line of subscription conversions over time
- Bar chart of average listening duration by subscription level

### 3. Artist Performance Dashboard

**Data Source**: `listen_events`

**Visualizations**:
- Top 20 artists by stream count (bar chart)
- Artist popularity trend over time (line chart)
- Geographic distribution of top artists (map)
- Genre distribution for top artists (pie chart)

### 4. User Engagement Metrics

**Data Sources**: 
- `listen_events`
- `auth_events`

**Visualizations**:
- Daily/Weekly/Monthly Active Users (line chart)
- Session duration distribution (histogram)
- User retention cohort analysis
- Authentication success rate by region

## Advanced Analytics

### Growth Rate Calculation

To calculate artist growth rate (similar to the API endpoint):

**Calculated Field - Recent Streams**:
```
{ FIXED [Artist] : 
  SUM(
    IF DATEDIFF('day', [Timestamp], TODAY()) <= 7 
    THEN 1 
    ELSE 0 
    END
  )
}
```

**Calculated Field - Previous Streams**:
```
{ FIXED [Artist] : 
  SUM(
    IF DATEDIFF('day', [Timestamp], TODAY()) > 7 
       AND DATEDIFF('day', [Timestamp], TODAY()) <= 14 
    THEN 1 
    ELSE 0 
    END
  )
}
```

**Calculated Field - Growth Rate**:
```
IF [Previous Streams] > 0 
THEN (([Recent Streams] - [Previous Streams]) / [Previous Streams]) * 100
ELSE 100
END
```

## Best Practices

1. **Use Extracts for Performance**: For large datasets, create Tableau extracts for faster performance
2. **Refresh Schedule**: Set up automatic extract refresh to keep data current
3. **Filters**: Add date range filters to focus on relevant time periods
4. **Parameters**: Create parameters for dynamic region/genre filtering
5. **Calculations**: Use calculated fields for complex metrics like growth rates

## Exporting Data from API to Tableau

You can also export data from the API endpoints to CSV and import into Tableau:

```bash
# Export genres by region
curl http://localhost:8000/api/genres/by-region > genres_data.json

# Export top artists
curl http://localhost:8000/api/artists/top?limit=100 > top_artists.json
```

Then use Tableau's JSON connector to import the data.

## Security Considerations

For production deployments:
1. Use SSL/TLS for database connections
2. Store credentials securely (not in version control)
3. Use read-only database users for Tableau
4. Implement row-level security if needed
5. Use Tableau Server for centralized access control

## Additional Resources

- [Tableau PostgreSQL Documentation](https://help.tableau.com/current/pro/desktop/en-us/examples_postgresql.htm)
- [Tableau Calculated Fields](https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields.htm)
- [Tableau Dashboard Best Practices](https://help.tableau.com/current/pro/desktop/en-us/dashboards_best_practices.htm)
