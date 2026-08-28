# ASTER AI

A simple AI chatbot built with Python and Google Gemini API. ASTER AI can understand user messages and generate intelligent, conversational responses using Gemini's generative AI capabilities.

---

## Features

* Interactive AI conversation
* Powered by Google Gemini
* Real-time response generation
* Secure API key management using `.env`
* Built with Python
* Runs locally using VS Code or terminal
* Personalized AI responses

---

## Technologies Used

* Python
* Google Gemini API
* Google GenAI SDK
* python-dotenv
* VS Code
* Git & GitHub

---

## Project Structure

```text
ASTER-AI/
│
├── chatbot.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/ASTER-AI.git
```

### 2. Navigate to the Project

```bash
cd ASTER-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## API Key Setup

Create a `.env` file in the project folder:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your API key to GitHub.

Add the following to `.gitignore`:

```text
.env
venv/
__pycache__/
```

---

## Run ASTER AI

Start the chatbot using:

```bash
python chatbot.py
```

You can then type messages and interact with ASTER AI.

Example:

```text
You: Hello

ASTER AI: Hello Adithya! How can I help you today?

You: Explain artificial intelligence

ASTER AI: Artificial intelligence is...
```

---

## How It Works

```text
             +-----------------+
             |      User       |
             +--------+--------+
                      |
                      v
             +-----------------+
             |   ASTER AI      |
             | Python Chatbot  |
             +--------+--------+
                      |
                      v
             +-----------------+
             |   Gemini API    |
             +--------+--------+
                      |
                      v
             +-----------------+
             | AI Generated    |
             |    Response     |
             +--------+--------+
                      |
                      v
             +-----------------+
             |      User       |
             +-----------------+
```

---

## What I Learned

Through this project, I learned:

* How to work with the Gemini API
* How to use the Google GenAI Python SDK
* How to manage API keys using environment variables
* How to build an AI-powered application
* How to create a conversational AI interface
* How to structure and upload a Python AI project to GitHub

---

## Future Improvements

* Conversation memory
* Web-based UI
* Telegram AI chatbot
* Voice input and output
* PDF and document question answering
* RAG-based knowledge retrieval
* Agentic AI capabilities
* Cloud deployment

---

## Project Goal

ASTER AI is part of my journey toward becoming a Generative AI Engineer.

The project provides a foundation for building more advanced AI applications involving:

```text
LLMs
  |
  v
Prompt Engineering
  |
  v
RAG
  |
  v
AI Agents
  |
  v
Production GenAI Applications
```

---

## Author

**Adithya Ubale**

B.Tech Student | Generative AI Enthusiast

---

## License

This project is created for educational and learning purposes.
