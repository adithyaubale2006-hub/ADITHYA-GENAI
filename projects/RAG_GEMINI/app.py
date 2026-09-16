import os

import streamlit as st
from dotenv import load_dotenv
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

DEFAULT_PDF_PATH = "Open_ai.pdf"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVAL_K = 5


@st.cache_resource
def get_rag_components(pdf_path: str = DEFAULT_PDF_PATH):
    """Build the vector DB, retriever, and RAG chain once per session."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db",
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": RETRIEVAL_K},
    )

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add it to your .env file or environment variables.")

    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
        api_key=api_key,
        temperature=0.3,
        max_output_tokens=200,
    )

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, say that you don't know. "
        "Use three sentences maximum and keep the answer concise.\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    return rag_chain, retriever


st.set_page_config(page_title="RAG with Gemini", page_icon="📘", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@500;600;700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap');

    :root {
        /* ── Color: cool paper + slate ink + a restrained pine accent,
           deliberately distinct from a warm-cream/terracotta default ── */
        --ink: #16202B;
        --muted: #56636D;
        --muted-soft: #7B8790;
        --paper: #EEF1F3;
        --paper-deep: #E2E7EA;
        --paper-line: #D2D9DD;
        --highlight: #FDE9A8;
        --highlight-line: #EBCF7C;
        --highlight-ink: #6B5410;
        --accent: #2F6F63;
        --accent-deep: #234F46;
        --accent-ink: #EAF3F0;
        --success: #2F7D52;
        --warning: #8A6712;
        --error: #A6392A;

        /* ── Spacing: 4px base scale ── */
        --sp-1: 4px;  --sp-2: 8px;  --sp-3: 12px; --sp-4: 16px;
        --sp-5: 24px; --sp-6: 32px; --sp-7: 48px; --sp-8: 64px;

        /* ── Type scale ── */
        --text-xs: 0.75rem;   --text-sm: 0.875rem;  --text-base: 1rem;
        --text-md: 1.125rem;  --text-lg: 1.375rem;  --text-xl: 1.75rem;
        --text-hero: clamp(2.25rem, 4.5vw, 3.6rem);

        --radius-sm: 6px; --radius-md: 10px; --radius-lg: 16px;
        --ease: cubic-bezier(0.2, 0.7, 0.3, 1);
    }

    html, body, .stApp {
        background: var(--paper);
        color: var(--ink);
        font-family: 'Inter', -apple-system, sans-serif;
        font-size: var(--text-base);
    }
    h1, h2, h3 { font-family: 'Lora', serif; letter-spacing: -0.01em; color: var(--ink); }
    :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: var(--radius-sm); }
    .block-container { padding-top: var(--sp-6); max-width: 1040px; }

    /* ── Sidebar ── */
    [data-testid='stSidebar'] {
        background: var(--paper-deep);
        border-right: 1px solid var(--paper-line);
    }
    [data-testid='stSidebar'] .block-container { padding-top: var(--sp-6); }
    .sidebar-logo { display: flex; align-items: center; gap: var(--sp-3); margin-bottom: var(--sp-4); }
    .sidebar-logo span { font-family: 'Lora', serif; font-weight: 600; font-size: var(--text-lg); }
    [data-testid='stSidebar'] label { color: var(--muted); font-size: var(--text-sm) !important; font-weight: 500; }
    [data-testid='stSidebar'] hr { border-color: var(--paper-line); margin: var(--sp-5) 0; }
    [data-testid='stSidebar'] [data-testid='stTextInput'] input {
        background: #fff !important; border: 1.5px solid var(--paper-line) !important;
        border-radius: var(--radius-sm) !important; font-family: 'IBM Plex Mono', monospace !important;
        font-size: var(--text-sm) !important; color: var(--ink) !important;
    }
    [data-testid='stSidebar'] [data-testid='stTextInput'] input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(47, 111, 99, 0.15) !important;
    }
    .pipeline-label {
        font-size: var(--text-xs); text-transform: uppercase; letter-spacing: 0.08em;
        color: var(--muted-soft); margin: var(--sp-2) 0 var(--sp-3); font-weight: 600;
    }
    .pipeline-row {
        display: flex; justify-content: space-between; align-items: center;
        font-family: 'IBM Plex Mono', monospace; font-size: var(--text-xs);
        color: var(--muted); padding: var(--sp-2) 0; border-bottom: 1px solid var(--paper-line);
    }
    .pipeline-row:last-child { border-bottom: none; }
    .pipeline-row strong { color: var(--ink); font-weight: 500; }

    /* ── Masthead ── */
    .masthead { padding: var(--sp-6) 0 var(--sp-6); border-bottom: 1px solid var(--paper-line); margin-bottom: var(--sp-6); }
    .kicker {
        display: inline-flex; align-items: center; gap: var(--sp-2);
        color: var(--accent-deep); font-size: var(--text-xs); font-weight: 600;
        letter-spacing: 0.1em; text-transform: uppercase;
    }
    .masthead h1 { font-size: var(--text-hero); line-height: 1.05; max-width: 18ch; margin: var(--sp-3) 0 var(--sp-4); }
    .masthead p { color: var(--muted); font-size: var(--text-md); max-width: 58ch; line-height: 1.55; }

    /* ── Ask section ── */
    .ask-label {
        display: flex; align-items: center; gap: var(--sp-2);
        font-family: 'Lora', serif; font-weight: 600;
        font-size: var(--text-lg); margin: 0 0 var(--sp-3);
    }
    [data-testid='stTextArea'] textarea {
        background: #fff !important; border: 1.5px solid var(--paper-line) !important;
        border-radius: var(--radius-md) !important; padding: var(--sp-4) !important;
        font-size: var(--text-md) !important; color: var(--ink) !important;
        font-family: 'Inter', sans-serif !important;
        transition: border-color 0.15s var(--ease), box-shadow 0.15s var(--ease);
    }
    [data-testid='stTextArea'] textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(47, 111, 99, 0.15) !important;
    }

    .stButton > button {
        background: var(--accent) !important; color: var(--accent-ink) !important;
        border: none !important; border-radius: var(--radius-md) !important;
        font-weight: 600 !important; padding: var(--sp-3) var(--sp-6) !important;
        font-size: var(--text-base) !important;
        transition: background 0.15s var(--ease), transform 0.1s var(--ease) !important;
        margin-top: var(--sp-3);
    }
    .stButton > button:hover { background: var(--accent-deep) !important; }
    .stButton > button:active { transform: translateY(1px); }

    /* ── Answer card: styled like a highlighted passage ── */
    .answer {
        background: var(--highlight); border: 1px solid var(--highlight-line);
        border-radius: var(--radius-lg); padding: var(--sp-6);
        margin: var(--sp-6) 0 var(--sp-4); animation: rise 0.35s var(--ease);
    }
    @keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
    .answer-label {
        display: flex; align-items: center; gap: var(--sp-2);
        color: var(--highlight-ink); font-size: var(--text-xs); font-weight: 700;
        letter-spacing: 0.08em; text-transform: uppercase;
    }
    .answer p { font-size: var(--text-lg); line-height: 1.55; margin: var(--sp-3) 0 0; color: var(--ink); font-family: 'Lora', serif; }
    .answer-meta { margin-top: var(--sp-4); font-size: var(--text-xs); color: var(--highlight-ink); opacity: 0.85; font-family: 'IBM Plex Mono', monospace; }

    /* ── Passage cards ── */
    .passage-card {
        background: #fff; border: 1px solid var(--paper-line); border-radius: var(--radius-md);
        padding: var(--sp-4) var(--sp-5); margin-bottom: var(--sp-3);
    }
    .passage-head {
        display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--sp-3);
    }
    .passage-number { font-family: 'Lora', serif; font-weight: 600; font-size: var(--text-base); color: var(--ink); }
    .passage-page {
        font-family: 'IBM Plex Mono', monospace; font-size: var(--text-xs); color: var(--accent-deep);
        background: var(--accent-ink); padding: var(--sp-1) var(--sp-3); border-radius: 999px;
        border: 1px solid var(--highlight-line);
    }
    .passage-card p { font-size: var(--text-sm); color: var(--muted); line-height: 1.65; margin: 0; }

    /* ── Native widget restyles ── */
    [data-testid='stExpander'] {
        border: 1px solid var(--paper-line) !important; border-radius: var(--radius-md) !important;
        background: var(--paper-deep); overflow: hidden; margin-top: var(--sp-2);
    }
    [data-testid='stExpander'] summary { font-weight: 600; padding: var(--sp-3) var(--sp-4) !important; }
    [data-testid='stExpander'] summary:hover { background: var(--paper); }
    [data-testid='stAlert'] { border-radius: var(--radius-md); border-width: 1px; border-style: solid; font-size: var(--text-sm); }
    [data-testid='stSpinner'] { color: var(--muted); font-size: var(--text-sm); }
    [data-testid='stSpinner'] > div > div { border-top-color: var(--accent) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-logo">
            <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
                <rect x="6" y="4" width="20" height="24" rx="2" fill="#fff" stroke="#16202B" stroke-width="1.6"/>
                <path d="M10 11h12M10 15h12M10 19h8" stroke="#2F6F63" stroke-width="1.6" stroke-linecap="round"/>
            </svg>
            <span>RAG Reader</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    pdf_path = st.text_input("Document path", value=DEFAULT_PDF_PATH)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="pipeline-label">Retrieval pipeline</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="pipeline-row"><span>Embeddings</span><strong>{EMBEDDING_MODEL}</strong></div>
        <div class="pipeline-row"><span>Chunk size</span><strong>{CHUNK_SIZE} / {CHUNK_OVERLAP} overlap</strong></div>
        <div class="pipeline-row"><span>Retrieved per query</span><strong>k={RETRIEVAL_K}</strong></div>
        <div class="pipeline-row"><span>Model</span><strong>{os.getenv("GEMINI_MODEL", "gemini-2.0-flash")}</strong></div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="masthead">
        <div class="kicker">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>
            PDF question answering
        </div>
        <h1>Ask your document anything.</h1>
        <p>This reads the PDF in the sidebar, retrieves the most relevant passages, and asks Gemini to answer strictly from what it finds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="ask-label">Your question</div>', unsafe_allow_html=True)
question = st.text_area(
    "Your question",
    height=120,
    placeholder="Ask something about the document...",
    label_visibility="collapsed",
)

if st.button("Ask question"):
    if not question.strip():
        st.warning("Please enter a question before submitting.")
    else:
        try:
            rag_chain, retriever = get_rag_components(pdf_path)
            with st.spinner("Reading the document and drafting an answer..."):
                response = rag_chain.invoke({"input": question})
            answer = response.get("answer", "No answer was generated.")
            retrieved_docs = retriever.invoke(question)

            st.markdown(
                f"""
                <div class="answer">
                    <div class="answer-label">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
                        Answer
                    </div>
                    <p>{answer}</p>
                    <div class="answer-meta">Grounded in {len(retrieved_docs)} retrieved passage{'s' if len(retrieved_docs) != 1 else ''} from {pdf_path}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("Relevant retrieved passages"):
                for i, doc in enumerate(retrieved_docs, start=1):
                    page = getattr(doc, "metadata", {}).get("page", "N/A")
                    st.markdown(
                        f"""
                        <div class="passage-card">
                            <div class="passage-head">
                                <span class="passage-number">Passage {i}</span>
                                <span class="passage-page">Page {page}</span>
                            </div>
                            <p>{doc.page_content[:1200]}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        except FileNotFoundError as exc:
            st.error(str(exc))
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Something went wrong while generating the answer: {exc}")