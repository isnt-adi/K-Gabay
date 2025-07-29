from PIL import Image
import pytesseract
import whisper
from googletrans import Translator

# --- Init Translator and Whisper model ---
translator = Translator()
whisper_model = whisper.load_model("base")

def translate_input(text):
    detected = translator.detect(text).lang
    translated = translator.translate(text, src=detected, dest='en').text
    return translated, detected

def translate_output(text, target_lang):
    if target_lang != 'en':
        return translator.translate(text, src='en', dest=target_lang).text
    return text

def transcribe_audio(file):
    with open("temp_audio.wav", "wb") as f:
        f.write(file.read())
    result = whisper_model.transcribe("temp_audio.wav")
    os.remove("temp_audio.wav")
    return result['text']

def extract_text_from_image(uploaded_file):
    image = Image.open(uploaded_file)
    return pytesseract.image_to_string(image)

def get_faqs():
    return [
        {"question": "What is RAG?", "answer": "Retrieval-Augmented Generation (RAG) is a system that combines retrieval from documents with text generation."},
        {"question": "Paano ito makakatulong sa akin?", "answer": "Makakatulong ito sa pagkuha ng impormasyon mula sa mga dokumentong educational sa pamamagitan ng tanong at sagot."},
        {"question": "Can I ask in Taglish?", "answer": "Oo naman! K-Gabay supports English, Filipino, and Taglish queries."},
    ]
