# app.py
import streamlit as st
from backend.utils import (
    translate_input,
    translate_output,
    transcribe_audio,
    extract_text_from_image,
    get_faqs,
)
from backend.rag import initialize_qa_chain 
from design import apply_custom_styles
import os

# --- Page Config & Styling ---
st.set_page_config(page_title="K-Gabay", layout="wide")
apply_custom_styles()

# --- Centered Logo ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jfif", use_container_width=True)

# --- Sidebar: File Upload & FAQs ---
with st.sidebar:
    st.subheader("📄 Upload a PDF")
    uploaded_file = st.file_uploader("Upload an educational PDF", type="pdf")
    st.subheader("📌 FAQs")
    for faq in get_faqs():
        with st.expander(faq["question"]):
            st.write(faq["answer"])

# --- Cached QA Chain Initialization ---
@st.cache_resource(show_spinner="Processing PDF and initializing AI...")
def get_qa_chain_cached(pdf_data_or_path):
    """
    Caches the initialization of the QA chain.
    pdf_data_or_path will either be the UploadedFile object or the raw bytes of the default PDF.
    """
    if isinstance(pdf_data_or_path, bytes):
        from io import BytesIO
        pdf_file_like = BytesIO(pdf_data_or_path)
        return initialize_qa_chain(pdf_file_like)
    else: 
        return initialize_qa_chain(pdf_data_or_path)

# Determine which PDF to use and get its content/object for caching
pdf_content_for_caching = None
current_pdf_id = None

if uploaded_file:
    pdf_content_for_caching = uploaded_file
    current_pdf_id = uploaded_file.name
else:

    try:
        with open("backend/data/base.pdf", "rb") as f:
            default_pdf_bytes = f.read()
        pdf_content_for_caching = default_pdf_bytes
        current_pdf_id = "base_pdf_default" # Use a fixed string ID for the default PDF
        st.info("Using a default PDF. Upload pdfs in the sidebar for more detailed answers.")
    except FileNotFoundError:
        st.error("❌ Default PDF not found. Please ensure 'backend/data/base.pdf' exists.")
        pdf_content_for_caching = None # Indicate no PDF is available


# Initialize QA chain if a PDF is available
if pdf_content_for_caching:
    st.session_state.qa_chain = get_qa_chain_cached(pdf_content_for_caching)
    
    if "current_pdf_id" not in st.session_state or st.session_state.current_pdf_id != current_pdf_id:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi there! Ask me anything about the document."}
        ]
        st.session_state.current_pdf_id = current_pdf_id
else:
    st.session_state.qa_chain = None
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Please upload a PDF or wait for the default to load."}
        ]


# --- Fallback Message History (if no PDF loaded or first run) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Upload a PDF to start chatting!"}
    ]

# --- Display Chat Messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Input Row: Chat + Expandable Media Uploads ---
user_prompt = st.chat_input("Type your message here...")

with st.expander("🎧 Upload Audio or Image", expanded=False):
    media_cols = st.columns(2)

    with media_cols[0]:
        audio_file = st.file_uploader("🎙️ Upload audio", type=["wav", "mp3"], key="audio")
        if audio_file:
            # Add a spinner while transcribing
            with st.spinner("Transcribing audio..."):
                transcribed_text = transcribe_audio(audio_file)
            if transcribed_text:
                user_prompt = transcribed_text
                st.success(f"Transcribed: {user_prompt}")
            else:
                st.warning("Could not transcribe audio.")


    with media_cols[1]:
        image_file = st.file_uploader("🖼️ Upload image", type=["png", "jpg", "jpeg"], key="image")
        if image_file:
            with st.spinner("Extracting text from image..."):
                extracted_text = extract_text_from_image(image_file)
            if extracted_text:
                user_prompt = extracted_text
                st.success(f"Extracted: {user_prompt}")
            else:
                st.warning("Could not extract text from image.")
        
# --- Chat Handling ---
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    if "qa_chain" in st.session_state and st.session_state.qa_chain:
        translated_input, lang = translate_input(user_prompt)

        with st.spinner("Thinking... (This may take a while on CPU)"):
            try:
                response_obj = st.session_state.qa_chain.invoke({"query": translated_input})
                raw_response = response_obj.get('result', "No answer found.")
                final_response = translate_output(raw_response, lang)
            except Exception as e:
                final_response = f"❌ Error during QA chain invocation: {e}"
                st.error(final_response)
    else:
        final_response = "⚠️ No PDF processed yet. Please upload a PDF or wait for the default."

    st.session_state.messages.append({"role": "assistant", "content": final_response})
    st.rerun()
