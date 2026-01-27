"""
Add genres to listen_events table using MusicBrainz API.
Looks up each unique artist and adds their primary genre.
No API key required!
"""

import time
import requests
from sqlalchemy import create_engine, text

# Database setup
DATABASE_URL = "postgresql://sunflower_user:zipmusic@xo.zipcode.rocks:9088/sunflower"
engine = create_engine(DATABASE_URL)

# MusicBrainz requires a User-Agent header
HEADERS = {"User-Agent": "SunflowerAnalytics/1.0"}


def get_artist_genre(artist_name):
    """Look up artist on MusicBrainz and return their primary genre/tag."""
    try:
        # Search for artist
        search_url = "https://musicbrainz.org/ws/2/artist/"
        params = {"query": artist_name, "fmt": "json", "limit": 1}

        response = requests.get(search_url, params=params, headers=HEADERS)

        if not response.ok:
            return None

        data = response.json()

        if not data.get("artists"):
            return None

        artist = data["artists"][0]

        # Get tags (genres) - they're sorted by vote count
        tags = artist.get("tags", [])
        if tags:
            # Filter out non-genre tags and get the highest voted one
            genre_tags = [t for t in tags if t.get("count", 0) > 0]
            if genre_tags:
                # Sort by count and return top tag
                genre_tags.sort(key=lambda x: x.get("count", 0), reverse=True)
                return genre_tags[0]["name"].title()

        return None

    except Exception as e:
        print(f"  Error looking up {artist_name}: {e}")
        return None


def add_genre_column():
    """Add genre column to listen_events if it doesn't exist."""
    with engine.connect() as conn:
        conn.execute(
            text("""
            ALTER TABLE listen_events 
            ADD COLUMN IF NOT EXISTS genre VARCHAR(100)
        """)
        )
        conn.commit()
    print("✓ Genre column ready")


def get_unique_artists():
    """Get all unique artists from listen_events that don't have genres yet."""
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
        artists = [row[0] for row in result]
    return artists


def update_artist_genre(artist_name, genre):
    """Update all rows for an artist with their genre."""
    with engine.connect() as conn:
        conn.execute(
            text("UPDATE listen_events SET genre = :genre WHERE artist = :artist"),
            {"genre": genre, "artist": artist_name},
        )
        conn.commit()


def main():
    print("=" * 60)
    print("  ADDING GENRES TO LISTEN_EVENTS (MusicBrainz)")
    print("=" * 60)

    # Add genre column
    add_genre_column()

    # Get unique artists
    artists = get_unique_artists()
    print(f"\nFound {len(artists):,} unique artists")
    print("Note: MusicBrainz rate limit is 1 request/second")
    print("This may take a while...\n")

    # Look up genres
    genres_found = 0
    genres_not_found = []

    for i, artist in enumerate(artists, 1):
        print(f"[{i}/{len(artists)}] Looking up: {artist}...", end=" ", flush=True)

        genre = get_artist_genre(artist)

        if genre:
            update_artist_genre(artist, genre)
            print(f"✓ {genre}")
            genres_found += 1
        else:
            print("✗ Not found")
            genres_not_found.append(artist)

        # MusicBrainz rate limit: 1 request per second
        time.sleep(1.1)

    # Summary
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"✓ Genres found: {genres_found}")
    print(f"✗ Genres not found: {len(genres_not_found)}")

    if genres_not_found and len(genres_not_found) <= 20:
        print(f"\nArtists without genres: {genres_not_found}")

    # Show genre distribution
    print("\nTop 10 genres in your data:")
    with engine.connect() as conn:
        result = conn.execute(
            text("""
            SELECT genre, COUNT(*) as count 
            FROM listen_events 
            WHERE genre IS NOT NULL
            GROUP BY genre 
            ORDER BY count DESC 
            LIMIT 10
        """)
        )
        for row in result:
            print(f"  {row[0]}: {row[1]:,} plays")


if __name__ == "__main__":
    main()
