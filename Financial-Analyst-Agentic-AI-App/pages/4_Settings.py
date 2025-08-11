import streamlit as st
import os

st.set_page_config(layout="wide")

st.markdown("<div class='card'><div class='h-title' style='font-size: 2.5rem; font-weight: 800;'>Settings</div>"
            "<div class='h-sub' style='font-size: 1.2rem; font-style: italic;'>Configure environment variables and agent endpoints.</div></div>", unsafe_allow_html=True)

st.markdown("---")

st.subheader("Agent Configuration")

agent_api_url = st.text_input("Agent API URL", value=os.environ.get("AGENT_API_URL", ""), placeholder="http://localhost:8000")
agent_api_key = st.text_input("Agent API Key", value=os.environ.get("AGENT_API_KEY", ""), type="password", placeholder="Enter your API key")

if st.button("Save Configuration"):
    os.environ["AGENT_API_URL"] = agent_api_url
    os.environ["AGENT_API_KEY"] = agent_api_key
    st.success("Configuration saved successfully!")

st.markdown("---")

st.subheader("PDF Generation Setup")
st.markdown("""
To enable polished PDF generation, you need to install `wkhtmltopdf`.

**Installation Instructions:**

*   **Windows:** Download the installer from the [official website](https://wkhtmltopdf.org/downloads.html) and add the `bin` folder to your system's PATH.
*   **macOS:** Install using Homebrew: `brew install --cask wkhtmltopdf`
*   **Linux (Debian/Ubuntu):** `sudo apt-get install wkhtmltopdf`

After installation, ensure that `wkhtmltopdf` is accessible from your system's PATH.
""")

st.markdown("---")
st.caption("© Financial Analyst • Agentic AI integration demo")
