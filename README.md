# K-Gabay: Edu Assistant for Filipino Youth 🇵🇭

K-Gabay is a multilingual, document-aware educational assistant designed to help Filipino senior high school students and out-of-school youth in the National Capital Region (NCR) navigate college admissions. It supports text, audio, and image inputs to answer queries about programs, schedules, scholarships, and more—powered by a Retrieval-Augmented Generation (RAG) pipeline.

---

## 🎯 Features

* 🧠 **Retrieval-Augmented Generation (RAG)** using CHED, TESDA, and DepEd source documents
* 📄 **PDF Upload & Vectorization** with FAISS and LangChain
* 🗣️ **Multilingual Support** (English, Filipino, Taglish)
* 🎙️ **Audio Input** via OpenAI Whisper transcription
* 🖼️ **Image Input** using OCR (Tesseract)
* 💬 **ChatGPT-style UI** with persistent short-term chat history
* 📌 **FAQs Sidebar** with expandable common questions

---

## 🧰 Technologies Used

* **Streamlit** for frontend interface
* **LangChain** for QA and prompt chaining
* **FAISS** for in-memory vector store
* **Transformers (Flan-T5)** for generation
* **PyMuPDF** for PDF parsing
* **Pillow + pytesseract** for image OCR
* **OpenAI Whisper** for audio transcription
* **Googletrans** for multilingual translation

---

## 🗂️ File Structure

```
k-gabay/
├── app.py                     # Streamlit main app
├── design.py                 # UI styles
├── backend/
│   ├── system.py             # Core logic: QA, OCR, audio, translation
│   └── syst_instructions.py  # LangChain RAG prompt
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started (Local)

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/k-gabay.git
cd k-gabay
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate  # For Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

> 🔒 **Note:** Ensure you have a `.env` file with any necessary HuggingFace keys or model configs.

---

## ☁️ Deploying to Streamlit Cloud

1. Push the repo to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo
4. Set `app.py` as the main file
5. Add `HF_API_KEY` or other secrets in Streamlit's Secrets tab

---

## 💡 Future Enhancements

* 🎓 Scholarship Matching System
* 🧾 Document citation rendering
* 🧑‍🎓 Personalized guidance based on learner profile

---

## 📜 License

MIT License

---

## 🤝 Acknowledgments

Inspired by the Filipino Facebook community "Kolehiyo Updates" and aligned with **SDG 4: Quality Education**.
