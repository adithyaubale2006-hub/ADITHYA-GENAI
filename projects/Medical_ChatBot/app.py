import os
import time
from typing import List

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def load_pdf_documents(folder: str = "Data") -> List:
    try:
        from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
        from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
    except Exception as exc:
        raise RuntimeError(
            "The LangChain PDF dependencies are missing. Install the project requirements first."
        ) from exc

    loader = DirectoryLoader(folder, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    if not documents:
        return []

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    return splitter.split_documents(documents)


def get_embeddings():
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except Exception:
        from langchain_community.embeddings import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def build_vector_store(documents):
    try:
        from langchain_pinecone import PineconeVectorStore
        from pinecone import Pinecone, ServerlessSpec
    except Exception as exc:
        raise RuntimeError(
            "Pinecone dependencies are missing. Install the project requirements first."
        ) from exc

    pinecone_api_key = get_required_env("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX", "medibot-384")

    pc = Pinecone(api_key=pinecone_api_key)

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

    return PineconeVectorStore.from_documents(
        documents=documents,
        index_name=index_name,
        embedding=get_embeddings(),
    )


def get_retriever():
    try:
        documents = load_pdf_documents("Data")
        if not documents:
            return None
        return build_vector_store(documents).as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4},
        )
    except RuntimeError:
        return None
    except Exception:
        return None


def get_llm():
    try:
        from langchain_nvidia_ai_endpoints import ChatNVIDIA
    except Exception:
        return None

    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
    if not NVIDIA_API_KEY:
        return None

    return ChatNVIDIA(
        model="openai/gpt-oss-20b",
        api_key=NVIDIA_API_KEY,
        temperature=0.2,
        max_completion_tokens=1086,
        top_p=1,
    )


def build_prompt_template():
    from langchain_classic.prompts import ChatPromptTemplate

    system_prompt = """
# ROLE AND PURPOSE
You are a highly advanced, professional Medical AI Assistant designed to provide evidence-based health information, explain medical terminology, and assist with general health inquiries. Your primary objective is to empower users with accurate medical knowledge while strictly adhering to patient safety and clinical liability boundaries.

# CRITICAL SAFETY & COMPLIANCE GUARDRAILS
1. No Medical Advice or Diagnosis: You are an AI, not a licensed physician. You must NEVER provide a definitive medical diagnosis, prescribe treatments, recommend specific dosages, or instruct a user to ignore professional medical advice.
2. Mandatory Medical Disclaimer: Every response discussing specific conditions, symptoms, or treatments must include a clear, professional disclaimer: *\"Please note: I am an AI, not a doctor. This information is for educational purposes and should not replace professional medical advice. Always consult a qualified healthcare provider for diagnosis and treatment.\"*
3. PII & Confidentiality: Do not ask for or store Personally Identifiable Information (PII) or Protected Health Information (PHI). If a user provides highly sensitive data, focus purely on the medical concepts rather than their personal identity.

# EMERGENCY PROTOCOL (RED FLAGS)
If a user describes symptoms indicative of a life-threatening emergency (e.g., severe chest pain, radiating arm/jaw pain, sudden shortness of breath, facial drooping, severe bleeding, or suicidal ideation):
- STOP normal processing.
- Immediately issue a high-priority warning.
- Direct the user to call their local emergency number (e.g., 911) or proceed to the nearest emergency department immediately.
- Do not attempt to diagnose the emergency.

# RAG & INFORMATION RETRIEVAL INSTRUCTIONS
Your knowledge is strictly limited to the information provided in the retrieved medical context.
- Grounding: Base your answers EXCLUSIVELY on the {context} provided below.
- Zero Hallucination: Do not invent medical facts, statistics, or studies. If the provided context does not contain the answer, you must state: *\"The retrieved medical documents do not contain sufficient information to answer this specific question.\"*
- Source Attribution: Where possible, briefly reference the type of document or medical guideline provided in the context (e.g., \"According to the provided clinical guidelines...\").

# TONE, STYLE, AND FORMATTING
- Tone: Empathetic, objective, reassuring, and strictly professional. Avoid alarmist language.
- Clarity: Translate complex clinical jargon into accessible, patient-friendly language while retaining medical accuracy.
- Structure: Use markdown formatting, bold text for key terms, and bullet points to make complex medical information easy to read and digest.

-------------------------
RETRIEVED MEDICAL CONTEXT:
{context}
-------------------------
"""

    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])


def answer_medical_question(question: str) -> str:
    if not question or not question.strip():
        return "Please enter a medical question first."

    cleaned_question = question.strip()
    lower_question = cleaned_question.lower()

    emergency_terms = [
        "chest pain",
        "shortness of breath",
        "severe bleeding",
        "suicidal",
        "stroke",
        "heart attack",
        "unconscious",
        "difficulty breathing",
        "severe trauma",
    ]

    if any(term in lower_question for term in emergency_terms):
        return (
            "🚨 Emergency: Please call your local emergency number immediately or go to the nearest emergency department right away. "
            "This is not a diagnosis. Please note: I am an AI, not a doctor. This information is for educational purposes and should not replace professional medical advice."
        )

    retriever = get_retriever()
    llm = get_llm()

    if retriever is not None and llm is not None:
        try:
            docs = retriever.invoke(cleaned_question)
            context = "\n\n".join(doc.page_content for doc in docs if getattr(doc, "page_content", None))
            prompt = build_prompt_template().format_messages(context=context, question=cleaned_question)
            reply = llm.invoke(prompt)
            return str(reply.content) if hasattr(reply, "content") else str(reply)
        except Exception:
            pass

    if retriever is not None:
        try:
            docs = retriever.invoke(cleaned_question)
            context = "\n\n".join(doc.page_content for doc in docs if getattr(doc, "page_content", None))
            if context:
                return (
                    "Based on the retrieved documents, the available medical context is limited. "
                    "Please note: I am an AI, not a doctor. This information is for educational purposes and should not replace professional medical advice.\n\n"
                    f"Relevant context:\n{context[:1200]}"
                )
        except Exception:
            pass

    return (
        "The retrieved medical documents do not contain sufficient information to answer this specific question. "
        "Please note: I am an AI, not a doctor. This information is for educational purposes and should not replace professional medical advice. "
        "Always consult a qualified healthcare provider for diagnosis and treatment."
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    answer = answer_medical_question(question)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
