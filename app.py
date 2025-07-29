import streamlit as st
import os

from backend.utils import (
    translate_input,
    translate_output,
    extract_text_from_image,
    transcribe_audio,
    get_faqs
)
from backend.rag import initialize_qa_chain

# --- Streamlit Page Setup ---
st.set_page_config(page_title="K-Gabay Enhanced", layout="wide")
st.title("📚 K-Gabay - Edu Assistant (Multilingual)")

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

# --- Sidebar ---
st.sidebar.title("📌 FAQs")
faqs = get_faqs()
for faq in faqs:
    with st.sidebar.expander(faq["question"]):
        st.write(faq["answer"])

st.sidebar.subheader("📄 Upload a PDF")
uploaded_files = st.sidebar.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files and st.session_state.qa_chain is None:
    try:
        st.session_state.qa_chain = initialize_qa_chain(uploaded_files[0])
        st.sidebar.success("PDF processed successfully!")
    except Exception as e:
        st.sidebar.error(f"Failed to process PDF: {e}")

# --- Input Section ---
st.markdown("### Ask a Question 🧠")

col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_input("Enter your question:", key="user_text")
with col2:
    input_type = st.radio("Input type:", ["Text", "Audio", "Image"])

# --- File Uploads ---
if input_type == "Audio":
    audio_file = st.file_uploader("Upload audio file (WAV/MP3)", type=["wav", "mp3"])
    if audio_file:
        user_input = transcribe_audio(audio_file)
        st.success(f"Transcribed: {user_input}")

elif input_type == "Image":
    image_file = st.file_uploader("Upload image with text", type=["png", "jpg", "jpeg"])
    if image_file:
        user_input = extract_text_from_image(image_file)
        st.success(f"Extracted: {user_input}")

# --- Chat Interaction ---
if user_input:
    translated_input, lang = translate_input(user_input)

    if st.session_state.qa_chain:
        try:
            response = st.session_state.qa_chain.run(translated_input)
        except Exception as e:
            response = f"❌ Error: {e}"
    else:
        response = "⚠️ Please upload a PDF first."

    translated_output = translate_output(response, lang)

    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "bot", "text": translated_output})

# --- Chat History Display ---
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(
            f"<div style='text-align:right; color:#1a73e8'><b>You:</b> {message['text']}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='text-align:left; background-color:#e6f0ff; padding:10px; border-radius:10px'><b>K-Gabay:</b> {message['text']}</div>",
            unsafe_allow_html=True,
        )
