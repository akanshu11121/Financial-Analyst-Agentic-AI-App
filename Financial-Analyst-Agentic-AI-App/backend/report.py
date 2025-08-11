# backend/report.py
import base64
import io
from datetime import datetime
from typing import Optional
import markdown as md_lib
from pathlib import Path

# Try preferred HTML->PDF engines in order
# WeasyPrint (pure python but system libs required)
try:
    from weasyprint import HTML, CSS
    _WEASYPRINT_AVAILABLE = True
except Exception:
    _WEASYPRINT_AVAILABLE = False

# pdfkit (wkhtmltopdf) fallback
try:
    import pdfkit
    _PDFKIT_AVAILABLE = True
except Exception:
    _PDFKIT_AVAILABLE = False

# fallback to simple ReportLab-based pdf (less styled)
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    _REPORLAB_AVAILABLE = True
except Exception:
    _REPORLAB_AVAILABLE = False

# ---------- Utilities ----------

def _img_bytes_to_data_uri(img_bytes: bytes, mime: str = "image/png") -> str:
    """Encode image bytes as data URI for inline embedding."""
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def _safe_read_logo(logo_path: Optional[str]) -> Optional[str]:
    if not logo_path:
        return None
    p = Path(logo_path)
    if not p.exists():
        return None
    with open(p, "rb") as f:
        return _img_bytes_to_data_uri(f.read())

# ---------- HTML Template & CSS ----------

_BASE_CSS = """
@page { size: A4; margin: 28mm 20mm 20mm 20mm; }
body {
  font-family: "Inter", "Arial", sans-serif;
  color: #111;
  background: #fff;
  line-height: 1.45;
  font-size: 12px;
}
.header {
  display:flex;
  align-items:center;
  justify-content:space-between;
  border-bottom: 1px solid #e6e6e6;
  padding-bottom: 10px;
  margin-bottom: 10px;
}
.brand {
  display:flex;
  align-items:center;
}
.logo {
  width:64px; height:64px; object-fit:contain; margin-right:12px;
}
.title {
  font-size:18px; font-weight:700;
}
.meta {
  text-align:right;
  font-size:11px;
  color:#555;
}
.section {
  margin-top:14px;
  margin-bottom:8px;
}
.h1 { font-size:16px; font-weight:700; margin-bottom:6px; }
.h2 { font-size:13px; font-weight:700; margin-bottom:6px; color:#222; }
.card {
  border: 1px solid #eaeaea;
  padding:10px;
  border-radius:6px;
  background: #fbfbfb;
}
.key-metrics {
  display:flex;
  gap:12px;
  margin-top:8px;
  flex-wrap:wrap;
}
.metric {
  background:#fff;
  padding:8px 10px;
  border-radius:6px;
  border:1px solid #eee;
  min-width:110px;
  text-align:center;
}
.chart {
  margin-top:10px;
  text-align:center;
}
.table {
  width:100%;
  border-collapse: collapse;
  margin-top:8px;
}
.table th, .table td {
  border: 1px solid #ddd;
  padding:8px;
  font-size:12px;
}
.table th {
  background:#f5f7fa;
  text-align:left;
}
.footer {
  margin-top:18px;
  font-size:10px;
  color:#666;
  border-top:1px solid #eee;
  padding-top:8px;
  text-align:right;
}
.page-break { page-break-after: always; }
"""

_HTML_TEMPLATE = """
<html>
  <head>
    <meta charset="utf-8" />
    <style>{css}</style>
  </head>
  <body>
    <div class="header">
      <div class="brand">
        {logo_html}
        <div>
          <div class="title">Comprehensive Risk Analysis Report</div>
          <div style="font-size:12px;color:#444;">{report_subtitle}</div>
        </div>
      </div>
      <div class="meta">
        <div><strong>{symbol}</strong> &middot; {exchange}</div>
        <div>{as_of}</div>
      </div>
    </div>

    <div class="section">
      <div class="h2">Overview</div>
      <div class="card">
        {overview_html}
      </div>
    </div>

    <div class="section">
      <div class="h2">Key Metrics</div>
      <div class="card key-metrics">
        {key_metrics_html}
      </div>
    </div>

    <div class="section chart">
      {chart_html}
    </div>

    <div class="section">
      <div class="h2">Detailed Analysis</div>
      {content_html}
    </div>

    <div class="section">
      <div class="h2">Risk Summary Table</div>
      {risk_table_html}
    </div>

    <div class="footer">
      Generated on {as_of_long} &nbsp;|&nbsp; Financial Analyst App
    </div>
  </body>
</html>
"""

# ---------- Converters ----------

