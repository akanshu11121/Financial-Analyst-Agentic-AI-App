# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for wkhtmltopdf
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sqlite3 \
        libsqlite3-dev \
        wkhtmltopdf \
        fontconfig \
        libxrender1 \
        libxext6 \
        libfontconfig1 \
        libjpeg62-turbo \
        libpng16-16 \
        libssl3 \
        libstdc++6 \
        build-essential \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Verify sqlite3 version
RUN sqlite3 --version

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the working directory
COPY . .

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT 8501
ENV STREAMLIT_SERVER_HEADLESS true

# Run FinoTron.py when the container launches
CMD ["streamlit", "run", "FinoTron.py"]
