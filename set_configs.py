import os
import streamlit as st

def set_configuration():
    os.environ["OPENAI_API_KEY"] = st.secrets["openai"]["api_key"]
    os.environ["OPENAI_MODEL_NAME"] = st.secrets["openai"]["model_name"]
    os.environ["SERPER_API_KEY"] = st.secrets["serper"]["api_key"]