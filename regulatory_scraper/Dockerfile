FROM ubuntu

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3-scrapy python3-pip cron

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your scrapy project files especially scrapy.cfg
COPY . /app

# Create a shell script to execute the scrapy crawl command
RUN echo 'scrapy crawl my_spider' > /app/run_scrapy.sh && chmod +x /app/run_scrapy.sh

# Create a crontab file and add the job
RUN echo "0 0 * * * /app/run_scrapy.sh > /app/scrapy.log 2>&1" > /etc/cron.d/scrapy-cron

# Apply the cron job
RUN crontab /etc/cron.d/scrapy-cron

# Ensure the environment is set up
WORKDIR /app

# Command to run cron in the foreground
CMD ["cron", "-f"]