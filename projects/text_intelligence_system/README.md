# Text Intelligence System

A Streamlit application for sentiment analysis, summarization, and zero-shot text classification.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the app

```powershell
streamlit run app/app.py
```

The first analysis downloads the selected model from Hugging Face and caches it locally.

## Project layout

- `app/`: Streamlit UI, model implementations, and preprocessing utilities
- `data/sample_texts/`: sample input text
- `tests/`: automated tests
