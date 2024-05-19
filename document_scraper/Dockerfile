FROM ubuntu

RUN apt-get update && \
    apt-get install -y wkhtmltopdf python3-scrapy

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# Rest of your Dockerfile instructions