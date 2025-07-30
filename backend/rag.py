import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from backend.syst_instructions import QA_PROMPT

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

# --- Load Larger Model for Better Accuracy ---
def load_llm():
    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-large",  # more accurate than flan-t5-base
        tokenizer="google/flan-t5-large",
        device=0,
        max_new_tokens=512
    )
    return HuggingFacePipeline(pipeline=pipe)

llm = load_llm()

# --- Extract Text from Uploaded PDF ---
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# --- Initialize RAG Chain ---
def initialize_qa_chain(uploaded_file):
    raw_text = extract_text_from_pdf(uploaded_file)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(raw_text)

    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = FAISS.from_texts(chunks, embedding=embedder)

    # Increase k to 4 for broader context, helps reduce hallucination
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=False,
        chain_type_kwargs={"prompt": QA_PROMPT}
    )
    return qa_chain
