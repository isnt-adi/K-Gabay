from transformers import pipeline, AutoTokenizer
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFacePipeline
from backend.syst_instructions import QA_PROMPT
import tempfile
import os

# Initialize tokenizer and model
MODEL_NAME = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def truncate_input(text: str, max_tokens: int = 512) -> str:
    """Truncate text to fit within token limit."""
    tokens = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    return tokenizer.decode(tokens, skip_special_tokens=True)

def initialize_qa_chain(pdf_file):
    try:
        # Save PDF to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.read())
            tmp_path = tmp_file.name

        # Load PDF and split into chunks
        loader = PyPDFLoader(tmp_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=100
        )
        docs = text_splitter.split_documents(documents)

        # Create FAISS vector store with MiniLM embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(docs, embeddings)

        # Setup HuggingFace pipeline for generation
        pipe = pipeline(
            "text2text-generation",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
            max_length=200,
            truncation=True,
            device="cpu",
            model_kwargs={"cache_dir": "./models"}
        )
        
        local_llm = HuggingFacePipeline(pipeline=pipe)

        # Create Retrieval-Augmented QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=local_llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": QA_PROMPT},
            return_source_documents=False
        )

        os.remove(tmp_path)  # Clean up
        return qa_chain

    except Exception as e:
        raise RuntimeError(f"Failed to initialize QA chain: {e}")
