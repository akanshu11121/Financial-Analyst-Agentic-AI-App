FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wkhtmltopdf \
        fontconfig \
        libxrender1 \
        libxext6 \
        libjpeg62-turbo \
        libpng16-16 \
        libssl3 \
        libstdc++6 \
        build-essential \
        curl && \
    rm -rf /var/lib/apt/lists/*

RUN sqlite3 --version
RUN python -c "import sqlite3; import sys; print('Python sqlite3:', sqlite3.sqlite_version)"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

CMD ["streamlit", "run", "FinoTron.py"]
