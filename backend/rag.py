from transformers import pipeline, AutoTokenizer
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import HuggingFacePipeline
from backend.syst_instructions import QA_PROMPT
import tempfile
import os

# Initialize tokenizer and model
MODEL_NAME = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def truncate_input(text, max_tokens=512):
    tokens = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    return tokenizer.decode(tokens, skip_special_tokens=True)

def initialize_qa_chain(pdf_file):
    try:
        # Step 1: Save PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.read())
            tmp_path = tmp_file.name

        # Step 2: Load PDF and split into chunks
        loader = PyPDFLoader(tmp_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=100
        )
        docs = text_splitter.split_documents(documents)

        # Step 3: Create FAISS index
        embeddings = HuggingFaceEmbeddings()
        vectorstore = FAISS.from_documents(docs, embeddings)

        # Step 4: Set up generation pipeline
        pipe = pipeline(
            "text2text-generation",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
            max_length=512,
            device=-1  # CPU
        )
        local_llm = HuggingFacePipeline(pipeline=pipe)

        prompt = QA_PROMPT
        
        # Step 6: Create RAG chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=local_llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=False
        )

        # Clean up temp file
        os.remove(tmp_path)
        return qa_chain

    except Exception as e:
        raise RuntimeError(f"Failed to initialize QA chain: {e}")
