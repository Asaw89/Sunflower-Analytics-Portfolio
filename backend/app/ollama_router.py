from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import ollama
import psycopg2
from typing import List, Dict, Any

client = ollama.Client(host="http://host.docker.internal:11434")

router = APIRouter(prefix="/api/ollama", tags=["ollama"])


class QuestionRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    sql: str
    answer: str
    raw_data: List[Dict[str, Any]]


SCHEMA_CONTEXT = """
You are a SQL expert for a music streaming analytics database named 'ziplistendb'.

Available tables and columns:

1. summary_artist_popularity_by_geo
   - artist (text) - artist name
   - last_updated (timestamp)
   - region_name (text) - US state abbreviations like 'NY', 'CA', 'TX'
   - play_count (integer) - total number of plays
   - unique_listeners (integer) - unique users who listened

2. summary_genre_by_region
   - genre (text) - music genre
   - last_updated (timestamp)
   - region_name (text) - US state abbreviations
   - listen_count (integer) - total listens

3. summary_subscribers_by_region
   - last_updated (timestamp)
   - level (text) - 'free' or 'paid'
   - region_name (text) - US state abbreviations
   - subscriber_count (integer) - number of subscribers

4. summary_city_growth_trends
   - city (text) - city name
   - date (date) - data collection date
   - last_updated (timestamp)
   - state (text) - US state abbreviation
   - new_users (integer) - new users in this city
   - percent_growth_wow (numeric) - week-over-week growth percentage
   - total_streaming_hours (integer) - total hours streamed

5. summary_platform_usage
   - device_type (text) - device type (e.g., 'mobile', 'desktop', 'tablet')
   - last_updated (timestamp)
   - region_name (text) - US region
   - active_users (integer) - number of active users
   - play_count (integer) - total plays on this device

6. summary_retention_cohort
   - cohort_month (date) - cohort starting month
   - last_updated (timestamp)
   - churned_users (integer) - users who left
   - downgrades (integer) - users who downgraded
   - period (integer) - time period
   - upgrades (integer) - users who upgraded

IMPORTANT: 
- When asked for totals across regions/cities, use SUM()
- When asking about specific locations, filter by region_name, state, or city
- Use state abbreviations (NY, CA, TX) for region_name and state fields
- For growth queries, use summary_city_growth_trends
- For device/platform queries, use summary_platform_usage
- For retention/churn queries, use summary_retention_cohort

Convert user questions to PostgreSQL queries.
Return ONLY the SQL query with no explanation.
Use the exact column and table names provided.
"""


def generate_sql(question: str) -> str:
    """Convert natural language to SQL using Ollama"""
    response = client.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": SCHEMA_CONTEXT},
            {"role": "user", "content": f"Convert this to SQL: {question}"},
        ],
    )
    return response["message"]["content"].strip()


def execute_query(sql: str) -> tuple:
    """Execute SQL on PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host="db",  # This is the Docker service name from docker-compose.yml
            port=5432,
            database="ziplistendb",
            user="zipuser",
            password="zippassword",
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        conn.close()
        return results, column_names
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def format_answer(question: str, results: list, columns: list) -> str:
    """Format results into natural language using Ollama"""
    formatted_data = []
    for row in results:
        row_dict = dict(zip(columns, row))
        formatted_data.append(row_dict)

    response = client.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "user",
                "content": f"User asked: '{question}'\n\nQuery results: {formatted_data}\n\nProvide a friendly, conversational answer in 1-2 sentences.",
            }
        ],
    )
    return response["message"]["content"]


@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QuestionRequest):
    """
    Natural language query endpoint.

    Takes a natural language question about music data and returns:
    - The generated SQL query
    - A natural language answer
    - Raw data results
    """
    try:
        # Generate SQL from natural language
        sql = generate_sql(request.question)

        # Execute query on database
        results, columns = execute_query(sql)

        # Format results into natural language
        answer = format_answer(request.question, results, columns)

        # Format raw data as list of dicts
        raw_data = [dict(zip(columns, row)) for row in results]

        return QueryResponse(
            question=request.question, sql=sql, answer=answer, raw_data=raw_data
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
