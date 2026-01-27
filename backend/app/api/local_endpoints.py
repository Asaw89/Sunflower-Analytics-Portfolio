from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2
from pydantic import BaseModel

router = APIRouter()

# Database connection config
DB_CONFIG = {
    "host": "db",
    "port": 5432,
    "database": "ziplistendb",
    "user": "zipuser",
    "password": "zippassword",
}


# Response models
class GenreByRegion(BaseModel):
    region: str
    genre: str
    stream_count: int


class SubscriberByRegion(BaseModel):
    region: str
    level: str
    user_count: int


class TopArtist(BaseModel):
    artist: str
    stream_count: int


class RisingArtist(BaseModel):
    artist: str
    growth_rate: float


def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_CONFIG)


@router.get("/genres/by-region", response_model=List[GenreByRegion])
async def get_genres_by_region():
    """Get genre distribution by region"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT region_name as region, genre, listen_count as stream_count
        FROM summary_genre_by_region
        ORDER BY region_name, listen_count DESC;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        return [
            GenreByRegion(region=row[0], genre=row[1], stream_count=row[2])
            for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/subscribers/by-region", response_model=List[SubscriberByRegion])
async def get_subscribers_by_region():
    """Get subscriber distribution by region"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT region_name as region, level, subscriber_count as user_count
        FROM summary_subscribers_by_region
        ORDER BY region_name, level;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        return [
            SubscriberByRegion(region=row[0], level=row[1], user_count=row[2])
            for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/artists/top", response_model=List[TopArtist])
async def get_top_artists(limit: int = 10):
    """Get top artists by play count"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT artist, SUM(play_count) as stream_count
        FROM summary_artist_popularity_by_geo
        GROUP BY artist
        ORDER BY stream_count DESC
        LIMIT %s;
        """

        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        conn.close()

        return [TopArtist(artist=row[0], stream_count=row[1]) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/artists/rising", response_model=List[RisingArtist])
async def get_rising_artists(limit: int = 10):
    """Get rising artists by unique listener ratio"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Calculate growth rate as (unique_listeners / play_count * 100)
        # Higher ratio = more engaged/rising artist
        query = """
        SELECT 
            artist,
            (SUM(unique_listeners)::float / NULLIF(SUM(play_count), 0) * 100) as growth_rate
        FROM summary_artist_popularity_by_geo
        GROUP BY artist
        HAVING SUM(play_count) > 100
        ORDER BY growth_rate DESC
        LIMIT %s;
        """

        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        conn.close()

        return [
            RisingArtist(artist=row[0], growth_rate=round(row[1], 2)) for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
