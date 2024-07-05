# Use Python Alpine image for a smaller base
FROM python:alpine

# Set the working directory
WORKDIR /code

RUN apk add --no-cache rust cargo

# Copy the requirements file to the working directory
COPY ./requirements.txt .

# Upgrade pip and install Python packages defined in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY ./app ./app

# Use ARG to define variables that will be used only during the build
ARG CORS_ORIGIN
ARG OPENAI_API_KEY
ARG COHERE_API_KEY
ARG FINSECURED_API_KEY
ARG QDRANT_URL
ARG PORT
ARG WORKERS

# Set environment variables from the build arguments
ENV CORS_ORIGIN=${CORS_ORIGIN} \
    OPENAI_API_KEY=${OPENAI_API_KEY} \
    COHERE_API_KEY=${COHERE_API_KEY} \
    FINSECURED_API_KEY=${FINSECURED_API_KEY} \
    QDRANT_URL=${QDRANT_URL} \
    PORT=${PORT} \
    WORKERS=${WORKERS}

# Expose the port defined by the PORT environment variable
EXPOSE ${PORT}

CMD gunicorn app:app --worker-class uvicorn.workers.UvicornWorker --workers $WORKERS --bind 0.0.0.0:$PORT --timeout 300