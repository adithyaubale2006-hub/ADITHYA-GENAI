#  Zomato AI OrderBot

A conversational AI ordering assistant built with **Chainlit**, **LangChain**, and **Google Gemini (1.5 Flash)**. This bot is designed to simulate a professional restaurant ordering experience with strict guardrails, memory, and upselling capabilities.

##  Tech Stack

- **Framework**: [Chainlit](https://docs.chainlit.io/) (for the interactive chat UI)
- **Orchestration**: [LangChain](https://python.langchain.com/) (for prompt templates and conversation memory)
- **LLM**: Google Generative AI (Gemini 1.5 Flash)
- **Language**: Python 3.10+

##  Project Structure

```text
├── app.py                # Main Chainlit application and session state handling
├── src/
│   ├── __init__.py
│   ├── llm.py            # LangChain model initialization and LCEL chain
│   └── prompt.py         # System persona, menu, and strict guardrails
├── .env                  # Environment variables (API Keys - Gitignored)
├── .gitignore            # Git exclusions
└── requirements.txt      # Python dependencies