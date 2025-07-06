import pandas as pd
import psycopg2
from pgvector.psycopg2 import register_vector
import requests

conn = psycopg2.connect(
    dbname="travel_blog",
    user="hiral",
    password="123",
    host="localhost",
    port=5432
)

register_vector(conn)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS blogs (
    id SERIAL PRIMARY KEY,
    city TEXT,
    region TEXT,
    section TEXT, 
    text TEXT,
    embedding VECTOR(768)
);
""")
conn.commit()

df = pd.read_csv("data/travel_data.csv")

for _, row in df.iterrows():
    combined_text = f"City: {row['city']}\nRegion: {row['region']}\nSection: {row['section']}\nText: {row['text']}"

    try:
        res = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": combined_text}
        )
        res.raise_for_status()
        embedding = res.json()["embedding"]

        cursor.execute("""
            INSERT INTO blogs (city, region, section, text, embedding)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            row["city"],
            row["region"],
            row["section"],
            row["text"],
            embedding
        ))

    except Exception as e:
        print(f"Embedding failed for {row['city']}: {e}")
        continue

conn.commit()
conn.close()

print("All embeddings stored in PostgreSQL.")
