import os

import streamlit as st
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter


SOURCE_URLS = [
	"https://www.victoriaonmove.com.au/local-removalists.html",
	"https://victoriaonmove.com.au/index.html",
	"https://victoriaonmove.com.au/contact.html",
]

load_dotenv()

st.set_page_config(
	page_title="Movewise | Victoria On Move",
	page_icon="📦",
	layout="wide",
	initial_sidebar_state="expanded",
)

st.markdown(
	"""
	<style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

	:root {
		/* ── Color: kraft-paper & route-map, grounded in moving/logistics ── */
		--ink: #16231B;
		--muted: #55624F;
		--muted-soft: #7C8677;
		--paper: #F7F5EF;
		--paper-deep: #ECE7DA;
		--paper-line: #DCD5C2;
		--mint: #DCEFE1;
		--mint-line: #B9DCC2;
		--mint-ink: #1F5C3A;
		--accent: #C15B32;
		--accent-deep: #9C4423;
		--accent-ink: #FBF3EE;
		--route: #35566E;
		--success: #2F7D52;
		--warning: #8A6D1D;
		--error: #A6392A;

		/* ── Spacing: 4px base scale ── */
		--sp-1: 4px;  --sp-2: 8px;  --sp-3: 12px; --sp-4: 16px;
		--sp-5: 24px; --sp-6: 32px; --sp-7: 48px; --sp-8: 64px;

		/* ── Type scale ── */
		--text-xs: 0.75rem;   --text-sm: 0.875rem;  --text-base: 1rem;
		--text-md: 1.125rem;  --text-lg: 1.375rem;  --text-xl: 1.75rem;
		--text-2xl: clamp(2rem, 4vw, 2.75rem);
		--text-hero: clamp(2.5rem, 5.5vw, 4.75rem);

		--radius-sm: 6px; --radius-md: 10px; --radius-lg: 16px;
		--ease: cubic-bezier(0.2, 0.7, 0.3, 1);
	}

	html, body, .stApp {
		background: var(--paper);
		color: var(--ink);
		font-family: 'DM Sans', -apple-system, sans-serif;
		font-size: var(--text-base);
	}
	h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.01em; color: var(--ink); }
	a { color: var(--route); text-decoration: none; border-bottom: 1px solid transparent; transition: border-color 0.15s var(--ease); }
	a:hover { border-bottom-color: var(--route); }
	:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: var(--radius-sm); }

	.block-container { padding-top: var(--sp-6); max-width: 1120px; }

	/* ── Sidebar ── */
	[data-testid='stSidebar'] {
		background: var(--paper-deep);
		border-right: 1px solid var(--paper-line);
	}
	[data-testid='stSidebar'] .block-container { padding-top: var(--sp-6); }
	.sidebar-logo { display: flex; align-items: center; gap: var(--sp-3); margin-bottom: var(--sp-2); }
	.sidebar-logo svg { flex-shrink: 0; }
	.sidebar-logo span { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: var(--text-lg); }
	[data-testid='stSidebar'] .stCaption, [data-testid='stSidebar'] p { color: var(--muted); font-size: var(--text-sm); }
	[data-testid='stSidebar'] h3 { font-size: var(--text-sm); text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin-top: var(--sp-2); }
	[data-testid='stSidebar'] hr { border-color: var(--paper-line); margin: var(--sp-5) 0; }
	.source-link {
		display: flex; align-items: center; gap: var(--sp-2);
		padding: var(--sp-2) var(--sp-3); margin-bottom: var(--sp-1);
		border-radius: var(--radius-sm); background: var(--paper);
		border: 1px solid var(--paper-line); font-size: var(--text-sm);
		transition: border-color 0.15s var(--ease), transform 0.1s var(--ease);
	}
	.source-link:hover { border-color: var(--route); border-bottom-color: transparent; transform: translateX(2px); }
	.model-tag {
		display: inline-flex; align-items: center; gap: var(--sp-2);
		font-size: var(--text-xs); color: var(--muted); font-family: 'DM Sans', monospace;
		background: var(--paper); border: 1px solid var(--paper-line);
		padding: var(--sp-1) var(--sp-3); border-radius: 999px;
	}

	/* ── Hero ── */
	.hero { padding: var(--sp-7) 0 var(--sp-6); border-bottom: 1px solid var(--paper-line); position: relative; }
	.eyebrow {
		display: inline-flex; align-items: center; gap: var(--sp-2);
		color: var(--accent-deep); font-size: var(--text-xs); font-weight: 700;
		letter-spacing: 0.1em; text-transform: uppercase;
	}
	.hero h1 { font-size: var(--text-hero); line-height: 0.98; max-width: 15ch; margin: var(--sp-3) 0 var(--sp-4); }
	.hero p { color: var(--muted); font-size: var(--text-md); max-width: 56ch; line-height: 1.5; }
	.route-line { position: absolute; right: 0; top: var(--sp-6); opacity: 0.9; display: none; }
	@media (min-width: 1000px) { .route-line { display: block; } }

	/* ── Metrics ── */
	.metric-row { display: flex; gap: var(--sp-6); flex-wrap: wrap; margin: var(--sp-6) 0 var(--sp-2); }
	.metric { border-top: 2px solid var(--ink); padding-top: var(--sp-3); min-width: 140px; }
	.metric strong { font-family: 'Space Grotesk', sans-serif; font-size: var(--text-xl); display: block; }
	.metric span { color: var(--muted); display: block; font-size: var(--text-sm); margin-top: var(--sp-1); }

	/* ── Ask section ── */
	.ask-label {
		display: flex; align-items: center; gap: var(--sp-2);
		font-family: 'Space Grotesk', sans-serif; font-weight: 600;
		font-size: var(--text-lg); margin: var(--sp-2) 0 var(--sp-3);
	}
	[data-testid='stTextInput'] input {
		background: #fff; border: 1.5px solid var(--paper-line) !important;
		border-radius: var(--radius-md) !important; padding: var(--sp-4) var(--sp-4) !important;
		font-size: var(--text-md) !important; color: var(--ink);
		transition: border-color 0.15s var(--ease), box-shadow 0.15s var(--ease);
	}
	[data-testid='stTextInput'] input:focus {
		border-color: var(--accent) !important;
		box-shadow: 0 0 0 3px rgba(193, 91, 50, 0.15) !important;
	}
	.ask-hint { color: var(--muted-soft); font-size: var(--text-xs); margin-top: var(--sp-2); }

	/* ── Answer card ── */
	.answer {
		background: var(--mint); border: 1px solid var(--mint-line);
		border-radius: var(--radius-lg); padding: var(--sp-6);
		margin: var(--sp-5) 0; animation: rise 0.35s var(--ease);
	}
	@keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
	.answer-label {
		display: flex; align-items: center; gap: var(--sp-2);
		color: var(--mint-ink); font-size: var(--text-xs); font-weight: 700;
		letter-spacing: 0.08em; text-transform: uppercase;
	}
	.answer p { font-size: var(--text-lg); line-height: 1.5; margin: var(--sp-3) 0 0; color: var(--ink); }
	.answer-meta { margin-top: var(--sp-4); font-size: var(--text-xs); color: var(--mint-ink); opacity: 0.85; }

	/* ── Source cards inside expander ── */
	.source-card {
		background: #fff; border: 1px solid var(--paper-line); border-radius: var(--radius-md);
		padding: var(--sp-4); margin-bottom: var(--sp-3);
	}
	.source-card .source-tag {
		font-family: monospace; font-size: var(--text-xs); color: var(--route);
		background: var(--paper-deep); padding: var(--sp-1) var(--sp-2);
		border-radius: var(--radius-sm); display: inline-block; margin-bottom: var(--sp-2);
		word-break: break-all;
	}
	.source-card p { font-size: var(--text-sm); color: var(--muted); line-height: 1.6; margin: 0; }

	/* ── Native widget restyles ── */
	[data-testid='stExpander'] {
		border: 1px solid var(--paper-line) !important; border-radius: var(--radius-md) !important;
		background: var(--paper); overflow: hidden;
	}
	[data-testid='stExpander'] summary { font-weight: 600; padding: var(--sp-3) var(--sp-4) !important; }
	[data-testid='stExpander'] summary:hover { background: var(--paper-deep); }

	[data-testid='stAlert'] { border-radius: var(--radius-md); border-width: 1px; border-style: solid; }

	[data-testid='stSpinner'] { color: var(--muted); font-size: var(--text-sm); }
	[data-testid='stSpinner'] > div > div { border-top-color: var(--accent) !important; }
	</style>
	""",
	unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def build_rag_chain():
	if not os.getenv("NVIDIA_API_KEY"):
		raise RuntimeError("NVIDIA_API_KEY is missing. Add it to your .env file to enable answers.")

	documents = UnstructuredURLLoader(urls=SOURCE_URLS).load()
	splitter = RecursiveCharacterTextSplitter(
		separators=["\n"], chunk_size=1000, chunk_overlap=0
	)
	chunks = splitter.split_documents(documents)
	embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
	vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings)
	retriever = vector_store.as_retriever(
		search_type="similarity", search_kwargs={"k": 3}
	)
	llm = ChatNVIDIA(
		model="openai/gpt-oss-20b",
		api_key=os.environ["NVIDIA_API_KEY"],
		max_tokens=200,
		temperature=0.2,
		top_p=1,
	)
	prompt = ChatPromptTemplate.from_messages(
		[
			(
				"system",
				"You are an assistant for question-answering tasks. "
				"Use the retrieved context to answer the question. "
				"If you don't know the answer, say that you don't know. "
				"Use three sentences maximum and keep the answer concise.\n\n{context}",
			),
			("human", "{input}"),
		]
	)
	answer_chain = create_stuff_documents_chain(llm, prompt)
	return create_retrieval_chain(retriever, answer_chain), len(chunks)


