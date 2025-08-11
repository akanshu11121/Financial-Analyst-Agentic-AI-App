# Use Python 3.10 slim image
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (minimal set)
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
    curl \
    && rm -rf /var/lib/apt/lists/*

# Compile and install SQLite 3.45+ from source
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3450000.tar.gz && \
    tar xzf sqlite-autoconf-3450000.tar.gz && \
    cd sqlite-autoconf-3450000 && \
    ./configure --prefix=/usr/local && \
    make && make install && \
    cd .. && rm -rf sqlite-autoconf-3450000*

# Make sure the new SQLite is found first
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"
ENV PATH="/usr/local/bin:${PATH}"

# Rebuild Python's sqlite3 module against the new SQLite
RUN apt-get update && apt-get install -y --no-install-recommends python3-dev && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    cd /usr/local/lib/python3.10 && \
    python3 -m pip uninstall -y pysqlite3-binary pysqlite3 || true && \
    python3 -m pip install pysqlite3-binary --no-cache-dir

# Verify SQLite version used by Python
RUN sqlite3 --version && \
    python -c "import sqlite3; print('Python sqlite3:', sqlite3.sqlite_version)"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

CMD ["streamlit", "run", "FinoTron.py"]
