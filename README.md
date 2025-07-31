---
Streamlit link
https://k-gabay-qbfmtzncqr6wbx2bawr88f.streamlit.app/
---
Huggingface Spaces link
https://huggingface.co/spaces/isnt-adi/K-Gabay
---

# 📘 K-Gabay: An AI College Assistant for Filipino Youth

### 🎓 K-Gabay: Educational Assistant Powered by RAG

**K-Gabay** is a multilingual, AI-powered chatbot that helps Filipino senior high school students and out-of-school youth in the **National Capital Region (NCR)** navigate the college admission process. It uses **Retrieval-Augmented Generation (RAG)** to provide accurate answers from CHED, TESDA, and DepEd documents — with support for **Taglish**, **image uploads**, and **spoken queries**.

---

## 🚀 Features

| Feature                          | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| 📄 PDF Knowledge Retrieval       | Upload CHED/TESDA/DepEd PDFs and ask questions directly                     |
| 🧠 RAG-powered Q&A               | Combines document retrieval + HuggingFace Flan-T5 for better answers        |
| 🌐 Multilingual Input            | English, Filipino, and Taglish supported automatically                      |
| 🖼️ OCR from Images               | Reads and answers questions based on text in screenshots or flyers         |
| 🎙️ Audio Input                   | Ask questions by voice via Whisper (speech-to-text)                         |
| 🧾 Session-based Chat Memory     | Short-term memory lets the bot understand follow-up questions               |
| ❓ Sidebar FAQ                   | Auto-generated helpful questions from your uploaded documents              |

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **AI/LLM:** HuggingFace Transformers (Flan-T5 base/large)  
- **RAG Engine:** LangChain + FAISS  
- **Embedding:** all-MiniLM-L6-v2 (via HuggingFaceEmbeddings)  
- **Speech-to-Text:** OpenAI Whisper  
- **OCR:** Tesseract (`pytesseract`)  
- **PDF Parsing:** PyMuPDF (`fitz`)  
- **Translation:** Google Translate (`googletrans`)

---

## 📦 Installation

### 1. Clone the Repository

```
git clone https://github.com/isnt-adi/K-Gabay.git
cd K-Gabay
```

### 2. Install System Dependencies

```
sudo apt install ffmpeg tesseract-ocr
```

### 3. Set Up Virtual Environment and Install Requirements

```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🧪 Running the App

```
streamlit run app.py
```

Then:
- Upload a CHED, TESDA, or DepEd document
- Or take a photo / screenshot of a flyer
- Or ask by voice in Filipino or English
- Get instant, accurate, document-based answers

---

## 🧠 Example Questions

- “May scholarship ba para sa STEM sa QC?”
- “Translate this CHED memo to Tagalog.”
- “Upload ko yung flyer — kailan ang deadline ng application?”
- “Paano mag-apply sa TESDA kung hindi graduate ng SHS?”

---

## 📁 Project Structure

```
K-Gabay/
├── app.py                  # Streamlit UI logic
├── design.py               # Custom CSS + layout
├── requirements.txt        # Python + ML dependencies
├── logo.jfif               # App branding logo
│
└── backend/
    ├── rag.py              # QA chain logic (RAG + LangChain)
    ├── utils.py            # OCR, audio, translation, and helper tools
    └── syst_instructions.py # System prompt + few-shot examples
```

---

## 🎯 SDG 4 – Quality Education

K-Gabay supports **UN Sustainable Development Goal #4** by improving access to trustworthy, localized college information for underprivileged students in the Philippines. Inspired by *Kolehiyo Updates* groups, it aims to centralize scattered educational resources into a smart, friendly chatbot.

---

## 🤝 Contributing

Got school datasets, feedback, or feature ideas?  
Feel free to fork the repo, open an issue, or send a pull request.

---

## 📜 License

MIT License — for educational, non-commercial use only.