def markdown_to_html(markdown_text: str) -> str:
    """
    Converts a Markdown string to an HTML string.
    Uses the 'python-markdown' library with 'extra' and 'sane_lists' extensions for table support.

    Args:
        markdown_text (str): The Markdown content to convert.

    Returns:
        str: The resulting HTML content.
    """
    html = md_lib.markdown(markdown_text, extensions=["extra", "sane_lists"])
    return html

def build_key_metrics_html(metrics: dict) -> str:
    """
    Builds an HTML snippet for displaying key metrics in styled boxes.

    Args:
        metrics (dict): A dictionary of metric labels to their values.

    Returns:
        str: An HTML string containing the styled metric boxes.
    """
    parts = []
    for k, v in metrics.items():
        parts.append(f'<div class="metric"><div style="font-weight:700">{k}</div><div style="margin-top:4px">{v}</div></div>')
    return "\n".join(parts)

def build_risk_table_html(risk_summary: list) -> str:
    """
    Builds an HTML table from a list of risk summary dictionaries.

    Args:
        risk_summary (list): A list of dictionaries, each representing a row in the risk table.
                             Expected keys: 'area', 'scenario', 'risk', 'mitigation'.

    Returns:
        str: An HTML string representing the risk summary table.
    """
    rows_html = []
    header = "<table class='table'><thead><tr><th>Area</th><th>Scenario</th><th>Risk</th><th>Mitigation</th></tr></thead><tbody>"
    for r in risk_summary:
        rows_html.append("<tr><td>{area}</td><td>{scenario}</td><td>{risk}</td><td>{mitigation}</td></tr>".format(
            area=r.get("area", ""),
            scenario=r.get("scenario", ""),
            risk=r.get("risk", ""),
            mitigation=r.get("mitigation", "")
        ))
    footer = "</tbody></table>"
    return header + "\n".join(rows_html) + footer

# ---------- Public API ----------

def assemble_html_report(
    markdown_report: str,
    overview_report: str,
    symbol: str,
    exchange: str = "NSE",
    chart_bytes: Optional[bytes] = None,
    logo_path: Optional[str] = None,
    capital: Optional[int] = None,
    last_close: Optional[float] = None,
    extra_metrics: Optional[dict] = None,
    risk_summary: Optional[list] = None
) -> str:
    """
    Assembles a complete, styled HTML report from various components.

    Args:
        markdown_report (str): The main report body in Markdown format.
        symbol (str): The stock symbol.
        exchange (str, optional): The stock exchange. Defaults to "NSE".
        chart_bytes (Optional[bytes], optional): PNG image bytes for the price chart. Defaults to None.
        logo_path (Optional[str], optional): Filesystem path to a logo image. Defaults to None.
        capital (Optional[int], optional): The investment capital. Defaults to None.
        last_close (Optional[float], optional): The last closing price of the stock. Defaults to None.
        extra_metrics (Optional[dict], optional): A dictionary of additional metrics. Defaults to None.
        risk_summary (Optional[list], optional): A list of dictionaries for the risk summary table. Defaults to None.

    Returns:
        str: The final, styled HTML report as a string.
    """

    logo_data_uri = _safe_read_logo(logo_path)
    logo_html = f'<img class="logo" src="{logo_data_uri}"/>' if logo_data_uri else ""

    overview_html = markdown_to_html(overview_report) #""
    # extract first paragraphs of markdown as overview (naive)
    # better: user can pass a short overview separately. For now take first 2 paragraphs.
    md_lines = markdown_report.strip().splitlines()
    para_lines = []
    count = 0
    for line in md_lines:
        if line.strip() == "" and para_lines:
            count += 1
        if count >= 2:
            break
        para_lines.append(line)
    # overview_html = "" #"<br/>".join(para_lines[:20])
    content_html = markdown_to_html(markdown_report)

    # chart
    chart_html = ""
    if chart_bytes:
        chart_data = _img_bytes_to_data_uri(chart_bytes, mime="image/png")
        chart_html = f'<img src="{chart_data}" style="max-width:100%; height:auto; border:1px solid #eee; border-radius:6px;" />'

    # key metrics
    metrics = {"Symbol": symbol}
    if exchange:
        metrics["Exchange"] = exchange
    if capital is not None:
        metrics["Capital (INR)"] = f"₹{int(capital):,}"
    if last_close is not None:
        metrics["Last close"] = f"₹{last_close:.2f}"
    if extra_metrics:
        metrics.update(extra_metrics)
    key_metrics_html = build_key_metrics_html(metrics)

    # risk summary table
    risk_html = ""
    if risk_summary:
        risk_html = build_risk_table_html(risk_summary)
    else:
        # attempt to extract headings like "1. Market Risk" etc and build mini table (naive)
        risk_html = "<div class='card'>See detailed analysis above.</div>"

    html = _HTML_TEMPLATE.format(
        css=_BASE_CSS,
        logo_html=logo_html,
        report_subtitle=f"{symbol} — Risk Analysis",
        symbol=symbol,
        exchange=exchange,
        as_of=datetime.utcnow().strftime("%Y-%m-%d"),
        as_of_long=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        overview_html=overview_html,
        key_metrics_html=key_metrics_html,
        chart_html=chart_html,
        content_html=content_html,
        risk_table_html=risk_html
    )
    return html

