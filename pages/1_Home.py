import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from wordcloud import WordCloud
import random

# --- Page Configuration ---
st.set_page_config(page_title="Home", layout="wide")

# --- Custom CSS for beautiful divs and reflections ---
st.markdown("""
<style>
.card-reflect {
    background: #ffffff;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: transform 0.3s;
    margin-bottom: 20px;
    -webkit-box-reflect: below 1px linear-gradient(transparent, transparent, #00000008);
}
.card-reflect:hover {
    transform: translateY(-5px);
}
.hero-title {
    font-size: 8rem;
    font-weight: 800;
    color: #1a237e;
    text-align: center;
    margin-bottom: 10px;
}
#special-title {
    font-size: 4.6rem;
    font-weight: 800;
    color: #dacabe;
    text-align: center;
    margin-bottom: 10px;
}
.hero-subtitle {
    font-size: 1.6rem;
    color: #546e7a;
    text-align: center;
    margin-bottom: 30px;
    font-style: italic;
    font-weight: 600;
}
#special-subtitle {
    font-size: 1.4rem;
    color: #deafbc;
    text-align: center;
    margin-bottom: 30px;
    font-style: italic;
    font-weight: 600;
}
.section-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #cfbead;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown('<p class="hero-title" id="special-title">Financial Analyst Agentic AI</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle" id="special-subtitle">Your AI-powered partner for smarter investment decisions in the Indian market.</p>', unsafe_allow_html=True)

# --- Quick Stats in styled divs ---
st.markdown('<div class="card-reflect">', unsafe_allow_html=True)
st.markdown('<p class="section-title">📊 Key Market Indicators</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📈 NSE Tickers", "2,160", delta="1.2%", delta_color="normal")
with col2:
    st.metric("📉 BSE Tickers", "5,246", delta="-0.5%", delta_color="inverse")
with col3:
    st.metric("📅 Last Update", "2025-08-11")
st.markdown('</div>', unsafe_allow_html=True)

# --- Interactive Market Trends Chart ---
st.markdown('<div class="card-reflect">', unsafe_allow_html=True)
st.markdown('<p class="section-title">📈 Interactive Market Trends Overview</p>', unsafe_allow_html=True)
df = pd.DataFrame({
    "Date": pd.to_datetime(pd.date_range(start="2025-07-01", periods=30)),
    "NIFTY 50": [random.uniform(18500, 19500) for _ in range(30)],
    "SENSEX": [random.uniform(62000, 65000) for _ in range(30)]
})
df = df.set_index("Date")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df["NIFTY 50"], mode='lines+markers', name='NIFTY 50', line=dict(color='#ff5722')))
fig.add_trace(go.Scatter(x=df.index, y=df["SENSEX"], mode='lines+markers', name='SENSEX', line=dict(color='#2196f3'), visible='legendonly'))
fig.update_layout(
    title="NIFTY 50 vs SENSEX Interactive Chart",
    xaxis_title="Date",
    yaxis_title="Index Value",
    legend_title="Indices",
    template="plotly_white",
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Financial Terms Word Cloud ---
st.markdown('<div class="card-reflect">', unsafe_allow_html=True)
st.markdown('<p class="section-title">💬 Key Financial Terms</p>', unsafe_allow_html=True)
terms = "Stocks Bonds Investment Portfolio Dividend IPO Index ETF MutualFunds Derivatives MarketCap Valuation BullMarket BearMarket InterestRate Inflation GDP Growth Earnings Revenue"
wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="viridis").generate(terms)
st.image(wordcloud.to_array(), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Call to Action ---
st.markdown('<div class="card-reflect" style="text-align:center;">', unsafe_allow_html=True)
st.markdown('<p class="section-title">🚀 Ready to Dive Deeper?</p>', unsafe_allow_html=True)
st.markdown("Navigate to the **Analysis** page from the sidebar to get detailed AI-driven insights on individual stocks.")
if st.button("Go to Analysis", use_container_width=True):
    st.switch_page("pages/2_Analysis.py")
st.markdown('</div>', unsafe_allow_html=True)
