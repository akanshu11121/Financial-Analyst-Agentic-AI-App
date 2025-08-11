FROM python:3.10-slim

WORKDIR /app

# Install system packages and build-essential
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget build-essential wkhtmltopdf fontconfig libxrender1 \
    libxext6 libjpeg62-turbo libpng16-16 libssl3 libstdc++6 curl \
    python3-dev libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install latest SQLite ≥3.35.0 from source
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3450000.tar.gz \
    && tar xvfz sqlite-autoconf-3450000.tar.gz \
    && cd sqlite-autoconf-3450000 \
    && ./configure --prefix=/usr/local \
    && make -j$(nproc) \
    && make install \
    && cd .. \
    && rm -rf sqlite-autoconf-3450000*

# Reinstall Python’s sqlite3 extension to use the new SQLite
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --force-reinstall pysqlite3-binary

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
