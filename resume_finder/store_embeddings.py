# Gets the resumes text from the csv, combines all the text, forms its embedding using Ollama, and then stores it in the database.
import pandas as pd
import psycopg2
from pgvector.psycopg2 import register_vector
import requests
import json

conn = psycopg2.connect(
    dbname="job_scrape",
    user="hiral",
    password="123",
    host="localhost",
    port=5432
)
register_vector(conn)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS resumes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    skills TEXT,
    experience TEXT,
    education TEXT,
    projects TEXT,
    source_file TEXT,
    embedding VECTOR(768)
);
""")
conn.commit()

df = pd.read_csv("output/resume_index.csv")

all_embeddings = []
for _, row in df.iterrows():
    combined_text = f"Name: {row['name']}\nExperience: {row['experience']}\nSkills: {row['skills']}\nProjects: {row['projects']}\nEducation: {row['education']}"

    try:
        res = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": combined_text}
        )
        res.raise_for_status()
        embedding = res.json()["embedding"]
        all_embeddings.append((row['source_file'], embedding))
    except Exception as e:
        print(f"Embedding failed for {row['source_file']}: {e}")
        continue

    cursor.execute("""
        INSERT INTO resumes (name, skills, experience, projects, education, source_file, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row["name"],
        row["skills"],
        row["experience"],
        row['projects'],
        row["education"],
        row["source_file"],
        embedding
    ))

conn.commit()
conn.close()

print("STORED")