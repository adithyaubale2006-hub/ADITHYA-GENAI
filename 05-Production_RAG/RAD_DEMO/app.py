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
	page_icon="M",
	layout="wide",
	initial_sidebar_state="expanded",
)

st.markdown(
	"""
	<style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
	:root { --ink: #17211b; --muted: #6c776f; --paper: #f7f5ef; --mint: #d9f2df; --orange: #ef724b; }
	.stApp { background: var(--paper); color: var(--ink); font-family: 'DM Sans', sans-serif; }
	h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; letter-spacing: 0; }
	.hero { padding: 3.5rem 0 2rem; border-bottom: 1px solid #dfe3dc; }
	.eyebrow { color: var(--orange); font-size: .78rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
	.hero h1 { font-size: clamp(2.5rem, 6vw, 5.4rem); line-height: .95; max-width: 760px; margin: .7rem 0 1rem; }
	.hero p { color: var(--muted); font-size: 1.05rem; max-width: 610px; }
	.answer { background: var(--mint); border: 1px solid #bdddc5; border-radius: 8px; padding: 1.5rem 1.7rem; margin: 1.2rem 0; }
	.answer-label { color: #39704b; font-size: .75rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }
	.answer p { font-size: 1.3rem; line-height: 1.45; margin: .6rem 0 0; }
	.metric { border-top: 2px solid var(--ink); padding-top: .7rem; }
	.metric strong { font-family: 'Space Grotesk'; font-size: 1.6rem; }
	.metric span { color: var(--muted); display: block; font-size: .8rem; margin-top: .15rem; }
	[data-testid='stSidebar'] { background: #e9eee7; border-right: 1px solid #d5ddd3; }
	[data-testid='stSidebar'] h2 { font-size: 1.05rem; }
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
		st.markdown("## Movewise")
		st.caption("A source-grounded assistant for Victoria On Move.")
		st.divider()
		st.markdown("### Knowledge base")
		st.caption("Answers are retrieved from the official Victoria On Move website.")
		for url in SOURCE_URLS:
			st.markdown(f"[{url.split('/')[-1] or 'home'}]({url})")
		st.divider()
		st.caption("Model · NVIDIA GPT-OSS 20B")

	st.markdown(
		'<div class="hero"><div class="eyebrow">Victoria On Move · Knowledge assistant</div>'
		'<h1>Plan your move with confidence.</h1>'
		'<p>Ask about services, coverage, contact details, or anything else in the Victoria On Move knowledge base.</p></div>',
		unsafe_allow_html=True,
	)

	try:
		rag_chain, chunk_count = build_rag_chain()
	except Exception as error:
		st.error(str(error))
		st.info("Create a .env file containing NVIDIA_API_KEY=your_key, then reload the app.")
		return

	metric_one, metric_two = st.columns(2)
	with metric_one:
		st.markdown(f'<div class="metric"><strong>{len(SOURCE_URLS)}</strong><span>official sources</span></div>', unsafe_allow_html=True)
	with metric_two:
		st.markdown(f'<div class="metric"><strong>{chunk_count}</strong><span>indexed text chunks</span></div>', unsafe_allow_html=True)

	st.markdown("## Ask the knowledge base")
	question = st.text_input(
		"Your question",
		placeholder="What kind of moving services do they provide?",
		label_visibility="collapsed",
	)
	if question:
		with st.spinner("Searching the knowledge base..."):
			response = rag_chain.invoke({"input": question})
		st.markdown(
			f'<div class="answer"><div class="answer-label">Answer</div><p>{response["answer"]}</p></div>',
			unsafe_allow_html=True,
		)
		with st.expander("View retrieved sources"):
			for index, document in enumerate(response.get("context", []), start=1):
				source = document.metadata.get("source", "Website")
				st.markdown(f"**Source {index}:** `{source}`")
				st.write(document.page_content[:700])


if __name__ == "__main__":
	main()
