import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from set_configs import set_configuration

# --- Page Configuration ---
# set_configuration()
st.set_page_config(
    page_title="Agentic AI in Finance",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Dark Theme and beautiful divs ---
st.markdown("""
<style>
    /* Main container */
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    /* Card-like divs */
    .dark-card {
        background: #1e293b;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        border: 1px solid #334155;
    }
    /* Hero section */
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        margin-bottom: 10px;
    }
    #hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 1.8rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 40px;
        font-style: italic;
        font-weight: 600;
    }
    #hero-subtitle {
        font-size: 1.8rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 40px;
        font-style: italic;
        font-weight: 600;
    }
    /* Section headers */
    .section-header {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 20px;
        border-bottom: 2px solid #38bdf8;
        padding-bottom: 10px;
    }
    #section-header {
        font-size: 1.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 20px;
        border-bottom: 2px solid #38bdf8;
        padding-bottom: 10px;
    }
    .st-emotion-cache-16txtl3 {
        font-size: 1.1rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown('<p class="hero-title" id="hero-title">The Power of Agentic AI in Finance</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle" id="hero-subtitle">Automating complex financial analysis with intelligent, autonomous agents.</p>', unsafe_allow_html=True)

# --- What is Agentic AI? ---
st.markdown('<div class="dark-card">', unsafe_allow_html=True)
st.markdown('<p class="section-header" id="section-header">What is Agentic AI?</p>', unsafe_allow_html=True)
st.write("""
Agentic AI represents a paradigm shift from traditional AI models. Instead of executing predefined tasks, agentic systems can:
- **Reason and Plan:** Break down complex goals into smaller, manageable steps.
- **Self-Correct:** Evaluate their own performance and adjust their approach to improve results.
- **Use Tools:** Interact with external tools and APIs (like web search or data analysis libraries) to gather information and perform actions.
- **Collaborate:** Work together in teams, where each agent has a specialized role, to solve multifaceted problems.

In essence, you give them a goal, and they figure out how to achieve it.
""")
st.markdown('</div>', unsafe_allow_html=True)

# --- Agentic AI in Finance ---
st.markdown('<div class="dark-card">', unsafe_allow_html=True)
st.markdown('<p class="section-header" id="section-header">Applications in Finance</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.assetmg.info%2Fdims4%2Fdefault%2F98a3187%2F2147483647%2Fstrip%2Ftrue%2Fcrop%2F1000x563%2B0%2B44%2Fresize%2F1440x810!%2Fquality%2F90%2F%3Furl%3Dhttps%3A%252F%252Fk2-prod-in-investor-prod.s3.us-east-1.amazonaws.com%252Fbrightspot%252Fd9%252F99%252Ffc42e85f4d3ba2adba59c6ac35d8%252Fart-aipredictions.jpg&f=1&nofb=1&ipt=06c58c66b165a2200e0fe3ebee49dfe43660a18e219328f4abbb16acadb2b84d", use_container_width=True)
with col2:
    st.write("""
    In finance, where data is vast and decisions are critical, Agentic AI offers transformative capabilities:
    - **Automated Research:** An agent can be tasked to "find all recent news and analyst ratings for a stock," and it will autonomously search the web, summarize findings, and present a report.
    - **Dynamic Risk Assessment:** A team of agents can monitor market data, identify potential risks, and even suggest hedging strategies in real-time.
    - **Personalized Financial Advice:** Agents can analyze an individual's financial situation and goals to provide tailored investment advice.
    """)
st.markdown('</div>', unsafe_allow_html=True)

# --- Interactive Graph ---
st.markdown('<div class="dark-card">', unsafe_allow_html=True)
st.markdown('<p class="section-header" id="section-header">Simulating Agentic Workflow</p>', unsafe_allow_html=True)
df = pd.DataFrame({
    "Task": ["Goal Setting", "Information Gathering", "Data Analysis", "Strategy Formulation", "Report Generation"],
    "Time (minutes)": [1, 15, 10, 8, 5],
})
fig = go.Figure(go.Funnel(
    y=df["Task"],
    x=df["Time (minutes)"],
    textposition="inside",
    textinfo="value+percent initial",
    marker={"color": ["#38bdf8", "#34d399", "#fbbf24", "#f87171", "#c084fc"]}
))
fig.update_layout(
    title="Time Allocation in an Agentic Financial Analysis Workflow",
    template="plotly_dark"
)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Call to Action ---
st.markdown('<div class="dark-card" style="text-align:center;">', unsafe_allow_html=True)
st.markdown("### Experience It Yourself")
st.markdown("Navigate to the **Home** page from the sidebar to begin your journey with our Financial Analyst Agentic AI.")
if st.button("Go to Home", use_container_width=True):
    st.switch_page("pages/1_Home.py")
st.markdown('</div>', unsafe_allow_html=True)
