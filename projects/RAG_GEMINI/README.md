### IMPLEMENTATION OF RAG CONCEPT

### CREATE ENVIRONMENT
conda create -n rag python=3.12 -y

### ACTIVATE
conda activate rag

### INSTALL REQUIREMENTS
pip install -r requirements.txt

### RUN THE APP
streamlit run app.py

### CREATE A .env FILE FOR API_KEY
GEMINI_API_KEY = "API_KEY"


