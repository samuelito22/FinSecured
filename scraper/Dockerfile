# Use Ubuntu 24.04 as the base image
FROM ubuntu:24.04

# Set working directory in the Docker image
WORKDIR /app

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    python3-venv \
    cron \
 && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt /app/
RUN python3 -m venv venv \
 && . venv/bin/activate \
 && python -m spacy download en_core_web_sm \
 && pip3 install -r requirements.txt \
 && curl -fsSL https://ollama.com/install.sh | sh \
 && ollama pull llama3 
# Copy the rest of the application
COPY . /app

# Set environment variables
ENV AWS_ACCESS_KEY=AKIA2UC3E5PLSMW37JVG \
    AWS_SECRET_ACCESS_KEY=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 \
    MAILERSEND_API_KEY=mlsn.2b5f4cedea8238f179dac85c277fab2e49ca37f5ea02888d5054a3b4441d8fbc \
    SENDER_EMAIL=impex.compliance@outlook.com \
    RECIPIENT_EMAIL=impex.compliance@outlook.com \
    DB_PSQL_HOST=finsecured-db \
    DB_PSQL_PORT=5432 \
    DB_PSQL_USER=postgres \
    DB_PSQL_PASSWORD=20032001Orte

# Setup the database and make the start script executable
RUN chmod +x /app/start.sh \
 && echo "0 0 */1 * * /app/start.sh >> /app/cron.log 2>&1" > /etc/cron.d/mycron \
 && chmod 0644 /etc/cron.d/mycron \
 && crontab /etc/cron.d/mycron \
 && touch /app/cron.log

# Run cron in the foreground
CMD ["sh", "-c", "cron && tail -f /app/cron.log"]
