import os  
from git import Repo
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

# Function to clone the github repository
def repo_ingestion():
    os.makedirs("repo", exist_ok=True)
    repo_path = "repo/"
    repo_url = "https://github.com/adithyaubale2006-hub/ADITHYA-GENAI.git"
    Repo.clone_from(repo_url, to_path=repo_path)
    
    return repo_path 

# Load The Repo and the documents
def load_repo(repo_path):
    # Sets up a document loader to search through the cloned repository
    loader = GenericLoader.from_filesystem(repo_path,
                                       glob="**/*",
                                       suffixes=[".py"],
                                       parser=LanguageParser(language=Language.PYTHON)
                                       )
    
    documents = loader.load()

    return documents

# Creating Chunks
def create_chunks(documents): # Added 'documents' as a parameter
    documents_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=500,
        chunk_overlap=20
    )
    text_chunks = documents_splitter.split_documents(documents)

    return text_chunks



# Add this function to the bottom of helper.py
def load_embedding():
    # You can specify a different model name here if the tutorial uses a specific one
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings

# Execution Check
if __name__ == "__main__":
    print("Cloning repo...")
    path = repo_ingestion()
    
    print("Loading documents...")
    docs = load_repo(path)
    print(f"Loaded {len(docs)} documents.")
    
    print("Splitting into chunks...")
    chunks = create_chunks(docs)
    print(f"Created {len(chunks)} text chunks.")

    print("Loading Embeddings")
    embebeddings = load_embedding()
    
