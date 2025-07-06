# takes input query, makes a retriever of the embedding data from the database, combines the llama3 llm and retriever to forma a RetrievalQA chain to answer the query.
from langchain_community.vectorstores import PGVector
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DataFrameLoader
from sqlalchemy import create_engine
from langchain_ollama import OllamaLLM
import pandas as pd

engine = create_engine("postgresql+psycopg2://hiral:123@localhost:5432/job_scrape")
df = pd.read_sql("SELECT name, experience, skills, projects FROM resumes", engine)

df["content"] = (
    "Name: " + df["name"].fillna("") +
    "\nExperience: " + df["experience"].fillna("") +
    "\nSkills: " + df["skills"].fillna("") +
    "\nProjects: " + df["projects"].fillna("")
)
docs = DataFrameLoader(df[["content"]], page_content_column="content").load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(docs)

embedding = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = PGVector.from_documents(
    documents=split_docs,
    embedding=embedding,
    collection_name="resume_chunks",
    connection_string="postgresql+psycopg2://hiral:123@localhost:5432/job_scrape" 
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = OllamaLLM(model="llama3")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


print("\nLangChain Resume Assistant is ready! Type 'quit/exit' to exit.")

while True:
    question = input("\nAsk your question: ")
    if question.lower() in ("quit", "exit"):
        print("Exiting assistant.")
        break 
    try:
        answer = qa_chain.invoke(question)
        print("\nAnswer:")
        print(answer)
    except Exception as e:
        print(f"Error: {e}")