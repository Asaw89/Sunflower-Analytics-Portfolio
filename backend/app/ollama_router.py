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
   - region_name (text) - US STATE abbreviations like 'NY', 'CA', 'TX', 'FL'
   - play_count (integer) - total number of plays
   - unique_listeners (integer) - unique users who listened

2. summary_genre_by_region
   - genre (text) - music genre
   - last_updated (timestamp)
   - region_name (text) - US REGIONS: 'West', 'Midwest', 'Northeast', 'Southeast'
   - listen_count (integer) - total listens

3. summary_subscribers_by_region
   - last_updated (timestamp)
   - level (text) - 'free' or 'paid'
   - region_name (text) - US REGIONS: 'West', 'Midwest', 'Northeast', 'Southeast'
   - subscriber_count (integer)

[... rest of your tables ...]

IMPORTANT QUERY RULES:
- summary_artist_popularity_by_geo uses STATE codes (NY, CA, TX)
- summary_genre_by_region uses REGIONS (West, Midwest, Northeast, Southeast)
- summary_subscribers_by_region uses REGIONS (West, Midwest, Northeast, Southeast)
- For city queries, use summary_city_growth_trends with STATE codes
- When users ask about genres or subscribers by REGION, use: West, Midwest, Northeast, Southeast
- When users ask about artists or cities by STATE, use: NY, CA, TX, FL, etc.


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
        if not results:
            return (
                "No data found for this query. Try asking about artists, genres, cities, subscribers, device types, or retention metrics.",
                None,
            )

        return results, column_names
    except Exception as e:
        # More helpful error messages
        if "column" in str(e).lower() and "does not exist" in str(e).lower():
            raise HTTPException(
                status_code=400,
                detail="That data doesn't exist in our database. Try asking about artists, genres, cities, subscribers, or device usage.",
            )
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
