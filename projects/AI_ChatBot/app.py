import streamlit as st
import base64
import uuid
from chat_bot import chat_with_gemini, create_chat, generate_title

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Aster AI Chatbot",
    page_icon="\u2726",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Logo -- a minimal geometric spark mark, inline SVG
# ---------------------------------------------------------
def spark_logo(size=40, css_class=""):
    return f'''<svg class="{css_class}" width="{size}" height="{size}" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="sparkGrad" x1="4" y1="4" x2="44" y2="44" gradientUnits="userSpaceOnUse">
<stop offset="0%" stop-color="#818CF8"/>
<stop offset="50%" stop-color="#C084FC"/>
<stop offset="100%" stop-color="#F472B6"/>
</linearGradient>
</defs>
<path d="M24 4 L28 20 L44 24 L28 28 L24 44 L20 28 L4 24 L20 20 Z" fill="url(#sparkGrad)"/>
</svg>'''

def _svg_to_data_uri(svg: str) -> str:
    encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"

# Avatars used by st.chat_message (needs an image source, not raw markup)
ASSISTANT_AVATAR = _svg_to_data_uri(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
    '<defs>'
    '<linearGradient id="avatarGrad" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">'
    '<stop offset="0%" stop-color="#818CF8"/>'
    '<stop offset="50%" stop-color="#C084FC"/>'
    '<stop offset="100%" stop-color="#F472B6"/>'
    '</linearGradient>'
    '</defs>'
    '<rect width="48" height="48" rx="12" fill="#18181b"/>'
    '<path d="M24 8 L27 21 L40 24 L27 27 L24 40 L21 27 L8 24 L21 21 Z" fill="url(#avatarGrad)"/>'
    '</svg>'
)
USER_AVATAR = _svg_to_data_uri(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
    '<rect width="48" height="48" rx="12" fill="#27272a"/>'
    '<circle cx="24" cy="18" r="8" fill="#a1a1aa"/>'
    '<path d="M8 40c0-8.837 7.163-14 16-14s16 5.163 16 14" fill="#a1a1aa"/>'
    '</svg>'
)

