#!/bin/bash

echo "Changing to the /app directory..."
cd /app

echo "Activating the virtual environment..."
source venv/bin/activate

echo "Setting up the database..."
python setup_database.py

echo "Starting the Scrapy spider..."
scrapy crawl fca_handbook_spider

echo "Cleaning up the database..."
python cleanup_database.py