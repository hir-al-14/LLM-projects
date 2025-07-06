# 🤖 Resume Finder Chatbot
#### This project is a Resume assistant that parses resume PDFs, extracts its information.  into different sections like name, skills, experience, and projects. It then converts it into vector embeddings using Ollama, and stores it in a PostgreSQL database using pgvector. It enables natural language search over resumes using LangChain and Llama3, where you can semantically query candidate resumes based on skills, experience, and project relevance, etc.
## How it works-
1. **SCRAPING RESUMES-**  Uses Beautiful Soup to scrape resumes from a northguru cv dataset.
2. **PDF Parsing-** Extracts text from pdf using pdfplumber and then uses regex to split sections into name, education, experience, skills, projects.
3. **STORING DATA-** Stores the text spiolt into sections into a csv.
4. **EMBEDDINGS-** Uses the csv to generated embeddings using Ollama with nomic-embed-text for each resume.
5. **SEMANTIC SEARCH-** Loaded resumes from the database and chunks the content using LangChain's RecursiveCharacterTextSplitter.
6. **QA Chain-** Used LangChain’s RetrievalQA combining Llama3 LLM and PGVector retriever for answering natural language queries.
