K-GABAY: A COLLEGE-PREP EDUCATIONAL ASSISTANT FOR FILIPINO YOUTH
================================================================

K-Gabay is an AI-powered educational assistant designed to support Filipino senior high school students and out-of-school youth (OSY) in the National Capital Region (NCR) as they navigate the complex process of entering higher education.

Built around SDG 4 – Quality Education, K-Gabay bridges information gaps in college admissions by consolidating official resources from CHED, TESDA, and DepEd, delivered through a multilingual, retrieval-augmented chatbot interface.

PROBLEM STATEMENT
------------------

Despite the abundance of educational programs, many youth in NCR still miss college opportunities due to:

- Lack of early orientation and guidance
- Confusing or mismatched exam/application timelines
- Scarce awareness of scholarships or accredited programs
- Language barriers and limited digital access

SOLUTION
--------

K-Gabay helps students:

- Upload and ask questions about educational PDFs (CHED memoranda, TESDA modules, etc.)
- Get info on college programs, admission schedules, and accredited schools
- Explore scholarship opportunities
- Extract text from images and transcribe audio using OCR and Whisper
- Ask questions in Tagalog, English, or Taglish — auto-translated!

TECH STACK
----------

Frontend       : Streamlit
Model          : google/flan-t5-base (HuggingFace)
RAG            : LangChain + FAISS
Embeddings     : all-MiniLM-L6-v2
PDF Handling   : PyMuPDF
OCR            : Tesseract
Audio Handling : OpenAI Whisper
Translation    : googletrans
Styling        : Custom CSS

FOLDER STRUCTURE
-----------------

K-Gabay/
│
├── app.py                   -> Main Streamlit app
├── design.py                -> Custom styles
├── requirements.txt         -> Python dependencies
├── logo.jfif                -> Branding image
│
└── backend/
    ├── rag.py               -> PDF processing and RAG logic
    ├── utils.py             -> OCR, audio, translation, FAQs
    └── syst_instructions.py -> System prompt template

HOW TO RUN
----------

1. Clone the repository

   git clone https://github.com/YOUR_USERNAME/K-Gabay.git
   cd K-Gabay

2. Install dependencies

   pip install -r requirements.txt

3. Run the app

   streamlit run app.py

SOURCE DOCUMENTS
-----------------

- CHED Connect        : https://phlconnect.ched.gov.ph/
- TESDA e-Learning    : https://e-tesda.gov.ph/
- CHED COE List (PDF) : https://ieducationphl.ched.gov.ph/
- PAASCU Schools      : https://paascu.org.ph/member-database/

SAMPLE QUESTIONS
----------------

- "Kailan ang entrance exam para sa nursing sa NCR?"
- "What is the passing grade in CHED Flexible Learning guidelines?"
- "I-upload ko yung TESDA Dressmaking module, then tanong ako."

LICENSE
-------

This project is for educational and non-commercial use only.
