import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        /* HARSHER BLUE GRADIENT SIDEBAR */
        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #002244 0%, #002244 30%, #3399ff 100%) !important;
            padding: 1rem;
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }

        [data-testid="stSidebar"] .stFileUploader label,
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stTextInput label,
        [data-testid="stSidebar"] .stButton,
        [data-testid="stSidebar"] .stMarkdown {
            color: white !important;
        }

        [data-testid="stSidebar"] .stFileUploader button {
            color: white !important;
            background-color: #004488 !important;
            border: 1px solid white !important;
            font-weight: bold;
        }

        [data-testid="stSidebar"] input {
            color: white !important;
            background-color: #001122 !important;
            border: 1px solid #ffffff55 !important;
        }

        /* MAIN BACKGROUND */
        [data-testid="stAppViewContainer"] {
            background-color: #e6f0ff;
        }

        /* CHAT MESSAGES */
        [data-testid="stChatMessage"] {
            padding: 10px;
            border-radius: 10px; 
        }

        [data-testid="stChatMessage"]:nth-child(odd) {
            background-color: #ffffff !important;
            border: 2px solid #003366 !important;
        }

        [data-testid="stChatMessage"]:nth-child(odd) [data-testid="stChatMessageContent"] {
            color: #000000 !important;
            padding-left: 0.5rem;
        }

        [data-testid="stChatMessage"]:nth-child(even) {
            background-color: #003366 !important;
            border: none !important;
        }

        [data-testid="stChatMessage"]:nth-child(even) [data-testid="stChatMessageContent"] {
            color: white !important;
            padding-left: 0.5rem;
        }

        [data-testid="stChatMessageAvatarUser"] {
            color: #003366 !important;
            background-color: #ffffff !important;
        }

        [data-testid="stChatMessageAvatarAssistant"] {
            color: white !important;
            background-color: #003366;
        }
    </style>
    """, unsafe_allow_html=True)
