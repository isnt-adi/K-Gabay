# === rag.py ===
from transformers import pipeline, AutoTokenizer
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFacePipeline
from backend.syst_instructions import QA_PROMPT, REFINE_PROMPT
import tempfile
import os

# Initialize tokenizer and model
MODEL_NAME = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def truncate_input(text: str, max_tokens: int = 512) -> str:
    """Truncate text to fit within token limit."""
    tokens = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    return tokenizer.decode(tokens, skip_special_tokens=True)

def initialize_qa_chain(pdf_file_like):
    try:
        if hasattr(pdf_file_like, 'seek'):
            pdf_file_like.seek(0)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file_like.read())
            tmp_path = tmp_file.name

        # Load and split PDF into chunks
        loader = PyPDFLoader(tmp_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        docs = text_splitter.split_documents(documents)

        # FAISS vector store with MiniLM embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(docs, embeddings)

        # HuggingFace generation pipeline
        pipe = pipeline(
            "text2text-generation",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
            device=-1,
            max_new_tokens=512,
            truncation=True
        )
        local_llm = HuggingFacePipeline(pipeline=pipe)

        # RetrievalQA chain using refine mode
        qa_chain = RetrievalQA.from_chain_type(
            llm=local_llm,
            chain_type="refine",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
            chain_type_kwargs={
                "question_prompt": QA_PROMPT,
                "refine_prompt": REFINE_PROMPT
            },
            return_source_documents=False
        )

        os.remove(tmp_path)
        return qa_chain

    except Exception as e:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise RuntimeError(f"Failed to initialize QA chain: {e}")
