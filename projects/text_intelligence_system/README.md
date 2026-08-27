# Text Intelligence System

A Streamlit application for sentiment analysis, text summarization, and zero-shot text classification using pretrained Transformer models from Hugging Face.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the Application

```powershell
streamlit run app/app.py
```

The first analysis downloads the selected models from Hugging Face and caches them locally.

## Features

### Sentiment Analysis

Predicts whether the input text is Positive or Negative and provides a confidence score.

### Text Summarization

Converts longer text into a shorter, meaningful summary using a pretrained Transformer model.

### Zero-Shot Text Classification

Classifies text into user-defined categories without requiring task-specific training data.

## Architecture

```text
                         User Text
                            |
                            v
                     Streamlit UI
                            |
                            v
                       AI Pipeline
                            |
            +---------------+---------------+
            |               |               |
            v               v               v
       Sentiment      Summarization    Classification
            |               |               |
            +---------------+---------------+
                            |
                            v
                      Final Results
```

## Technologies

* Python
* Hugging Face Transformers
* PyTorch
* Streamlit

## Project Structure

```text
text_intelligence_system/
|
+-- app/
|   +-- app.py
|   +-- pipeline.py
|   |
|   +-- models/
|       +-- sentiment.py
|       +-- summarizer.py
|       +-- classifier.py
|
+-- requirements.txt
+-- README.md
+-- .gitignore
```

## How It Works

```text
Input Text
    |
    v
Tokenization
    |
    v
Pretrained Transformer Model
    |
    +-------------------+
    |                   |
    v                   v
Task Prediction     Generated Output
    |                   |
    +---------+---------+
              |
              v
        Streamlit UI
```

## Learning Objectives

This project demonstrates:

* Working with pretrained Transformer models
* Using Hugging Face Tokenizers
* Sentiment analysis
* Text summarization
* Zero-shot text classification
* Model inference
* Building a modular AI pipeline
* Creating an NLP application with Streamlit

## Project Status

Completed as Project 1 of my GenAI portfolio.

## Author

Adithya Ubale
