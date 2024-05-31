import time
import os

def run_spider():
    # Command to run the Scrapy spider
    os.system("scrapy crawl fca_handbook_spider")

def main():
    os.system("scrapy crawl fca_handbook_spider")

if __name__ == "__main__":
    main()
