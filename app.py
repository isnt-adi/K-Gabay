import streamlit as st
from backend.system import initialize_qa_chain
from backend.utils import extract_text_from_file, detect_language, convert_audio_to_text, extract_text_from_image, translate_text

# --- Page Config ---
st.set_page_config(page_title="K-Gabay", layout="wide")

# --- Custom CSS for Sidebar and Upload Buttons ---
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #003300, #25d025);
        color: white;
    }
    .small-upload .stFileUploader {
        padding: 0.25rem !important;
        font-size: 0.75rem !important;
        max-width: 200px;
    }
</style>
""", unsafe_allow_html=True)

# --- Logo ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jfif", width=900)

# --- Upload Section in Dropdown ---
with st.expander("📎 Upload Image, Audio, or PDF"):
    st.markdown('<div class="small-upload">', unsafe_allow_html=True)
    pdf_file = st.file_uploader("📄 Upload PDF", type=["pdf"])
    image_file = st.file_uploader("🖼️ Upload Image", type=["png", "jpg", "jpeg"])
    audio_file = st.file_uploader("🎙️ Upload Audio", type=["mp3", "wav"])
    st.markdown('</div>', unsafe_allow_html=True)

# --- Initialize QA System ---
qa_chain = initialize_qa_chain()

# --- Chat Interface ---
user_input = st.chat_input("Ask me anything about the uploaded content...")

if user_input:
    final_input = ""

    # Handle uploaded content
    if pdf_file:
        text = extract_text_from_file(pdf_file)
        final_input += text + "\n"
    if image_file:
        image_text = extract_text_from_image(image_file)
        final_input += image_text + "\n"
    if audio_file:
        audio_text = convert_audio_to_text(audio_file)
        final_input += audio_text + "\n"

    final_input += user_input

    # Detect language and translate if necessary
    detected_lang = detect_language(final_input)
    if detected_lang != "en":
        final_input = translate_text(final_input, detected_lang, "en")

    # Get answer
    response = qa_chain.invoke({"question": final_input})
    answer = response if isinstance(response, str) else response.get("answer", "Sorry, I couldn't find an answer.")

    # Translate answer back to original language
    if detected_lang != "en":
        answer = translate_text(answer, "en", detected_lang)

    # Display messages
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        st.write(answer)
