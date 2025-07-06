# 🤖 Travel Planner Chatbot
#### This project is a travel-focused semantic chatbot that fetches and parses destination content from Wikivoyage using the MediaWiki API, structures it into sections (like “Get In,” “See,” “Do,” etc.), and stores both the text and its vector embeddings in a PostgreSQL database using pgvector. It enables natural language queries using LangChain and Llama3 to retrieve relevant, sectioned content from travel data across global cities.

## How it works-
1. **DATA FETCHING-**  Uses the MediaWiki API to get HTML content from Wikivoyage pages and parses it into clean sections using BeautifulSoup.
2. **PDF Parsing-** Extracts text from pdf using pdfplumber and then uses regex to split sections into name, education, experience, skills, projects.
3. **STORING DATA-** Stores the text spiolt into sections into a csv.
4. **EMBEDDINGS-** Uses the csv to generated embeddings using Ollama with nomic-embed-text for each resume.
5. **SEMANTIC SEARCH-** Loaded resumes from the database and chunks the content using LangChain's RecursiveCharacterTextSplitter.
6. **QA Chain-** Used LangChain’s RetrievalQA combining Llama3 LLM and PGVector retriever for answering natural language queries.

