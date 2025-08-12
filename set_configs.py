import os
import streamlit as st

def set_configuration():
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["OPENAI_MODEL_NAME"] = st.secrets["OPENAI_MODEL_NAME"]
    os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]