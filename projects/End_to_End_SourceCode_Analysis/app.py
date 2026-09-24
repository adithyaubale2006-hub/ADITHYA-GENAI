from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from src.helper import load_embedding
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI  # Swap with ChatGoogleGenerativeAI if using Gemini
from langchain_classic.memory import ConversationSummaryMemory
from langchain_classic.chains import ConversationalRetrievalChain
import os
import json
import re
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load embeddings and connect to the persisted vector database
embeddings = load_embedding()
persist_directory = "db"
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# Initialize LLM, Memory, and the Conversational Retrieval Chain
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    api_key=os.environ["GEMINI_API_KEY"],
    max_tokens=1000,
    temperature=0.2
)
memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)
qa = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 8}),
    memory=memory
)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route('/get', methods=["POST"])
def chat():
    """
    Gets the message from the HTML form, passes it to LangChain, and
    returns the answer as JSON.

    NOTE: The only change here from the original version is that the
    call is wrapped in try/except. The RAG chain itself (qa.invoke) is
    completely unchanged - this just makes sure that if something goes
    wrong (bad API key, retrieval error, rate limit, etc.) the frontend
    gets a clean JSON error message instead of a raw HTML stack trace.

    Kept as-is (non-streaming) for backwards compatibility / as a simple
    fallback endpoint; the frontend now calls /stream instead.
    """
    msg = request.form.get("msg", "").strip()

    if not msg:
        return jsonify({"error": "Please enter a message before sending."}), 400

    try:
        result = qa.invoke({"question": msg})
        return jsonify({"answer": result["answer"]})
    except Exception as e:
        # Log the real error server-side for debugging...
        app.logger.error(f"Error while processing chat message: {e}")
        # ...but only send a generic, user-friendly message to the client.
        return jsonify({"error": "Something went wrong while generating a response. Please try again."}), 500


def sse_event(payload: dict) -> str:
    """Formats one Server-Sent-Events message: 'data: <json>\\n\\n'."""
    return f"data: {json.dumps(payload)}\n\n"


def generate_answer_stream(msg: str):
    """
    Generator that yields the AI's answer to the browser word-by-word.

    IMPORTANT (design note, see chat explanation): this is a *simulated*
    stream, not true LLM token streaming. qa.invoke() is called exactly
    once, exactly as it always was — the chain/retriever/memory logic is
    100% unchanged. Once the full answer text comes back, we release it
    to the client gradually instead of all at once, so the browser can
    render it as if it were being typed live. The delay between words is
    an artificial pacing choice for the UI, not a sign of real per-word
    computation.
    """
    try:
        result = qa.invoke({"question": msg})
        answer = result["answer"]
    except Exception as e:
        app.logger.error(f"Error while processing chat message: {e}")
        yield sse_event({"error": "Something went wrong while generating a response. Please try again."})
        return

    # Split on whitespace but keep the whitespace attached to each word,
    # so spacing/newlines in the original answer are preserved exactly.
    for word in re.findall(r"\S+\s*", answer):
        yield sse_event({"token": word})
        time.sleep(0.025)  # pacing only - tune for faster/slower "typing"

    yield sse_event({"done": True})


@app.route('/stream', methods=["POST"])
def stream():
    """
    Streaming counterpart to /get. Uses Server-Sent Events (SSE): a plain
    HTTP response kept open, with the server pushing 'data: ...' lines as
    they become available, instead of the client waiting for one single
    JSON payload at the end.
    """
    msg = request.form.get("msg", "").strip()

    if not msg:
        def empty_message_error():
            yield sse_event({"error": "Please enter a message before sending."})
        return Response(stream_with_context(empty_message_error()), mimetype="text/event-stream")

    response = Response(stream_with_context(generate_answer_stream(msg)), mimetype="text/event-stream")
    # Ask any intermediate proxy (e.g. nginx) not to buffer the response,
    # since buffering would defeat the purpose of streaming.
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


if __name__ == '__main__':
    app.run(debug=True)