# ---------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    :root {
        --grad-1: #818CF8;
        --grad-2: #C084FC;
        --grad-3: #F472B6;
        --grad-full: linear-gradient(135deg, var(--grad-1), var(--grad-2), var(--grad-3));
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Ambient background glow -- subtle, premium, not distracting */
    .stApp {
        background:
            radial-gradient(circle at 15% 0%, rgba(129,140,248,0.10), transparent 45%),
            radial-gradient(circle at 85% 15%, rgba(244,114,182,0.08), transparent 40%),
            radial-gradient(circle at 50% 100%, rgba(192,132,252,0.06), transparent 50%),
            #0a0a0d;
    }

    /* Gradient title text */
    .brand-title {
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -0.02em;
        background: var(--grad-full);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .brand-subtitle {
        color: #9a9aa5;
        font-size: 0.92rem;
        text-align: center;
        margin-top: 4px;
        margin-bottom: 1.6rem;
    }

    .logo-hero {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
    .logo-hero svg {
        filter: drop-shadow(0 0 18px rgba(192,132,252,0.35));
    }

    .sidebar-logo {
        margin-bottom: 4px;
    }
    .sidebar-logo svg {
        filter: drop-shadow(0 0 8px rgba(192,132,252,0.3));
    }

    /* Sidebar background -- faint gradient tint */
    div[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(129,140,248,0.05), rgba(244,114,182,0.02) 60%, transparent),
            #0d0d11;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    /* Sidebar buttons -- base, force override of Streamlit's default theme */
    div[data-testid="stSidebar"] button {
        border-radius: 10px !important;
        transition: all 0.18s ease !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }

    /* "New Chat" -- the first button widget in the sidebar.
       Ghost/outline style: clearly a CTA, but not competing visually
       with the active-session highlight below it. */
    div[data-testid="stSidebar"] div[data-testid="stButton"]:nth-of-type(1) button {
        background: rgba(192,132,252,0.08) !important;
        border: 1px solid rgba(192,132,252,0.4) !important;
        color: #f1f1f4 !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"]:nth-of-type(1) button:hover {
        background: rgba(192,132,252,0.16) !important;
        border-color: rgba(192,132,252,0.7) !important;
        color: #ffffff !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"]:nth-of-type(1) button p {
        color: inherit !important;
    }

    /* Active session -- soft tinted highlight, not a loud filled gradient.
       Multiple selector variants covering different Streamlit DOM versions. */
    div[data-testid="stSidebar"] button[kind="primary"],
    div[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"],
    div[data-testid="stSidebar"] button[data-testid="baseButton-primary"] {
        background: rgba(192,132,252,0.16) !important;
        color: #f8f8fa !important;
        font-weight: 600 !important;
        border: 1px solid rgba(192,132,252,0.45) !important;
        border-left: 3px solid #C084FC !important;
        box-shadow: none !important;
    }
    div[data-testid="stSidebar"] button[kind="primary"]:hover,
    div[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"]:hover,
    div[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover {
        background: rgba(192,132,252,0.24) !important;
    }
    div[data-testid="stSidebar"] button[kind="primary"] p,
    div[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] p,
    div[data-testid="stSidebar"] button[data-testid="baseButton-primary"] p {
        color: inherit !important;
    }

    /* Inactive session buttons -- same coverage for secondary variants */
    div[data-testid="stSidebar"] button[kind="secondary"],
    div[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"],
    div[data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
        background: transparent !important;
        color: #a1a1aa !important;
        border: 1px solid transparent !important;
        box-shadow: none !important;
    }
    div[data-testid="stSidebar"] button[kind="secondary"]:hover,
    div[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover,
    div[data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover {
        background: rgba(255,255,255,0.06) !important;
        color: #e4e4e7 !important;
    }
    div[data-testid="stSidebar"] button[kind="secondary"] p,
    div[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] p,
    div[data-testid="stSidebar"] button[data-testid="baseButton-secondary"] p {
        color: inherit !important;
    }

    /* Chat message entrance -- plain fade, no bounce */
    .stChatMessage {
        animation: fadeIn 0.25s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }

    /* Alternating message tint: user (odd) vs assistant (even) --
       chat messages strictly alternate in this app */
    div[data-testid="stChatMessage"]:nth-of-type(odd) {
        background: linear-gradient(135deg, rgba(129,140,248,0.10), rgba(244,114,182,0.05));
        border: 1px solid rgba(192,132,252,0.15);
        border-radius: 14px;
    }
    div[data-testid="stChatMessage"]:nth-of-type(even) {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
    }

    /* Thinking indicator -- logo gently breathes with a gradient glow */
    .thinking-row {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 4px 0 2px 0;
    }
    .thinking-logo {
        animation: breathe 1.6s ease-in-out infinite;
    }
    .thinking-logo svg {
        filter: drop-shadow(0 0 6px rgba(192,132,252,0.5));
    }
    @keyframes breathe {
        0%, 100% { opacity: 0.5; transform: scale(0.92); }
        50%      { opacity: 1;   transform: scale(1.08); }
    }
    .thinking-label {
        color: #9a9aa5;
        font-size: 0.9rem;
    }

    /* Chat input -- gradient focus ring, premium feel */
    div[data-testid="stChatInput"] {
        border-color: rgba(255,255,255,0.12) !important;
        border-radius: 14px !important;
        box-shadow: none !important;
        background: rgba(255,255,255,0.02) !important;
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: rgba(192,132,252,0.5) !important;
        box-shadow: 0 0 0 3px rgba(192,132,252,0.15) !important;
    }
    div[data-testid="stChatInput"] textarea {
        border-color: transparent !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State -- multiple chat sessions, ChatGPT-style
# ---------------------------------------------------------
def _new_session():
    """Create a brand new chat session and make it active."""
    session_id = str(uuid.uuid4())
    st.session_state.sessions[session_id] = {
        "title": "New chat",
        "messages": [],
        "chat": create_chat(),
        "titled": False,
    }
    st.session_state.session_order.insert(0, session_id)
    st.session_state.active_session = session_id

if "sessions" not in st.session_state:
    st.session_state.sessions = {}
    st.session_state.session_order = []
    _new_session()

active_id = st.session_state.active_session
active_session = st.session_state.sessions[active_id]

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(f'<div class="sidebar-logo">{spark_logo(32)}</div>', unsafe_allow_html=True)
    st.markdown("### Aster AI")
    st.caption("Your intelligent assistant")

    st.divider()

    if st.button("+ New Chat", use_container_width=True):
        _new_session()
        st.rerun()

    st.divider()
    st.caption("RECENT CHATS")

    for session_id in st.session_state.session_order:
        session = st.session_state.sessions[session_id]
        is_active = session_id == active_id

        # Don't list the chat you're already on if it has no messages yet --
        # it's redundant with the "New Chat" button above and would show
        # as a second, identical "New chat" entry.
        if is_active and not session["messages"]:
            continue

        label = session["title"] if session["title"] else "New chat"
        if st.button(
            label,
            key=f"session_btn_{session_id}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.active_session = session_id
            st.rerun()

    st.divider()
    st.caption("Session-based \u00b7 no data stored")

# ---------------------------------------------------------
# Header -- only show the hero/branding on an empty (new) chat
# ---------------------------------------------------------
if not active_session["messages"]:
    st.markdown(f'<div class="logo-hero">{spark_logo(56)}</div>', unsafe_allow_html=True)
    st.markdown('<p class="brand-title">Aster AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">Ask anything, get instant answers</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Chat History (active session only)
# ---------------------------------------------------------
for message in active_session["messages"]:
    avatar = ASSISTANT_AVATAR if message["role"] == "assistant" else USER_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------------------------------------------------
# Chat Input
# ---------------------------------------------------------
user_message = st.chat_input("Type your message...")

if user_message:
    active_session["messages"].append({"role": "user", "content": user_message})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(user_message)

    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        placeholder = st.empty()
        thinking_html = (
            '<div class="thinking-row">'
            f'<div class="thinking-logo">{spark_logo(20)}</div>'
            '<div class="thinking-label">Generating response...</div>'
            '</div>'
        )
        placeholder.markdown(thinking_html, unsafe_allow_html=True)
        try:
            response = chat_with_gemini(active_session["chat"], user_message)
        except Exception as e:
            response = f"Sorry, something went wrong while getting a response.\n\n*Details: {e}*"
        placeholder.markdown(response)

    active_session["messages"].append({"role": "assistant", "content": response})

    # Auto-generate the session title from the first exchange, like GPT
    if not active_session["titled"]:
        active_session["title"] = generate_title(user_message)
        active_session["titled"] = True
        st.rerun()