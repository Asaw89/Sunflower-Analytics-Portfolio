import ollama
import psycopg2

SCHEMA_CONTEXT = """
You are a SQL expert for a music streaming analytics database named 'ziplistendb'.

Available tables and columns:

1. summary_artist_popularity_by_geo
   - region_name (text) - e.g., 'Northwest', 'Midwest', 'Northeast','Southwest','Southeast'
   - artist (text) - artist name
   - play_count (integer) - total number of plays
   - unique_listeners (integer) - unique users who listened
   - last_updated (timestamp)

2. summary_genre_by_region
   - region_name (text)
   - genre (text) - music genre
   - listen_count (integer) - total listens

3. summary_subscribers_by_region
   - region_name (text)
   - level (text) - 'free' or 'paid'
   - subscriber_count (integer)

Convert user questions to PostgreSQL queries.
Return ONLY the SQL query with no explanation.
Use the exact column and table names provided.
"""


def generate_sql(question):
    """Convert natural language to SQL"""
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": SCHEMA_CONTEXT},
            {"role": "user", "content": f"Convert this to SQL: {question}"},
        ],
    )
    return response["message"]["content"].strip()


def execute_query(sql):
    try:
        conn = psycopg2.connect(
            host="xo.zipcode.rocks",
            port=9088,
            database="sunflower",  # Changed from "sunflower"
            user="sunflower_user",  # Changed from "sunflower_user"
            password="zipmusic",  # Changed from "zipmusic"
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        conn.close()
        return results, column_names
    except Exception as e:
        return f"Error: {e}", None


def format_answer(question, results, columns):
    """Format results into natural language"""
    if isinstance(results, str):  # Error occurred
        return results

    # Format results for the model
    formatted_data = []
    for row in results:
        row_dict = dict(zip(columns, row))
        formatted_data.append(row_dict)

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "user",
                "content": f"User asked: '{question}'\n\nQuery results: {formatted_data}\n\nProvide a friendly, conversational answer in 1-2 sentences.",
            }
        ],
    )
    return response["message"]["content"]


# Test the full pipeline
questions = [
    "Who is the top artist in the Northeast?",
    "What are the top 5 genres in the Midwest?",
    "How many paid subscribers are in the Southeast region?",
]

for question in questions:
    print(f"\n{'=' * 80}")
    print(f"Question: {question}")

    # Generate SQL
    sql = generate_sql(question)
    print(f"SQL: {sql}")

    # Execute query
    results, columns = execute_query(sql)
    print(f"Raw Results: {results}")

    # Format answer
    answer = format_answer(question, results, columns)
    print(f"Answer: {answer}")
