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

# Compile SQLite 3.45+ from source to satisfy Chroma requirement
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3450000.tar.gz && \
    tar xvfz sqlite-autoconf-3450000.tar.gz && \
    cd sqlite-autoconf-3450000 && \
    ./configure && make && make install && \
    cd .. && rm -rf sqlite-autoconf-3450000*

# Verify SQLite version
RUN sqlite3 --version
RUN python -c "import sqlite3; print('Python sqlite3:', sqlite3.sqlite_version)"

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

CMD ["streamlit", "run", "FinoTron.py"]
