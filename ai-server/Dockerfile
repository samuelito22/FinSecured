# Use a slim Python image
FROM python:3.11-slim

# Set environment variables
ENV PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables from build arguments
ARG CORS_ORIGIN
ARG OPENAI_API_KEY
ARG COHERE_API_KEY
ARG FINSECURED_API_KEY
ARG QDRANT_URL
ARG PORT
ARG WORKERS
ENV CORS_ORIGIN=${CORS_ORIGIN} \
    OPENAI_API_KEY=${OPENAI_API_KEY} \
    COHERE_API_KEY=${COHERE_API_KEY} \
    FINSECURED_API_KEY=${FINSECURED_API_KEY} \
    QDRANT_URL=${QDRANT_URL} \
    PORT=${PORT} \
    WORKERS=${WORKERS}

# Expose the application port
EXPOSE $PORT

# Run the FastAPI application using Gunicorn with Uvicorn workers
CMD gunicorn app:app --worker-class uvicorn.workers.UvicornWorker --workers $WORKERS --bind 0.0.0.0:$PORT --timeout 300

# Optionally, add a non-root user for security
# RUN addgroup --system appgroup && adduser --system --no-create-home --ingroup appgroup appuser
# USER appuser
