# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API does not require authentication (development mode).

## Endpoints

### Health Check

#### GET /health
Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

### Root

#### GET /
Get API information and available endpoints.

**Response:**
```json
{
  "message": "Welcome to Zip Listen Analytics API",
  "version": "1.0.0",
  "endpoints": [
    "/api/genres/by-region",
    "/api/subscribers/by-region",
    "/api/artists/top",
    "/api/artists/rising"
  ]
}
```

---

## Analytics Endpoints

### Genres by Region

#### GET /api/genres/by-region
Get music genre distribution across US regions.

**Query Parameters:**
| Parameter | Type   | Required | Description                                           |
|-----------|--------|----------|-------------------------------------------------------|
| region    | string | No       | Filter by specific region (Northeast, Southeast, Midwest, West) |

**Example Request:**
```bash
# Get all genres by region
curl http://localhost:8000/api/genres/by-region

# Filter by specific region
curl "http://localhost:8000/api/genres/by-region?region=Northeast"
```

**Response:**
```json
[
  {
    "region": "Northeast",
    "genre": "Pop",
    "stream_count": 150
  },
  {
    "region": "Northeast",
    "genre": "Rock",
    "stream_count": 89
  },
  {
    "region": "West",
    "genre": "Hip-Hop",
    "stream_count": 203
  }
]
```

**Response Fields:**
| Field        | Type    | Description                      |
|--------------|---------|----------------------------------|
| region       | string  | US region name                   |
| genre        | string  | Music genre                      |
| stream_count | integer | Number of streams in this category |

---

### Subscribers by Region

#### GET /api/subscribers/by-region
Get subscriber distribution (paid vs free) across US regions.

**Query Parameters:**
| Parameter | Type   | Required | Description                                           |
|-----------|--------|----------|-------------------------------------------------------|
| region    | string | No       | Filter by specific region (Northeast, Southeast, Midwest, West) |

**Example Request:**
```bash
# Get all subscribers by region
curl http://localhost:8000/api/subscribers/by-region

# Filter by specific region
curl "http://localhost:8000/api/subscribers/by-region?region=West"
```

**Response:**
```json
[
  {
    "region": "Northeast",
    "level": "paid",
    "user_count": 50
  },
  {
    "region": "Northeast",
    "level": "free",
    "user_count": 23
  },
  {
    "region": "West",
    "level": "paid",
    "user_count": 67
  }
]
```

**Response Fields:**
| Field      | Type    | Description                           |
|------------|---------|---------------------------------------|
| region     | string  | US region name                        |
| level      | string  | Subscription level (paid or free)     |
| user_count | integer | Number of unique users in this category |

---

### Top Artists

#### GET /api/artists/top
Get top artists ranked by total stream count.

**Query Parameters:**
| Parameter | Type    | Required | Default | Description                         |
|-----------|---------|----------|---------|-------------------------------------|
| limit     | integer | No       | 10      | Number of top artists to return (1-100) |

**Example Request:**
```bash
# Get top 10 artists (default)
curl http://localhost:8000/api/artists/top

# Get top 20 artists
curl "http://localhost:8000/api/artists/top?limit=20"
```

**Response:**
```json
[
  {
    "artist": "Taylor Swift",
    "stream_count": 500,
    "rank": 1
  },
  {
    "artist": "Drake",
    "stream_count": 432,
    "rank": 2
  },
  {
    "artist": "Ed Sheeran",
    "stream_count": 387,
    "rank": 3
  }
]
```

**Response Fields:**
| Field        | Type    | Description                      |
|--------------|---------|----------------------------------|
| artist       | string  | Artist name                      |
| stream_count | integer | Total number of streams          |
| rank         | integer | Ranking position (1 = highest)  |

---

### Rising Artists

#### GET /api/artists/rising
Get rising artists based on growth rate between time periods.

The endpoint compares streams from the most recent 7 days vs the previous 7 days (8-14 days ago) to calculate growth rate.

**Query Parameters:**
| Parameter | Type    | Required | Default | Description                           |
|-----------|---------|----------|---------|---------------------------------------|
| limit     | integer | No       | 10      | Number of rising artists to return (1-100) |

**Example Request:**
```bash
# Get top 10 rising artists (default)
curl http://localhost:8000/api/artists/rising

# Get top 5 rising artists
curl "http://localhost:8000/api/artists/rising?limit=5"
```

**Response:**
```json
[
  {
    "artist": "NewArtist1",
    "growth_rate": 150.5,
    "current_streams": 100,
    "previous_streams": 40
  },
  {
    "artist": "EmergingBand",
    "growth_rate": 87.3,
    "current_streams": 234,
    "previous_streams": 125
  }
]
```

**Response Fields:**
| Field            | Type    | Description                                    |
|------------------|---------|------------------------------------------------|
| artist           | string  | Artist name                                    |
| growth_rate      | float   | Percentage growth rate between periods         |
| current_streams  | integer | Stream count in most recent 7 days            |
| previous_streams | integer | Stream count in previous 7 days (8-14 days ago) |

**Growth Rate Calculation:**
- If previous_streams > 0: `((current_streams - previous_streams) / previous_streams) * 100`
- If previous_streams = 0 and current_streams > 0: `100.0` (new artist)
- Otherwise: `0.0`

---

## Error Responses

All endpoints may return the following error responses:

### 422 Unprocessable Entity
Invalid query parameters.

```json
{
  "detail": [
    {
      "loc": ["query", "limit"],
      "msg": "ensure this value is less than or equal to 100",
      "type": "value_error.number.not_le"
    }
  ]
}
```

### 500 Internal Server Error
Server error (database connection issues, etc.).

```json
{
  "detail": "Internal server error"
}
```

---

## Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- View all endpoints and their parameters
- Test API calls directly from the browser
- See request/response schemas
- Download OpenAPI specification

---

## Rate Limiting

Currently, there are no rate limits in place (development mode). In production, implement rate limiting based on your requirements.

---

## Data Freshness

Data is queried in real-time from the PostgreSQL database. No caching is currently implemented. For production use, consider adding caching for frequently accessed endpoints.

---

## CORS

CORS is enabled for all origins in development mode. For production, update the allowed origins in `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Sample Data

The database is initialized with sample data including:
- 45+ listen events across different genres and regions
- Auth events for multiple users
- Status change events showing subscription transitions
- Coverage of all 4 US regions
- Mix of paid and free users

You can modify or extend the sample data in `init_db.sql`.
