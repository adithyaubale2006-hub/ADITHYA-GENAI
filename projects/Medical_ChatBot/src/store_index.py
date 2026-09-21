import os
import time
from dotenv import load_dotenv
from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

# Load environment variables securely
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is missing from your .env file.")

print("1. Extracting text from PDFs in Data/ folder...")
extracted_data = load_pdf_file(data='Data/')

print("2. Splitting text into chunks...")
text_chunks = text_split(extracted_data)

print("3. Loading HuggingFace embeddings model...")
embeddings_model = download_hugging_face_embeddings()

index_name = "medibot-384"
pc = Pinecone(api_key=PINECONE_API_KEY)

print(f"4. Checking Pinecone for index: {index_name}...")
if index_name not in pc.list_indexes().names():
    print(f"   Index not found. Creating '{index_name}'...")
    
    # Dynamically calculating the dimension based on the model
    dimension_size = len(embeddings_model.embed_query("dimension check"))
    
    pc.create_index(
        name=index_name,
        dimension=dimension_size,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

print("   Waiting for index to initialize...")
while not pc.describe_index(index_name).status["ready"]:
    time.sleep(1)

print(f"5. Uploading {len(text_chunks)} chunks to Pinecone (this may take a moment)...")
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings_model,
)

print("✅ Ingestion complete! You can now start your Flask app.")