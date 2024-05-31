# Use Ubuntu 24.04 as the base image
FROM ubuntu:24.04

# Update and install Python, pip, and necessary libraries
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
    python3-venv  # Make sure to install python3-venv to create virtual environments

# Set working directory in the Docker image
WORKDIR /app

# Copy the requirements.txt file into our working directory /app
COPY requirements.txt .

# Create a virtual environment and activate it
RUN python3 -m venv venv
# Install Python dependencies within the virtual environment
RUN . venv/bin/activate && pip3 install -r requirements.txt

# Copy the rest of the application into the working directory
COPY . .

# Set environment variables
ENV AWS_ACCESS_KEY='AKIA2UC3E5PLSMW37JVG' \
    AWS_SECRET_ACCESS_KEY='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' \
    MAILERSEND_API_KEY='mlsn.2b5f4cedea8238f179dac85c277fab2e49ca37f5ea02888d5054a3b4441d8fbc' \
    SENDER_EMAIL='impex.compliance@outlook.com' \
    RECIPIENT_EMAIL='impex.compliance@outlook.com' \
    DB_PSQL_HOST='172.17.0.3' \
    DB_PSQL_PORT=5432 \
    DB_PSQL_USER='postgres' \
    DB_PSQL_NAME='main_db' \
    DB_PSQL_PASSWORD='20032001Orte'


RUN . venv/bin/activate && python setup_database.py
# Activate virtual environment and run the database setup script
CMD . venv/bin/activate && python app.py
