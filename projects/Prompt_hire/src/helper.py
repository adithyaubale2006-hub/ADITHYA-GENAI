from langchain_community.document_loaders import PyPDFLoader
from langchain_community.docstore.document import Document
from langchain_text_splitters import TokenTextSplitter
from langchain_nvidia import ChatNVIDIA
from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA

import os
from dotenv import load_dotenv
from src.prompt import *


#Load API KEY
load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
os.environ["NVIDIA_API_KEY"] = api_key

def file_processing(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()

    question_gen = ""

    for page in data:
        question_gen += page.page_content

    splitter_ques_gen = TokenTextSplitter(
        chunk_size=2000, chunk_overlap=200
    )

    chunks_ques_gen = splitter_ques_gen.split_text(question_gen)

    document_ques_gen = [Document(page_content=t) for t in chunks_ques_gen]

    splitter_ans_gen = TokenTextSplitter(
        chunk_size=2000, chunk_overlap=200
    )

    document_answer_gen = splitter_ans_gen.split_documents(document_ques_gen)

    return document_ques_gen, document_answer_gen


def llm_pipeline(file_path):
    document_ques_gen, document_answer_gen = file_processing(file_path)

    llm = ChatNVIDIA(
        temperature=0.3,
        model="openai/gpt-oss-20b"
    )

    PROMPT_QUESTIONS = PromptTemplate(template=prompt_template, input_variables=["text"])

    REFINE_PROMPT_QUESTIONS = PromptTemplate(
        input_variables=["existing_answer", "text"],
        template=refine_template,
    )

    ques_chain_gen = load_summarize_chain(
        llm=llm,
        chain_type="refine",
        question_prompt=PROMPT_QUESTIONS,
        refine_prompt=REFINE_PROMPT_QUESTIONS,
        verbose=True
    )

    ques = ques_chain_gen.invoke(document_ques_gen)

    return ques


def llm_pipeline(file_path):
    document_ques_gen, document_answer_gen = file_processing(file_path)

    # Initialize NVIDIA LLM and Embeddings to replace OpenAI
    llm = ChatNVIDIA(model="openai/gpt-oss-20b", temperature=0.3, timeout=120)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Generate questions using the refine chain
    ques_chain_gen = load_summarize_chain(
    llm, 
    chain_type="refine", 
    question_prompt= prompt_template, 
    refine_prompt= refine_template, 
    verbose=True
)
    ques = ques_chain_gen.invoke(document_ques_gen)
    ques_text = ques.get("output_text", "")

    # Build the FAISS vector store
    vector_store = FAISS.from_documents(document_answer_gen, embeddings)

    # Process and filter the question list (matching the instructor's logic visible on screen)
    ques_list = ques_text.split("\n")
    filtered_ques_list = [element for element in ques_list if element.endswith('?') or element.endswith('.')]

    # Create the RetrievalQA chain for answers
    answer_generation_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )

    return answer_generation_chain, filtered_ques_list