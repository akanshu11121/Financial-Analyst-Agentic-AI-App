import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
from backend.data_fetcher import fetch_history, plot_history_to_bytes
from backend.agent_client import call_agent_api
from backend.report import markdown_to_pdf_bytes
from components.buttons import styled_button, styled_download_button

# ---------------------------------------------------------------------
# Helper utilities (copied from app.py for modularity)
# ---------------------------------------------------------------------
DATA = Path("data")
DEFAULT_TICKERS = DATA / "tickers_sample.json"
TICKERS_FILE = DATA / "tickers.json"

def load_tickers():
    try:
        if TICKERS_FILE.exists():
            with open(TICKERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            with open(DEFAULT_TICKERS, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        return {"NSE": [], "BSE": []}

def build_options_and_map(tickers_data, cap=3000):
    options = []
    mapping = {}
    for exch in ["NSE", "BSE"]:
        for item in tickers_data.get(exch, [])[:cap]:
            label = f"{item['symbol']} — {item.get('name','')}"
            options.append(label)
            mapping[label] = {"symbol": item["symbol"], "exchange": exch}
    return options, mapping

def create_price_figure(df, symbol):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Close"))
    fig.update_layout(
        title=f"{symbol} — Price (close)",
        margin=dict(l=10, r=10, t=32, b=10),
        template="plotly_dark" if st.session_state.get("theme", "dark") == "dark" else "plotly_white",
        height=380
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(rangemode="tozero", showgrid=True)
    return fig

# ---------------------------------------------------------------------
# Analysis Page UI
# ---------------------------------------------------------------------
st.markdown("<div class='card'><div class='h-title' style='font-size: 2.5rem; font-weight: 800;'>Stock Analysis Dashboard</div>"
            "<div class='h-sub' style='font-size: 1.2rem; font-style: italic;'>Select a stock, set your constraints and run the Agentic AI to receive a detailed Markdown report.</div></div>", unsafe_allow_html=True)

tickers_data = load_tickers()
options, mapping = build_options_and_map(tickers_data)

# ---------------------------------------------------------------------
# Input Section
# ---------------------------------------------------------------------
def reset_analysis():
    for key in ["last_md", "last_pdf", "last_chart_bytes", "stock_label", "capital", "strategy", "risk", "news_impact"]:
        if key in st.session_state:
            del st.session_state[key]

with st.container():
    st.markdown("#### 1. Select Inputs")
    stock_label = st.selectbox("Select stock", options, index=0, help="Symbol — Company name", key="stock_label")
    capital = st.number_input("Capital (INR)", min_value=1000, step=1000, value=10000, format="%d", key="capital")
    strategy = st.selectbox(
        "Trading strategy",
        ["Swing", "Intraday", "Positional", "Delivery"],
        key="strategy",
        help="""
        - **Swing:** Holding stocks for a few days to weeks to profit from short-term price movements.
        - **Intraday:** Buying and selling stocks within the same trading day.
        - **Positional:** Holding stocks for several weeks to months based on long-term trends.
        - **Delivery:** Buying stocks and holding them in your Demat account for more than one day.
        """
    )
    risk = st.selectbox("Risk tolerance", ["Medium", "High", "Low"], key="risk")
    news_impact = st.checkbox("Consider News Impact", value=True, key="news_impact")

    # Real-time display of inputs
    st.markdown("---")
    st.markdown("#### 2. Review Selections (Real-time)")
    symbol = mapping[st.session_state.stock_label]["symbol"]
    exchange = mapping[st.session_state.stock_label]["exchange"]
    
    # Display selections in a table
    selection_data = {
        "Parameter": ["Symbol", "Exchange", "Capital (INR)", "Risk Tolerance", "Trading Strategy", "Consider News Impact"],
        "Value": [symbol, exchange, f"₹{int(st.session_state.capital):,}", st.session_state.risk, st.session_state.strategy, "Yes" if st.session_state.news_impact else "No"]
    }
    selection_df = pd.DataFrame(selection_data)
    st.table(selection_df)

    # Run and Reset buttons
    st.markdown("---")
    col1, col2, _ = st.columns([1, 1, 3])
    with col1:
        run = st.button("Run Analysis", use_container_width=True)
    with col2:
        if st.button("Reset", use_container_width=True, on_click=reset_analysis):
            st.experimental_rerun()

# ---------------------------------------------------------------------
# Output Section
# ---------------------------------------------------------------------
if run:
    st.markdown("#### 3. Analysis & Report")

# Results area
if run:
    # Clear previous results in session
    st.session_state.pop("last_md", None)
    st.session_state.pop("last_pdf", None)
    st.session_state.pop("last_chart_bytes", None)

    # Fetch history
    with st.spinner("Fetching price history..."):
        try:
            df = fetch_history(symbol, exchange, period="1y")
        except Exception as e:
            st.error(f"Price fetch failed: {e}")
            df = pd.DataFrame()

    if df.empty:
        st.error("No price history available for this symbol.")
    else:
        # Interactive chart
        fig = create_price_figure(df, symbol)
        st.plotly_chart(fig, use_container_width=True)

        # Also prepare PNG bytes for embedding in PDF
        try:
            chart_buf = plot_history_to_bytes(df, title=f"{symbol} price (1y)")
            if hasattr(chart_buf, "getvalue"):
                st.session_state["last_chart_bytes"] = chart_buf.getvalue()
            else:
                st.session_state["last_chart_bytes"] = chart_buf.read()
        except Exception:
            st.session_state["last_chart_bytes"] = None

    # Prepare payload
    payload = {
        "stock_symbol": symbol,
        "exchange": exchange,
        "capital": int(capital),
        "risk_tolerance": risk,
        "strategy": strategy,
        "news_impact": bool(news_impact),
        "price_summary": {
            "last_close": float(df["Close"].iloc[-1]) if not df.empty else None,
            "mean_30d": float(df["Close"].tail(30).mean()) if len(df) >= 30 else None
        }
    }

    # Call Agentic API
    with st.spinner("Calling Agentic AI..."):
        try:
            resp = call_agent_api(payload)
            md = resp.get("markdown_report", "")
            ov = resp.get("stock_overview", "")
            if not md:
                md = "## No report returned from Agent.\n"
        except Exception as e:
            md = f"# Error\nAgent API call failed: {e}"
            ov = f"# Error\nAgent API call failed: {e}"
            st.error("Agent API call failed: see report for details.")

    # Store markdown in session and show expandable report
    st.session_state["last_md"] = md
    st.session_state["last_ov"] = ov
    st.subheader("AI Report")
    st.markdown("The AI-generated report is shown below. Use the download buttons to export MD or PDF.")
    with st.expander("View full report (Markdown)", expanded=False):
        st.markdown(md, unsafe_allow_html=True)

    # Downloads
    md_bytes = md.encode("utf-8")
    now_stamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
    md_filename = f"{symbol}_{now_stamp}.md"
    pdf_filename = f"{symbol}_{now_stamp}.pdf"

    col_dl1, col_dl2, _ = st.columns([1, 1, 3])
    with col_dl1:
        styled_download_button("Download .md", data=md_bytes, file_name=md_filename, mime="text/markdown")
    with col_dl2:
        try:
            pdf_bytes = markdown_to_pdf_bytes(md, ov, symbol=symbol,
                                              chart_bytes=st.session_state.get("last_chart_bytes"),
                                              capital=int(st.session_state.capital),
                                              last_close=payload["price_summary"].get("last_close"))
            st.session_state["last_pdf"] = pdf_bytes
            styled_download_button("Download .pdf", data=pdf_bytes, file_name=pdf_filename, mime="application/pdf")
        except Exception as e:
            st.warning("PDF generation failed (server may lack HTML engine). You can still download the .md file.")
            st.write(f"Debug: {e}")

    # Small post-run tips
    st.info("Tip: Review the chart and the risk sections carefully before trading. Use downloads to archive.")

else:
    st.markdown("<div class='card'><b>Ready to analyze</b> — choose a stock and press **Run analysis**.</div>", unsafe_allow_html=True)
