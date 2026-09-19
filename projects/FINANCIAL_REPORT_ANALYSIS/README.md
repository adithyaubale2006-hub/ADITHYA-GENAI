### ARCHITECTURE

Financial Reports / Stock Data
          ↓
      Data Loading
          ↓
     LlamaIndex
          ↓
   Document Chunking
          ↓
      Embeddings
          ↓
    Vector Database
          ↓
    Retrieval (RAG)
          ↓
       LLM
          ↓
 Financial Analysis / Q&A
          ↓
      Streamlit UI


### FOLDER STURCTURE

06-financial-stock-analysis/
│
├── data/
│   ├── financial_reports/
│   └── stock_data/
│
├── src/
│   ├── data_loader.py
│   ├── indexer.py
│   ├── retriever.py
│   ├── financial_analyzer.py
│   └── utils.py
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md