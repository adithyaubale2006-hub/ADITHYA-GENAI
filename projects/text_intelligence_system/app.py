import streamlit as st
from datetime import datetime
from pipeline import process_text

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Text Intelligence AI",
    page_icon=":material/psychology:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# CUSTOM CSS — professional, modern, subtle animations
# ----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ---------- Global (dark theme, consistent regardless of system settings) ---------- */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .stApp {
        background: radial-gradient(circle at 20% 0%, #191933 0%, #0e0e18 55%);
    }
    #MainMenu, footer, header {visibility: hidden;}

    h1, h2, h3, h4, p, label, span, div {
        color: #e8e8f0;
        font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* ---------- Hero header ---------- */
    .hero {
        padding: 2.2rem 2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #5b3df0 0%, #8f6fff 45%, #b18bff 100%);
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 34px rgba(106, 92, 255, 0.35);
    }
    .hero h1 {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0 0 0.4rem 0;
        color: #ffffff !important;
    }
    .hero p {
        font-size: 1.02rem;
        opacity: 0.92;
        margin: 0;
        color: #f1eeff !important;
    }

    /* ---------- Cards ---------- */
    .card {
        background: #161625;
        border-radius: 16px;
        padding: 1.6rem 1.8rem;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 1.2rem;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .card:hover {
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.5);
        border-color: rgba(143, 111, 255, 0.35);
    }
    .card h3 {
        margin-top: 0;
        font-size: 1.15rem;
        font-weight: 700;
        color: #f1f1f8 !important;
    }
    .card p, .card div { color: #c7c7db; }

    /* ---------- Sentiment badge ---------- */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.02em;
    }
    .badge-positive { background: rgba(46, 204, 113, 0.15); color: #4fd888 !important; }
    .badge-negative { background: rgba(231, 76, 60, 0.15); color: #ff6b5e !important; }
    .badge-neutral  { background: rgba(150, 150, 180, 0.15); color: #b3b3c9 !important; }

    /* ---------- Category chip ---------- */
    .chip {
        display: inline-block;
        background: rgba(143, 111, 255, 0.15);
        color: #b39dff !important;
        padding: 0.3rem 0.85rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.92rem;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        background: linear-gradient(135deg, #5b3df0, #8f6fff);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.6rem;
        font-weight: 700;
        font-size: 1rem;
        transition: transform 0.12s ease, box-shadow 0.12s ease;
        box-shadow: 0 4px 14px rgba(106, 92, 255, 0.35);
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 22px rgba(106, 92, 255, 0.5);
    }
    .stButton > button p { color: white !important; }

    .stDownloadButton > button {
        background: #1e1e30;
        color: #e8e8f0 !important;
        border: 1px solid rgba(143, 111, 255, 0.4);
        border-radius: 10px;
        font-weight: 600;
    }
    .stDownloadButton > button:hover {
        border-color: #8f6fff;
        background: #24243a;
    }

    /* ---------- Text area ---------- */
    .stTextArea textarea {
        border-radius: 12px;
        border: 1.5px solid #2a2a40;
        background: #14141f;
        color: #e8e8f0;
        font-size: 0.98rem;
    }
    .stTextArea textarea:focus {
        border-color: #8f6fff;
        box-shadow: 0 0 0 3px rgba(143, 111, 255, 0.2);
    }
    .stTextArea textarea::placeholder { color: #6a6a80; }

    /* ---------- Stats card ---------- */
    .stats-card {
        background: #161625;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1rem 1.2rem;
    }
    .stats-label { font-size: 0.8rem; color: #8a8aa8; font-weight: 700; letter-spacing: 0.04em; }
    .stats-value { font-size: 1.5rem; font-weight: 800; color: #f1f1f8; margin-top: 0.15rem; }
    .stats-unit { font-size: 0.8rem; color: #8a8aa8; margin-bottom: 0.5rem; }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: #12121e;
        border-right: 1px solid #23233a;
    }
    section[data-testid="stSidebar"] * { color: #d6d6e6 !important; }
    section[data-testid="stSidebar"] .stCaption, section[data-testid="stSidebar"] small {
        color: #7f7f98 !important;
    }

    /* Toggle accent */
    div[data-baseweb="checkbox"] div[aria-checked="true"] {
        background-color: #8f6fff !important;
        border-color: #8f6fff !important;
    }

    /* ---------- Progress bar ---------- */
    .stProgress > div > div > div { background: linear-gradient(90deg, #5b3df0, #8f6fff) !important; }

    /* ---------- Footer note ---------- */
    .footnote {
        text-align: center;
        color: #6a6a80;
        font-size: 0.85rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Settings")
    show_confidence_bar = st.toggle("Show confidence bar", value=True)
    show_word_count = st.toggle("Show text stats", value=True)
    st.markdown("---")
    st.markdown("### History")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"{item['time']} · {item['sentiment'].capitalize()}"):
                st.caption(item["preview"])
        if st.button("Clear history", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.caption("No analyses yet. Run one to see it here.")
    st.markdown("---")
    st.caption("Built with Streamlit · Text Intelligence AI")

# ----------------------------------------------------------------------------
# HERO HEADER
# ----------------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>Text Intelligence AI</h1>
    <p>Analyze sentiment, generate summaries, and classify text — all in one place.</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# INPUT AREA
# ----------------------------------------------------------------------------
input_col, stats_col = st.columns([3, 1]) if show_word_count else (st.container(), None)

with input_col if show_word_count else st.container():
    user_text = st.text_area(
        "Enter your text here",
        height=200,
        placeholder="Paste an article, review, email, or any text you'd like analyzed...",
        label_visibility="collapsed",
    )

if show_word_count and stats_col is not None:
    with stats_col:
        words = len(user_text.split())
        chars = len(user_text)
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-label">TEXT STATS</div>
            <div class="stats-value">{words}</div>
            <div class="stats-unit">words</div>
            <div class="stats-value">{chars}</div>
            <div class="stats-unit">characters</div>
        </div>
        """, unsafe_allow_html=True)

analyze_col, _ = st.columns([1, 4])
with analyze_col:
    run_analysis = st.button("Analyze Text", use_container_width=True)

# ----------------------------------------------------------------------------
# ANALYSIS
# ----------------------------------------------------------------------------
if run_analysis:
    if user_text.strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing text... this might take a moment!"):
            results = process_text(user_text)

        # Save to history
        st.session_state.history.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "sentiment": results.get("sentiment", "unknown"),
            "preview": user_text[:80] + ("..." if len(user_text) > 80 else ""),
        })

        st.divider()
        st.markdown("## Results")

        sentiment = str(results.get("sentiment", "neutral")).lower()
        badge_class = {
            "positive": "badge-positive",
            "negative": "badge-negative",
        }.get(sentiment, "badge-neutral")

        col1, col2, col3 = st.columns(3)

        # ---- Sentiment card ----
        with col1:
            st.markdown(f"""
            <div class="card">
                <h3>Sentiment</h3>
                <span class="badge {badge_class}">{sentiment.capitalize()}</span>
            </div>
            """, unsafe_allow_html=True)

        # ---- Classification card ----
        with col2:
            category = results.get("classification", "N/A")
            confidence = results.get("confidence", None)
            conf_display = f"{float(confidence)*100:.1f}%" if isinstance(confidence, (int, float)) and confidence <= 1 else f"{confidence}"
            st.markdown(f"""
            <div class="card">
                <h3>Classification</h3>
                <span class="chip">{category}</span>
                <div style="margin-top:0.6rem;color:#6b6b80;font-size:0.9rem;">
                    Confidence: <strong>{conf_display}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if show_confidence_bar and isinstance(confidence, (int, float)):
                st.progress(min(max(float(confidence), 0.0), 1.0) if confidence <= 1 else min(confidence / 100, 1.0))

        # ---- Quick stats card ----
        with col3:
            st.markdown(f"""
            <div class="card">
                <h3>Overview</h3>
                <div style="color:#6b6b80;font-size:0.9rem;">
                    Analyzed at <strong>{datetime.now().strftime('%H:%M:%S')}</strong><br>
                    Input length: <strong>{len(user_text.split())} words</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ---- Summary card (full width) ----
        st.markdown(f"""
        <div class="card">
            <h3>Summary</h3>
            <p style="color:#c7c7db; line-height:1.6;">{results.get('summary', 'No summary available.')}</p>
        </div>
        """, unsafe_allow_html=True)

        # ---- Download results ----
        report = (
            f"TEXT INTELLIGENCE AI — REPORT\n"
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Sentiment: {sentiment.capitalize()}\n"
            f"Classification: {category}\n"
            f"Confidence: {conf_display}\n\n"
            f"Summary:\n{results.get('summary', '')}\n\n"
            f"Original Text:\n{user_text}\n"
        )
        st.download_button(
            "Download Report",
            data=report,
            file_name=f"text_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
        )

st.markdown('<div class="footnote">Text Intelligence AI · Sentiment · Summarization · Classification</div>', unsafe_allow_html=True)