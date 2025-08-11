FROM python:3.10-alpine

WORKDIR /app

RUN apk add --no-cache \
    sqlite \
    sqlite-dev \
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

RUN sqlite3 --version
RUN python -c "import sqlite3; print('Python sqlite3:', sqlite3.sqlite_version)"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
a
EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

CMD ["streamlit", "run", "FinoTron.py"]