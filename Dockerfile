FROM python:3.10-alpine

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    wget \
    tar \
    wkhtmltopdf \
    fontconfig \
    libxrender \
    libxext \
    jpeg \
    libpng \
    openssl \
    g++ \
    make \
    curl

# Build SQLite from source (3.45.3 is just an example - use latest stable)
ENV SQLITE_VERSION=3.45.3
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3450300.tar.gz && \
    tar xzf sqlite-autoconf-3450300.tar.gz && \
    cd sqlite-autoconf-3450300 && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    cd .. && rm -rf sqlite-autoconf-3450300*

# Verify SQLite versions
RUN sqlite3 --version
RUN python -c "import sqlite3; print('Python sqlite3 version:', sqlite3.sqlite_version)"

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

CMD ["streamlit", "run", "FinoTron.py"]