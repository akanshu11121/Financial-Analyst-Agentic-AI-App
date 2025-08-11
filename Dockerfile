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
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pysqlite3-binary for Chroma compatibility
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir pysqlite3-binary

# Verify Python's sqlite3 is actually using pysqlite3
RUN python -c "import sys, sqlite3; print('Python sqlite3 version:', sqlite3.sqlite_version)"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

CMD ["streamlit", "run", "FinoTron.py"]
