# Standard library imports
import os
from pathlib import Path

# Third-party imports
import streamlit as st
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ui import render

load_dotenv()

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVAL_K = 5

SYSTEM_PROMPT = """
You are an AI Financial Research Assistant specializing in stock and company analysis.

Answer the user's question using ONLY the information provided in the context.

Rules:
- Do not invent financial figures, facts, dates, or company information.
- If the context does not contain enough information, say:
  "The available documents do not contain enough information to answer this question."
- Preserve the original units such as USD, million, billion, and percentage.
- Clearly distinguish reported figures from calculated figures.
- When comparing financial periods, mention the relevant years or quarters.
- Explain financial terms briefly when useful.
- Do not provide personalized investment advice.
- Do not guarantee future stock performance or returns.

Provide your answer in this format:

Answer:
Give a concise answer to the user's question.

Key Financial Metrics:
Mention the relevant financial metrics and figures.

Analysis:
Explain the important trends or relationships found in the context.

Risks / Considerations:
Mention relevant risks or uncertainties found in the documents.

Source:
Mention the relevant document or page information when available.

-------------------------
Context:
{context}
-------------------------
"""


@st.cache_resource
def build_retriever():
    project_root = Path(__file__).resolve().parent
    article_path = project_root / "articles"

    pdf_files = sorted(article_path.rglob("*.pdf"))
    documents = []
    for pdf_file in pdf_files:
        loader = PyPDFLoader(str(pdf_file))
        documents.extend(loader.load())

    if not documents:
        raise ValueError(
            "No PDF documents were found in the 'articles' folder. "
            "Add company annual reports or filings before running the app."
        )

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(documents)

    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name="financial_documents",
    )

    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": RETRIEVAL_K})
    stats = {"filings": len(pdf_files), "chunks": len(chunks)}
    return retriever, stats


@st.cache_resource
def build_rag_chain():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add it to your .env file or environment variables.")

    retriever, stats = build_retriever()

    prompt = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("human", "{input}")])

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=api_key,
        temperature=0.4,
        max_output_tokens=1086,
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, question_answer_chain), stats


def render_page(rag_chain, stats):
    with st.sidebar:
        render.render_sidebar_logo()
        st.caption("Grounded Q&A over the filings in your `articles/` folder.")
        st.markdown("<hr>", unsafe_allow_html=True)
        render.render_pipeline_panel(
            [
                ("Embeddings", EMBEDDING_MODEL),
                ("Chunk size", f"{CHUNK_SIZE} / {CHUNK_OVERLAP} overlap"),
                ("Retrieved per query", f"k={RETRIEVAL_K}"),
                ("Filings indexed", str(stats["filings"])),
                ("Passages indexed", str(stats["chunks"])),
            ]
        )
        render.render_disclaimer()

    render.render_masthead(filings=stats["filings"], chunks=stats["chunks"], k=RETRIEVAL_K)

    st.markdown('<div class="ask-label">Your question</div>', unsafe_allow_html=True)
    question = st.text_area(
        "Your question",
        placeholder="Example: What was Apple's revenue in 2025?",
        label_visibility="collapsed",
    )

    if st.button("Analyze") and question:
        with st.spinner("Retrieving relevant documents and answering..."):
            response = rag_chain.invoke({"input": question})

        sections = render.parse_answer_sections(response.get("answer", "No answer returned."))
        render.render_answer_report(sections)

        st.subheader("Relevant sources")
        context_docs = response.get("context", [])
        if not context_docs:
            st.info("No context documents were returned for this query.")
            return

        for idx, doc in enumerate(context_docs, start=1):
            if hasattr(doc, "page_content"):
                text, metadata = doc.page_content, getattr(doc, "metadata", {})
            elif isinstance(doc, dict):
                text = doc.get("page_content") or doc.get("content") or str(doc)
                metadata = doc.get("metadata", {})
            else:
                text, metadata = str(doc), {}

            source_name = Path(metadata.get("source", "unknown")).name if metadata else "unknown"
            page = metadata.get("page", "N/A") if metadata else "N/A"
            render.render_passage_card(idx, source_name, page, text)


def main():
    st.set_page_config(page_title="Financial Stock Analysis", page_icon="📈", layout="wide", initial_sidebar_state="expanded")
    render.inject_css()
    st.title("Financial Stock Analysis Assistant")

    try:
        rag_chain, stats = build_rag_chain()
    except ValueError as exc:
        st.error(str(exc))
        st.stop()
        return

    render_page(rag_chain, stats)


if __name__ == "__main__":
    main()