def html_to_pdf_bytes(html: str, base_url: Optional[str] = None, css_string: Optional[str] = None) -> bytes:
    """
    Converts an HTML string to PDF bytes using the best available engine.
    It tries WeasyPrint, then pdfkit (wkhtmltopdf), and finally a simple ReportLab fallback.

    Args:
        html (str): The HTML content to convert.
        base_url (Optional[str], optional): The base URL for resolving relative paths in the HTML. Defaults to None.
        css_string (Optional[str], optional): An additional CSS string to apply. Defaults to None.

    Raises:
        RuntimeError: If no suitable HTML-to-PDF conversion engine is found.

    Returns:
        bytes: The generated PDF content as bytes.
    """
    # 1) WeasyPrint
    if _WEASYPRINT_AVAILABLE:
        try:
            extra_css = CSS(string=css_string) if css_string else None
            html_obj = HTML(string=html, base_url=base_url)
            out = html_obj.write_pdf(stylesheets=[extra_css] if extra_css else None)
            return out
        except Exception as e:
            # try next
            print("WeasyPrint conversion failed:", e)

    # 2) pdfkit (wkhtmltopdf)
    if _PDFKIT_AVAILABLE:
        try:
            # default options: enable local file access, reasonable margins
            options = {
                "enable-local-file-access": None,
                "margin-top": "10mm",
                "margin-right": "10mm",
                "margin-bottom": "10mm",
                "margin-left": "10mm",
                "encoding": "UTF-8"
            }
            out = pdfkit.from_string(html, False, options=options)  # returns bytes
            return out
        except Exception as e:
            print("pdfkit conversion failed:", e)

    # 3) ReportLab fallback (very plain)
    if _REPORLAB_AVAILABLE:
        try:
            # Very naive: strip tags and place paragraphs.
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text("\n")
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
            styles = getSampleStyleSheet()
            story = []
            for line in text.splitlines():
                if not line.strip():
                    story.append(Spacer(1,6))
                else:
                    story.append(Paragraph(line.replace("**",""), styles['BodyText']))
            doc.build(story)
            buffer.seek(0)
            return buffer.read()
        except Exception as e:
            print("ReportLab fallback failed:", e)

    raise RuntimeError("No available HTML->PDF engine: install WeasyPrint or wkhtmltopdf (pdfkit), or ensure ReportLab is available.")

# ---------- convenience wrapper ----------

def markdown_to_pdf_bytes(markdown_text: str,
                          overview_text: str,
                          symbol: str,
                          exchange: str = "NSE",
                          chart_bytes: Optional[bytes] = None,
                          logo_path: Optional[str] = None,
                          capital: Optional[int] = None,
                          last_close: Optional[float] = None,
                          extra_metrics: Optional[dict] = None,
                          risk_summary: Optional[list] = None) -> bytes:
    """
    A high-level wrapper to convert a Markdown report directly to a styled PDF.
    This function assembles the HTML and then converts it to PDF bytes.

    Args:
        markdown_text (str): The main report body in Markdown format.
        symbol (str): The stock symbol.
        exchange (str, optional): The stock exchange. Defaults to "NSE".
        chart_bytes (Optional[bytes], optional): PNG image bytes for the price chart. Defaults to None.
        logo_path (Optional[str], optional): Filesystem path to a logo image. Defaults to None.
        capital (Optional[int], optional): The investment capital. Defaults to None.
        last_close (Optional[float], optional): The last closing price of the stock. Defaults to None.
        extra_metrics (Optional[dict], optional): A dictionary of additional metrics. Defaults to None.
        risk_summary (Optional[list], optional): A list of dictionaries for the risk summary table. Defaults to None.

    Returns:
        bytes: The generated PDF content as bytes.
    """
    html = assemble_html_report(
        markdown_report=markdown_text,
        overview_report=overview_text,
        symbol=symbol,
        exchange=exchange,
        chart_bytes=chart_bytes,
        logo_path=logo_path,
        capital=capital,
        last_close=last_close,
        extra_metrics=extra_metrics,
        risk_summary=risk_summary
    )
    pdf = html_to_pdf_bytes(html, css_string=_BASE_CSS)
    return pdf
