from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import pandas as pd

from ..db.database import get_db
from ..models.models import ListenEvent, StatusChangeEvent
from ..schemas.schemas import (
    GenreByRegionResponse,
    SubscriberByRegionResponse,
    TopArtistResponse,
    RisingArtistResponse
)
from ..utils.regions import STATE_TO_REGION

router = APIRouter()


@router.get("/genres/by-region", response_model=List[GenreByRegionResponse])
def get_genres_by_region(
    region: Optional[str] = Query(None, description="Filter by specific region"),
    db: Session = Depends(get_db)
):
    """
    Get genre distribution by US region (Northeast, Southeast, Midwest, West)
    """
    # Query all listen events
    query = db.query(
        ListenEvent.state,
        ListenEvent.genre,
        func.count(ListenEvent.id).label('stream_count')
    ).group_by(ListenEvent.state, ListenEvent.genre)
    
    results = query.all()
    
    # Convert to dataframe for easier processing
    df = pd.DataFrame(results, columns=['state', 'genre', 'stream_count'])
    
    # Map states to regions
    df['region'] = df['state'].map(STATE_TO_REGION)
    
    # Filter by region if specified
    if region:
        df = df[df['region'] == region]
    
    # Group by region and genre
    region_genre = df.groupby(['region', 'genre'])['stream_count'].sum().reset_index()
    
    # Convert to response format
    response = []
    for _, row in region_genre.iterrows():
        response.append(GenreByRegionResponse(
            region=row['region'],
            genre=row['genre'],
            stream_count=int(row['stream_count'])
        ))
    
    return response


@router.get("/subscribers/by-region", response_model=List[SubscriberByRegionResponse])
def get_subscribers_by_region(
    region: Optional[str] = Query(None, description="Filter by specific region"),
    db: Session = Depends(get_db)
):
    """
    Get subscriber distribution (paid vs free) by US region
    """
    # Query unique users by state and level
    query = db.query(
        StatusChangeEvent.state,
        StatusChangeEvent.level,
        func.count(func.distinct(StatusChangeEvent.userId)).label('user_count')
    ).group_by(StatusChangeEvent.state, StatusChangeEvent.level)
    
    results = query.all()
    
    # Convert to dataframe
    df = pd.DataFrame(results, columns=['state', 'level', 'user_count'])
    
    # Map states to regions
    df['region'] = df['state'].map(STATE_TO_REGION)
    
    # Filter by region if specified
    if region:
        df = df[df['region'] == region]
    
    # Group by region and level
    region_level = df.groupby(['region', 'level'])['user_count'].sum().reset_index()
    
    # Convert to response format
    response = []
    for _, row in region_level.iterrows():
        response.append(SubscriberByRegionResponse(
            region=row['region'],
            level=row['level'],
            user_count=int(row['user_count'])
        ))
    
    return response


@router.get("/artists/top", response_model=List[TopArtistResponse])
def get_top_artists(
    limit: int = Query(10, ge=1, le=100, description="Number of top artists to return"),
    db: Session = Depends(get_db)
):
    """
    Get top artists by total stream count
    """
    # Query artists with stream counts
    query = db.query(
        ListenEvent.artist,
        func.count(ListenEvent.id).label('stream_count')
    ).group_by(ListenEvent.artist).order_by(func.count(ListenEvent.id).desc()).limit(limit)
    
    results = query.all()
    
    # Convert to response format with ranking
    response = []
    for rank, (artist, stream_count) in enumerate(results, 1):
        response.append(TopArtistResponse(
            artist=artist,
            stream_count=stream_count,
            rank=rank
        ))
    
    return response


@router.get("/artists/rising", response_model=List[RisingArtistResponse])
def get_rising_artists(
    limit: int = Query(10, ge=1, le=100, description="Number of rising artists to return"),
    db: Session = Depends(get_db)
):
    """
    Get rising artists based on growth rate between time periods
    Compares recent 7 days vs previous 7 days
    """
    from datetime import datetime, timedelta
    
    # Get current time and calculate time windows
    now = datetime.utcnow()
    recent_start = now - timedelta(days=7)
    previous_start = now - timedelta(days=14)
    
    # Query recent period (last 7 days)
    recent_query = db.query(
        ListenEvent.artist,
        func.count(ListenEvent.id).label('stream_count')
    ).filter(
        ListenEvent.timestamp >= recent_start
    ).group_by(ListenEvent.artist)
    
    recent_results = recent_query.all()
    recent_df = pd.DataFrame(recent_results, columns=['artist', 'current_streams'])
    
    # Query previous period (8-14 days ago)
    previous_query = db.query(
        ListenEvent.artist,
        func.count(ListenEvent.id).label('stream_count')
    ).filter(
        ListenEvent.timestamp >= previous_start,
        ListenEvent.timestamp < recent_start
    ).group_by(ListenEvent.artist)
    
    previous_results = previous_query.all()
    previous_df = pd.DataFrame(previous_results, columns=['artist', 'previous_streams'])
    
    # Merge dataframes
    df = recent_df.merge(previous_df, on='artist', how='left')
    df['previous_streams'] = df['previous_streams'].fillna(0)
    
    # Calculate growth rate (avoid division by zero)
    df['growth_rate'] = df.apply(
        lambda row: (
            ((row['current_streams'] - row['previous_streams']) / row['previous_streams'] * 100)
            if row['previous_streams'] > 0
            else (100.0 if row['current_streams'] > 0 else 0.0)
        ),
        axis=1
    )
    
    # Sort by growth rate and limit
    df = df.sort_values('growth_rate', ascending=False).head(limit)
    
    # Convert to response format
    response = []
    for _, row in df.iterrows():
        response.append(RisingArtistResponse(
            artist=row['artist'],
            growth_rate=float(row['growth_rate']),
            current_streams=int(row['current_streams']),
            previous_streams=int(row['previous_streams'])
        ))
    
    return response
