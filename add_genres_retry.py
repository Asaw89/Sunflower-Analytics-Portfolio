"""
Add genres to listen_events - WITH RETRY LOGIC
Handles connection drops from XO server.
"""

import time
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# XO Database
DATABASE_URL = "postgresql://sunflower_user:zipmusic@xo.zipcode.rocks:9088/sunflower"

HEADERS = {"User-Agent": "SunflowerAnalytics/1.0"}

# Cache for genres
genre_cache = {}


def get_engine():
    """Create a fresh database connection."""
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def retry_on_disconnect(func, max_retries=3):
    """Retry a database operation if connection drops."""
    for attempt in range(max_retries):
        try:
            return func()
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(
                    f"\n  Connection dropped, reconnecting (attempt {attempt + 2})..."
                )
                time.sleep(2)
            else:
                raise e


def get_artist_genre(artist_name):
    """Look up artist on MusicBrainz."""
    if artist_name in genre_cache:
        return genre_cache[artist_name]

    try:
        search_url = "https://musicbrainz.org/ws/2/artist/"
        params = {"query": artist_name, "fmt": "json", "limit": 1}
        response = requests.get(search_url, params=params, headers=HEADERS, timeout=10)

        if not response.ok:
            genre_cache[artist_name] = None
            return None

        data = response.json()

        if not data.get("artists"):
            genre_cache[artist_name] = None
            return None

        artist = data["artists"][0]
        tags = artist.get("tags", [])

        if tags:
            genre_tags = [t for t in tags if t.get("count", 0) > 0]
            if genre_tags:
                genre_tags.sort(key=lambda x: x.get("count", 0), reverse=True)
                genre = genre_tags[0]["name"].title()
                genre_cache[artist_name] = genre
                return genre

        genre_cache[artist_name] = None
        return None

    except Exception as e:
        print(f"  API Error: {e}")
        genre_cache[artist_name] = None
        return None


def update_artist_genre(engine, artist_name, genre):
    """Update genre with retry logic."""

    def do_update():
        with engine.connect() as conn:
            conn.execute(
                text("UPDATE listen_events SET genre = :genre WHERE artist = :artist"),
                {"genre": genre, "artist": artist_name},
            )
            conn.commit()

    retry_on_disconnect(do_update)


def main():
    print("=" * 60)
    print("  ADDING GENRES (with retry logic)")
    print("=" * 60)

    engine = get_engine()

    # Add genre column if needed
    def add_column():
        with engine.connect() as conn:
            conn.execute(
                text(
                    "ALTER TABLE listen_events ADD COLUMN IF NOT EXISTS genre VARCHAR(100)"
                )
            )
            conn.commit()

    retry_on_disconnect(add_column)
    print("✓ Genre column ready")

    # Get artists without genres
    def get_artists():
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                SELECT DISTINCT artist 
                FROM listen_events 
                WHERE artist IS NOT NULL
                AND (genre IS NULL OR genre = '')
                ORDER BY artist
            """)
            )
            return [row[0] for row in result]

    artists = retry_on_disconnect(get_artists)
    print(f"\nFound {len(artists):,} artists without genres")
    print("This will take a while... (Ctrl+C to stop)\n")

    # Process artists
    genres_found = 0

    for i, artist in enumerate(artists, 1):
        print(f"[{i}/{len(artists)}] {artist}...", end=" ", flush=True)

        genre = get_artist_genre(artist)

        if genre:
            try:
                # Refresh engine every 500 artists to prevent stale connections
                if i % 500 == 0:
                    engine = get_engine()
                    print("\n  (Refreshed connection)")

                update_artist_genre(engine, artist, genre)
                print(f"✓ {genre}")
                genres_found += 1
            except Exception as e:
                print(f"✗ DB Error: {e}")
                engine = get_engine()  # Reconnect
        else:
            print("✗ Not found")

        time.sleep(1.1)

    # Summary
    print("\n" + "=" * 60)
    print(f"  DONE! Added genres to {genres_found} artists")
    print("=" * 60)


if __name__ == "__main__":
    main()
