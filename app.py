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

# --- QA Chain Setup ---
if uploaded_file and "qa_chain" not in st.session_state:
    try:
        st.session_state.qa_chain = initialize_qa_chain(uploaded_file)
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi there! Ask me anything about the PDF!"}
        ]
    except Exception as e:
        st.error(f"❌ PDF processing failed: {e}")

# --- Fallback Message History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Upload a PDF to start chatting!"}
    ]

# --- Display Chat Messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input Form ---
user_prompt = ""
with st.form("chat_input", clear_on_submit=True):
    col1, col2, col3 = st.columns([6, 1, 1])

    # Text input
    user_text = col1.text_input("Ask K-Gabay something")

    # Audio upload via mic icon
    with col2:
        st.markdown('<label for="audio-upload" class="upload-icon">🎤</label>', unsafe_allow_html=True)
        user_audio = st.file_uploader("Audio", type=["mp3", "wav", "m4a"], key="audio-upload", label_visibility="collapsed")

    # Image upload via photo icon
    with col3:
        st.markdown('<label for="image-upload" class="upload-icon">📷</label>', unsafe_allow_html=True)
        user_image = st.file_uploader("Image", type=["jpg", "jpeg", "png"], key="image-upload", label_visibility="collapsed")

    submitted = st.form_submit_button("📨 Send")

# --- Input Prioritization ---
if submitted:
    if user_text:
        user_prompt = user_text
    elif user_audio:
        user_prompt = transcribe_audio(user_audio)
        st.success(f"Transcribed: {user_prompt}")
    elif user_image:
        user_prompt = extract_text_from_image(user_image)
        st.success(f"Extracted: {user_prompt}")

# --- Chat Handling ---
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    if "qa_chain" in st.session_state:
        translated_input, lang = translate_input(user_prompt)

        with st.spinner("Thinking..."):
            try:
                raw_response = st.session_state.qa_chain.run(translated_input)
                final_response = translate_output(raw_response, lang)
            except Exception as e:
                final_response = f"❌ Error: {e}"
    else:
        final_response = "⚠️ No PDF processed yet."

    st.session_state.messages.append({"role": "assistant", "content": final_response})
    st.rerun()
