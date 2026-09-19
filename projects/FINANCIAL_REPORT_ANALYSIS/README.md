### ARCHITECTURE

```text
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


```

```text
### HOW TO RUN

1. conda create -n fine-env python=3.12 -y
2. conda activate fine-env

3. pip install -r requirements.txt
4. test the .ipynb file
5. streamlit run app.py
```
