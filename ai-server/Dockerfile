# Use the official Python base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Introduce environment variables needed at runtime
ARG CORS_ORIGIN
ARG OPENAI_API_KEY
ARG COHERE_API_KEY
ARG FINSECURED_API_KEY
ARG QDRANT_URL
ARG PORT
ARG WORKERS

# Set environment variables from ARGs
ENV CORS_ORIGIN=${CORS_ORIGIN} 
ENV OPENAI_API_KEY=${OPENAI_API_KEY} 
ENV COHERE_API_KEY=${COHERE_API_KEY} 
ENV FINSECURED_API_KEY=${FINSECURED_API_KEY} 
ENV QDRANT_URL=${QDRANT_URL}
ENV PORT=${PORT}
ENV WORKERS=${WORKERS}

# Expose the port defined by the PORT environment variable
EXPOSE ${PORT}

# Run the FastAPI application using Gunicorn with Uvicorn workers
CMD gunicorn app:app --worker-class uvicorn.workers.UvicornWorker --workers $WORKERS --bind 0.0.0.0:$PORT --timeout 300
