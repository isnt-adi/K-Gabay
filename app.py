import streamlit as st
from backend.rag import initialize_qa_chain
from backend.utils import (
    extract_text_from_file,
    detect_language,
    convert_audio_to_text,
    extract_text_from_image,
    translate_text
)

# --- Page Config ---
st.set_page_config(page_title="K-Gabay", layout="wide")

# --- App Logo and Title ---
st.markdown("<h1 style='text-align: center;'>📚 K-Gabay</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your multilingual education assistant powered by AI + CHED/TESDA data</p>", unsafe_allow_html=True)

# --- Initialize Session State ---
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = initialize_qa_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input Form ---
with st.form("chat_input", clear_on_submit=True):
    col1, col2, col3 = st.columns([6, 1, 1])

    # Text input
    user_text = col1.text_input("Ask K-Gabay something", label_visibility="collapsed")

    # Audio upload via mic icon
    with col2:
        st.markdown('<label for="audio-upload" class="upload-icon">🎤</label>', unsafe_allow_html=True)
        user_audio = st.file_uploader("Audio", type=["mp3", "wav", "m4a"], key="audio-upload", label_visibility="collapsed")

    # Image upload via photo icon
    with col3:
        st.markdown('<label for="image-upload" class="upload-icon">📷</label>', unsafe_allow_html=True)
        user_image = st.file_uploader("Image", type=["jpg", "jpeg", "png"], key="image-upload", label_visibility="collapsed")

    submitted = st.form_submit_button("📨 Send")

# --- Process User Input ---
if submitted:
    user_prompt = ""

    if user_text:
        user_prompt = user_text
    elif user_audio:
        user_prompt = convert_audio_to_text(user_audio)
    elif user_image:
        user_prompt = extract_text_from_image(user_image)

    if not user_prompt:
        st.warning("Please enter a question, upload an image, or speak your question.")
        st.stop()

    # Language Detection and Translation
    original_language = detect_language(user_prompt)
    translated_input = translate_text(user_prompt, dest_language="en")

    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.spinner("Thinking..."):
        try:
            raw_response = st.session_state.qa_chain.run(translated_input)
            final_response = translate_text(raw_response, dest_language=original_language)
        except Exception as e:
            final_response = f"⚠️ Error generating response: {e}"

    st.session_state.messages.append({"role": "assistant", "content": final_response})

    with st.chat_message("assistant"):
        st.markdown(final_response)
