FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
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

# Upgrade SQLite to latest (optional)
RUN apt-get install -y sqlite3 libsqlite3-dev && sqlite3 --version

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

CMD ["python", "app.py"]
