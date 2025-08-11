# Use Python 3.10 slim image
FROM python:3.10-slim

WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    wkhtmltopdf \
    fontconfig \
    libxrender1 \
    libxext6 \
    libjpeg62-turbo \
    libpng16-16 \
    libssl3 \
    libstdc++6 \
    curl \
    && ln -sf /usr/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pysqlite3-binary
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir pysqlite3-binary

# Copy requirements & install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Copy sitecustomize.py into Python's site-packages so it runs at startup
COPY sitecustomize.py /usr/local/lib/python3.10/site-packages/

EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

CMD ["streamlit", "run", "FinoTron.py"]
