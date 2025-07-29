import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        /* === Logo Color Palette === */
        :root {
            --logo-primary: #4a54ad;     /* Deep Periwinkle (main brand) */
            --logo-dark: #282e60;        /* Navy (contrast/dark mode) */
            --logo-light: #e5f1fd;      /* Cloud Blue (background) */
            --logo-white: #feffff;       /* Pure White (text/accents) */
            --logo-accent: #ff6b6b;     /* Complementary accent (optional) */
        }

        /* === App Container === */
        [data-testid="stAppViewContainer"] {
            background-color: var(--logo-light);
            font-family: 'Arial', sans-serif;
        }

        /* === Sidebar (Vertical Gradient) === */
        [data-testid="stSidebar"] {
            background: linear-gradient(
                to bottom,
                var(--logo-dark),
                var(--logo-primary)
            ) !important;
            padding: 1.5rem;
        }

        /* === Typography === */
        [data-testid="stMarkdownContainer"] h1 {
            color: var(--logo-dark) !important;
            border-bottom: 2px solid var(--logo-primary);
            padding-bottom: 8px;
        }
        [data-testid="stMarkdownContainer"] h2 {
            color: var(--logo-primary) !important;
            font-weight: 600;
        }
        [data-testid="stMarkdownContainer"] h3 {
            color: var(--logo-dark) !important;
        }
        [data-testid="stMarkdownContainer"] p {
            color: var(--logo-dark);
        }

        /* === Chat Messages === */
        [data-testid="stChatMessage"] {
            padding: 14px;
            border-radius: 12px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        /* User messages (white with primary accent) */
        [data-testid="stChatMessage"]:nth-child(odd) {
            background-color: var(--logo-white) !important;
            border-left: 4px solid var(--logo-primary) !important;
        }
        /* Assistant messages (primary color) */
        [data-testid="stChatMessage"]:nth-child(even) {
            background-color: var(--logo-primary) !important;
            color: var(--logo-white) !important;
        }

        /* === Interactive Elements === */
        /* Buttons */
        button {
            background-color: var(--logo-primary) !important;
            color: var(--logo-white) !important;
            border-radius: 8px !important;
            transition: all 0.2s;
        }
        button:hover {
            background-color: var(--logo-dark) !important;
            transform: translateY(-1px);
        }
        /* File uploader */
        [data-testid="stFileUploader"] {
            border: 2px dashed var(--logo-primary);
            border-radius: 12px;
            padding: 1rem;
            background-color: rgba(74, 84, 173, 0.05);
        }

        /* === Avatars === */
        [data-testid="stChatMessageAvatarUser"] {
            background-color: var(--logo-white) !important;
            color: var(--logo-primary) !important;
        }
        [data-testid="stChatMessageAvatarAssistant"] {
            background-color: var(--logo-dark) !important;
            color: var(--logo-white) !important;
        }
    </style>
    """, unsafe_allow_html=True)
