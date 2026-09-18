+---------------------+
|  1. Data Ingestion  |
|  (PyMuPDFReader)    |
|  File: TGR.pdf      |
+----------+----------+
           | (Creates Document Objects)
           v
+----------+----------+      +-----------------------+
|  2. Global Settings |      |  3. Embedding Model   |
|  - LLM: Gemini      |      |  - HuggingFace BGE    |
|  - Chunk Size: 800  |      |  - BAAI/bge-small     |
|  - Overlap: 20      |      |                       |
+----------+----------+      +----------+------------+
           |                            |
           +-------------+--------------+
                         |
                         v
              +----------+-----------+
              |  4. Vector Index     |
              | (VectorStoreIndex)   |
              +----------+-----------+
                         | (Persist to Disk)
               +---------+---------+
               |  Local Storage    |
               | (./storage)       |
               +---------+---------+
                         | (Load Index)
                         v
              +----------+-----------+
User Query -> |  5. Query Engine     | -> LLM Final Response
              | (Retrieval & Synth)| -> Display Source Nodes
              +----------------------+
