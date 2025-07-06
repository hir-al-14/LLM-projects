from langchain_community.vectorstores import PGVector
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA
import os

# Database & model config
DB_LINK = "postgresql+psycopg2://hiral:123@localhost:5432/travel_blog"
COLLECTION_NAME = "blogs"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3"

# Initialize embedding and vector store
embedding = OllamaEmbeddings(model=EMBEDDING_MODEL)

vectorstore = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=DB_LINK,
    embedding_function=embedding,
)

# Create retriever and QA chain
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
llm = OllamaLLM(model=LLM_MODEL)

qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

print("\nLangChain Travel Assistant is ready!")
print("Ask travel questions")
print("Type 'exit' to quit.")

# Chat loop
while True:
    query = input("Your Question: ")
    if query.lower() in ["exit", "quit"]:
        print("Exiting Travel Assistant.")
        break
    try:
        answer = qa_chain.invoke(query)
        print("\nAnswer:\n" + answer["result"])
    except Exception as e:
        print(f"Error: {e}")
