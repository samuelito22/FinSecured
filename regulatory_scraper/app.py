import time
import os
import logging

# Set the log level to NOTSET to suppress all logs
logging.getLogger('fontTools')
logging.getLogger('weasyprint')


def run_spider():
    # Command to run the Scrapy spider
    os.system("scrapy crawl fca_handbook_spider")

def main():
    os.system("scrapy crawl fca_handbook_spider")

if __name__ == "__main__":
    main()
