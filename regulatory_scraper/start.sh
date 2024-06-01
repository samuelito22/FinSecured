#!/bin/bash
# Activate the virtual environment
source /app/venv/bin/activate

# Now run Scrapy or other Python commands
scrapy crawl fca_handbook_spider

# Deactivate the virtual environment if needed
deactivate