def main():
	with st.sidebar:
		st.markdown(
			"""
			<div class="sidebar-logo">
				<svg width="30" height="30" viewBox="0 0 32 32" fill="none">
					<rect x="4" y="12" width="24" height="16" rx="2" fill="#C15B32"/>
					<path d="M4 12L16 5l12 7" stroke="#16231B" stroke-width="2" fill="none" stroke-linejoin="round"/>
					<path d="M16 12v16M4 12v16h24V12" stroke="#16231B" stroke-width="1.4" fill="none"/>
				</svg>
				<span>Movewise</span>
			</div>
			""",
			unsafe_allow_html=True,
		)
		st.caption("A source-grounded assistant for Victoria On Move.")
		st.divider()
		st.markdown("### Knowledge base")
		st.caption("Answers are retrieved from the official Victoria On Move website.")
		for url in SOURCE_URLS:
			label = url.split('/')[-1] or 'home'
			st.markdown(
				f'<a class="source-link" href="{url}" target="_blank">↗ {label}</a>',
				unsafe_allow_html=True,
			)
		st.divider()
		st.markdown('<span class="model-tag">● NVIDIA GPT-OSS 20B</span>', unsafe_allow_html=True)

	st.markdown(
		"""
		<div class="hero">
			<div class="eyebrow">
				<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
				Victoria On Move &middot; Knowledge assistant
			</div>
			<h1>Plan your move with confidence.</h1>
			<p>Ask about services, coverage, contact details, or anything else in the Victoria On Move knowledge base.</p>
			<svg class="route-line" width="180" height="90" viewBox="0 0 180 90" fill="none">
				<path d="M5 80 Q 60 10 100 45 T 175 15" stroke="#C15B32" stroke-width="2" stroke-dasharray="1 8" stroke-linecap="round"/>
				<circle cx="5" cy="80" r="4" fill="#16231B"/>
				<circle cx="175" cy="15" r="5" fill="#C15B32"/>
			</svg>
		</div>
		""",
		unsafe_allow_html=True,
	)

	try:
		rag_chain, chunk_count = build_rag_chain()
	except Exception as error:
		st.error(str(error))
		st.info("Create a .env file containing NVIDIA_API_KEY=your_key, then reload the app.")
		return

	st.markdown(
		f"""
		<div class="metric-row">
			<div class="metric"><strong>{len(SOURCE_URLS)}</strong><span>official sources</span></div>
			<div class="metric"><strong>{chunk_count}</strong><span>indexed text chunks</span></div>
		</div>
		""",
		unsafe_allow_html=True,
	)

	st.markdown(
		"""
		<div class="ask-label">
			<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16231B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
			Ask the knowledge base
		</div>
		""",
		unsafe_allow_html=True,
	)
	question = st.text_input(
		"Your question",
		placeholder="What kind of moving services do they provide?",
		label_visibility="collapsed",
	)
	st.markdown('<p class="ask-hint">Press Enter to search the knowledge base.</p>', unsafe_allow_html=True)

	if question:
		with st.spinner("Searching the knowledge base..."):
			response = rag_chain.invoke({"input": question})

		context_count = len(response.get("context", []))
		st.markdown(
			f"""
			<div class="answer">
				<div class="answer-label">
					<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
					Answer
				</div>
				<p>{response["answer"]}</p>
				<div class="answer-meta">Grounded in {context_count} passage{'s' if context_count != 1 else ''} from the knowledge base</div>
			</div>
			""",
			unsafe_allow_html=True,
		)
		with st.expander("View retrieved sources"):
			for index, document in enumerate(response.get("context", []), start=1):
				source = document.metadata.get("source", "Website")
				st.markdown(
					f"""
					<div class="source-card">
						<div class="source-tag">Source {index} &middot; {source}</div>
						<p>{document.page_content[:700]}</p>
					</div>
					""",
					unsafe_allow_html=True,
				)


if __name__ == "__main__":
	main()