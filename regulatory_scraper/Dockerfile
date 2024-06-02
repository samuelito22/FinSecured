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
 && pip3 install -r requirements.txt

# Copy the rest of the application
COPY . /app

# Setup the database and make the start script executable
RUN chmod +x /app/start.sh \
 && echo "0 0 */3 * * /app/start.sh >> /app/cron.log 2>&1" > /etc/cron.d/mycron \
 && chmod 0644 /etc/cron.d/mycron \
 && crontab /etc/cron.d/mycron \
 && touch /app/cron.log

# Run cron in the foreground
CMD ["sh", "-c", "cron && tail -f /app/cron.log"]
