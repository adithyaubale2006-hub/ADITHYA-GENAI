# Medical Chatbot with RAG

A medical AI assistant that answers health-related questions using a Retrieval-Augmented Generation (RAG) pipeline over PDF medical documents. The app loads PDF files from the `Data/` directory, splits them into chunks, embeds them into a vector database, retrieves the most relevant context, and passes that context to an LLM for response generation.

## Overview

This project is designed to provide:

- General medical information using retrieved source documents
- A simple Flask web interface for user interaction
- PDF ingestion and chunking for local knowledge retrieval
- Pinecone vector search for semantic retrieval
- NVIDIA-hosted LLM access for response generation
- Safety guardrails for emergency and medical disclaimer scenarios

## Features

- PDF document loading using `PyPDFLoader`
- Chunk splitting with `RecursiveCharacterTextSplitter`
- Embeddings using Hugging Face sentence-transformers
- Vector storage in Pinecone
- RAG-based question answering
- Emergency detection for critical symptoms
- Web interface built with Flask
- Clean separation between UI, app logic, and helper modules

## Tech Stack

- Python
- Flask
- LangChain
- Hugging Face Transformers
- Pinecone
- NVIDIA AI Endpoints
- PyPDF
- HTML / CSS / JavaScript

## Project Structure

```text
Medical_ChatBot/
├── app.py                  # Flask app and chatbot logic
├── requirements.txt        # Python dependencies
├── setup.py                # Package metadata
├── README.md               # Project documentation
├── .env                    # Local environment variables (not committed)
├── Data/                   # PDF knowledge base
├── templates/
│   └── index.html          # Web interface
├── static/
│   └── styles.css          # Frontend styling
├── src/
│   ├── __init__.py
│   ├── helper.py
│   ├── prompt.py
│   └── store_index.py
├── research/
│   └── trials.ipynb       # Experimental notebook
└── medical_chatbot.egg-info/
```

## Prerequisites

Before running the app, make sure you have:

- Python 3.10+ recommended
- A Pinecone account and API key
- An NVIDIA API key
- At least one PDF file in the `Data/` directory
- Internet access for model downloads and cloud APIs

## Installation

1. Clone the project:

```bash
git clone <repository-url>
cd Medical_ChatBot
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root with values like:

```env
PINECONE_API_KEY=your_pinecone_api_key
NVIDIA_API_KEY=your_nvidia_api_key
PINECONE_INDEX=medibot-384
DATA_FOLDER=Data
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=openai/gpt-oss-20b
CHUNK_SIZE=500
CHUNK_OVERLAP=50
RETRIEVAL_K=4
PORT=5000
```

Notes:

- Keep your secret keys private and do not commit them to version control.
- `PINECONE_INDEX` should match an existing or intended Pinecone index.
- Ensure the embedding dimension matches the model used in Pinecone.

## Running the Application

Start the Flask app:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## How It Works

1. PDF files are loaded from `Data/`
2. Documents are split into smaller chunks
3. Each chunk is embedded using a Hugging Face transformer model
4. Embeddings are stored in Pinecone
5. A user question is embedded and matched to relevant chunks
6. The most relevant text is supplied to the LLM
7. The answer is returned through the Flask interface

## Safety Notes

This project is intended for educational and informational use only.

- It is not a substitute for professional medical advice
- It does not diagnose diseases or prescribe treatment
- It includes emergency detection for high-risk medical situations
- Every health-related answer should be reviewed cautiously

## Example Questions

- What are common symptoms of the flu?
- What should I know about ibuprofen?
- How can I improve sleep quality?
- What are the signs of dehydration?

## Troubleshooting

### Module not found errors

Run:

```bash
pip install -r requirements.txt
```

### Pinecone index issues

Check:

- Your API key is valid
- The index name exists or can be created
- The index region is supported
- The embedding dimension matches the model

### Empty or poor answers

Check:

- PDF files exist in `Data/`
- The PDF files are readable
- The documents were indexed successfully
- The model and retrieval settings are correct

## License

This project is intended for educational and experimental use. Please ensure compliance with the licensing terms of the LLM, embedding models, and third-party services used.

## Future Improvements

- Add user authentication
- Improve UI with chat history and streaming responses
- Add support for more medical document types
- Add better validation and logging
- Improve the safety layer and medical disclaimers

## Maintainer

This project was created for medical AI experimentation and educational demonstration purpose 

#### **ADITHYA UBALE**
