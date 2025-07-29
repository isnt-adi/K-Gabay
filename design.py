import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(#002244, #3399ff) !important;
            padding: 1rem;
        }

        [data-testid="stAppViewContainer"] {
            background-color: #e6f0ff;
        }

        [data-testid="stMarkdownContainer"] h3 {
            font-family: 'Arial', sans-serif !important;
            color: white !important;
        }

        [data-testid="stMarkdownContainer"] h2 {
            font-family: 'Arial', sans-serif !important;
            color: #003366 !important;
        }

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

        [data-testid="stFileUploaderFile"],
        [data-testid="stWidgetLabel"],
        [data-testid="stAlertContentWarning"],
        [data-testid="stAlertContentInfo"],
        [data-testid="stAlertContentSuccess"],
        [data-testid="stFileUploader"] button {
            color: #EBEBEB !important;
            text-shadow:
                -0.25px -0.25px 0 gray,
                 0.25px -0.25px 0 gray,
                -0.25px  0.25px 0 gray,
                 0.25px  0.25px 0 gray !important;
        }
                
    </style>
    """, unsafe_allow_html=True)
