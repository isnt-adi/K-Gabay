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

# Always determine which PDF to use
if uploaded_file:
    source_pdf = uploaded_file
else:
    source_pdf = open("backend/data/base.pdf", "rb")
    st.info("Using a default PDF. Upload pdfs in the sidebar for more detailed answers.")

# Always initialize or reinitialize QA chain if file changes
if "last_source" not in st.session_state or st.session_state.last_source != source_pdf:
    try:
        st.session_state.qa_chain = initialize_qa_chain(source_pdf)
        st.session_state.last_source = source_pdf
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi there! Ask me anything about the document."}
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

# --- Input Row: Chat + Expandable Media Uploads ---
user_prompt = st.chat_input("Type your message here...")

with st.expander("🎧 Upload Audio or Image", expanded=False):
    media_cols = st.columns(2)

    with media_cols[0]:
        audio_file = st.file_uploader("🎙️ Upload audio", type=["wav", "mp3"], key="audio")
        if audio_file:
            user_prompt = transcribe_audio(audio_file)
            st.success(f"Transcribed: {user_prompt}")

    with media_cols[1]:
        image_file = st.file_uploader("🖼️ Upload image", type=["png", "jpg", "jpeg"], key="image")
        if image_file:
            user_prompt = extract_text_from_image(image_file)
            st.success(f"Extracted: {user_prompt}")
        
# --- Chat Handling ---
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    if "qa_chain" in st.session_state:
        translated_input, lang = translate_input(user_prompt)

       with st.spinner("Thinking..."):
    try:
        raw_response = st.session_state.qa_chain.invoke(
            {"query": translated_input},
            timeout=30
        )
        final_response = translate_output(raw_response["result"], lang) 
    except Exception as e:
        final_response = f"❌ Processing took too long or failed: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": final_response})
