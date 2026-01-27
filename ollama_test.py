import ollama

# Your actual database schema
SCHEMA_CONTEXT = """
You are a SQL expert for a music streaming analytics database named 'sunflower'.

Available tables and columns:

1. summary_artist_popularity_by_geo
   - region_name (text) - e.g., 'California', 'Texas', 'Northeast'
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


def ask_question(question):
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": SCHEMA_CONTEXT},
            {"role": "user", "content": f"Convert this to SQL: {question}"},
        ],
    )
    return response["message"]["content"]


# Test questions
questions = [
    "Who is the top artist in California?",
    "What are the top 5 genres in Texas?",
    "How many paid subscribers are in the Northeast region?",
]

for q in questions:
    print(f"\nQuestion: {q}")
    print(f"SQL: {ask_question(q)}")
    print("-" * 80)
