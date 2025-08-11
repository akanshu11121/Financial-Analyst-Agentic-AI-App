FROM python:3.10-slim

WORKDIR /app

# Install build tools & dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget build-essential zlib1g-dev libssl-dev libbz2-dev libreadline-dev \
    libsqlite3-dev tk-dev libgdbm-dev libnss3-dev libffi-dev liblzma-dev \
    uuid-dev wkhtmltopdf fontconfig libxrender1 libxext6 \
    libjpeg62-turbo libpng16-16 curl \
    && rm -rf /var/lib/apt/lists/*

# Build SQLite 3.45+
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3450000.tar.gz && \
    tar xvfz sqlite-autoconf-3450000.tar.gz && \
    cd sqlite-autoconf-3450000 && \
    ./configure --prefix=/usr/local && make && make install && \
    cd .. && rm -rf sqlite-autoconf-3450000*

# Build Python 3.10 from source linked to new SQLite
RUN wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz && \
    tar xzf Python-3.10.14.tgz && cd Python-3.10.14 && \
    ./configure --enable-optimizations && make && make install && \
    cd .. && rm -rf Python-3.10.14*

# Verify SQLite in Python
RUN python3 -c "import sqlite3; print(sqlite3.sqlite_version)"

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

CMD ["streamlit", "run", "FinoTron.py"]
