from src.helper import repo_ingestion, load_repo, text_splitter, load_embedding
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma # Updated from langchain_classic
import os

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# url = "https://github.com/adithyaubale2006-hub/ADITHYA-GENAI.git"
# repo_ingestion(url)

# 1. Load the documents from the repo
documents = load_repo("repo/")

# 2. Split documents into chunks
text_chunks = text_splitter(documents)

# 3. Load the embedding model
embeddings = load_embedding()

# 4. Store vectors in ChromaDB 
vectordb = Chroma.from_documents(
    documents=text_chunks, 
    embedding=embeddings, 
    persist_directory='./chroma_db'
)

# Persist the database to disk (Optional but recommended for the tutorial)
vectordb.persist()