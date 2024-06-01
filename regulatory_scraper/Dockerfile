# Use Ubuntu 24.04 as the base image
FROM ubuntu:24.04

# Update and install Python, pip, necessary libraries, and cron
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
    cron

# Set working directory in the Docker image
WORKDIR /app

COPY . .

RUN python3 -m venv venv

RUN . venv/bin/activate && pip3 install -r requirements.txt

RUN chmod +x /app/start.sh

RUN echo "0 0 * * * /app/start.sh >> /app/cron.log 2>&1" > /etc/cron.d/mycron
RUN echo "* * * * * /app/start.sh >> /app/cron.log 2>&1" > /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron
RUN crontab /etc/cron.d/mycron
RUN touch /app/cron.log

RUN . venv/bin/activate && python setup_database.py

CMD ["cron", "-f"]

# Copy the requirements.txt file into our working directory /app
#COPY requirements.txt .

# Create a virtual environment and activate it
#RUN python3 -m venv venv
#RUN . venv/bin/activate && pip3 install -r requirements.txt

# Copy the rest of the application into the working directory
#COPY . .

# Make sure the shell script is executable
#RUN chmod +x /app/start.sh

# Create a cron job
# RUN echo "0 0 * * * /app/start.sh >> /app/cron.log 2>&1" > /etc/cron.d/mycron
#RUN echo "* * * * * /app/start.sh >> /app/cron.log 2>&1" > /etc/cron.d/mycron
#RUN chmod 0644 /etc/cron.d/mycron
#RUN crontab /etc/cron.d/mycron
#RUN touch /app/cron.log

# Install Python dependencies within the virtual environment
#RUN . venv/bin/activate && python setup_database.py

# Command to start the cron daemon
#CMD ["cron", "-f"]
