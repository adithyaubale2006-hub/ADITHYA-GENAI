# End-to-End Source Code Analysis Generative AI

This project is a Generative AI-powered Source Code Analyzer built with Flask and LangChain. It allows users to ingest a GitHub repository, convert the codebase into a vector database, and interact with an AI chatbot to ask questions, summarize functions, and understand the architecture of the code.

## 🛠️ Tech Stack Used

- **Python**
- **LangChain**
- **Flask**
- **Google Gemini API** (LLM)
- **HuggingFace** (Embeddings)
- **ChromaDB** (Vector Database)
- **Bootstrap & jQuery** (Frontend UI)

## 📁 Project Structure

```text
├── app.py                # Main Flask application and API routing
├── src/
│   ├── __init__.py
│   └── helper.py         # Functions for repo cloning, chunking, and embeddings
├── templates/
│   └── index.html        # Chat interface UI
├── static/
│   └── style.css         # Custom frontend styling
├── repo/                 # Cloned target repository (gitignored)
├── chroma_db/            # Local vector database storage (gitignored)
├── .env                  # Environment variables (API Keys)
├── .gitignore            # Git exclusions
└── requirements.txt      # Python dependencies
```

### **Environment** 
conda create -n llm-app python=3.11 -y

condata activate llm-app

### **Clone**
git clone <your-repository-url>
cd <your-project-folder>

#### **AUTHOR**
ADITHYA UBALE

