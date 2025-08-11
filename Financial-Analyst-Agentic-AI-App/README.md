# FinoTron - AI-Powered Financial Analyst

FinoTron is an interactive, AI-powered stock analysis platform for the Indian stock market (NSE & BSE). It features a modular design, a beautiful and intuitive user interface, and a powerful Agentic AI backend for generating detailed financial reports.

## ✨ Features

- **Modular & Scalable:** Built with a multipage Streamlit structure, separating pages, components, and backend logic for easy maintenance and extension.
- **Beautiful Homepage:** A welcoming landing page with market trends, key stats, and a financial terms word cloud.
- **Interactive Analysis:** A dedicated analysis page to select stocks, set investment parameters (capital, risk, strategy), and run the AI agent.
- **Real-time Input Display:** Instantly see your selected parameters before running the analysis.
- **Modern UI:** A clean UI with custom styling for a better user experience.
- **PDF & Markdown Downloads:** Download the AI-generated reports in both PDF and Markdown formats with a single click.
- **Configuration Page:** Easily configure API keys and other settings from the UI.
- **About the Author:** A dedicated page with information about the developer.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- `pip` for package management

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/financial-analyst-agentic-ai.git
    cd financial-analyst-agentic-ai
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys:**
    You can set your API keys in the `Settings` page of the application. You will need an `OPENAI_API_KEY` and a `SERPER_API_KEY`.

4.  **(Optional) For PDF Generation:**
    To enable high-quality PDF exports, install `wkhtmltopdf`:
    -   **Ubuntu/Debian:** `sudo apt-get install wkhtmltopdf`
    -   **macOS (with Homebrew):** `brew install wkhtmltopdf`
    -   **Windows:** Download from the [official site](https://wkhtmltopdf.org/downloads.html) and add to PATH.

### Running the App

Execute the following command in your terminal:
```bash
streamlit run FinoTron.py
```
The application will open in your default web browser.

## 📂 Project Structure

```
/
├── FinoTron.py             # Main Streamlit app (global config & styles)
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── set_configs.py          # Environment variable setup
├── assets/                 # Static assets (images, etc.)
├── backend/                # Backend logic
│   ├── agent_client.py     # Agentic AI client (CrewAI)
│   ├── data_fetcher.py     # Fetches stock data
│   └── report.py           # Generates PDF/Markdown reports
├── components/             # Reusable Streamlit UI components
│   └── buttons.py          # Styled buttons
├── data/                   # Data files (tickers, etc.)
│   ├── tickers.json
│   └── tickers_sample.json
├── pages/                  # Streamlit multipage app pages
│   ├── 1_Home.py
│   ├── 2_Analysis.py
│   ├── 3_About.py
│   └── 4_Settings.py
└── scripts/                # Utility scripts
    └── fetch_tickers.py
```

## 👨‍💻 Author

-   **Akanshu Sonkar**
    -   [LinkedIn](https://www.linkedin.com/in/akanshu11121/)
    -   [GitHub](https://github.com/akanshu11121)
    -   [Medium](https://medium.com/@akanshu11121)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs, feature requests, or improvements.

## 📄 License

This project is licensed under the MIT License.
