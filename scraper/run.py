import os
import json
from selenium_scripts.spiders.gov_uk_spider import GovUKSpider
from selenium_scripts.utils.email_alert import send_email_alert
import logging
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(filename='scraper.log', level=logging.ERROR)

def run_scrapy_spiders():
    print("Running Scrapy Spiders...")
    os.chdir("scrapy")
    # subprocess.run(["scrapy", "crawl", "some_spider_name"])  # replace 'some_spider_name' with your actual Scrapy spider name
    os.chdir("..")
    print("Finished running Scrapy Spiders.")

def run_gov_uk_spider():
    bucket_name = 'impex-compliance-regulations-docs'
    access_key_id = os.getenv('AWS_ACCESS_KEY')
    secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    with open('urls.json') as file:
        data = json.load(file)
        urls = data['gov_uk_urls']

    try:
        spider = GovUKSpider(bucket_name, access_key_id, secret_access_key)
        spider.download_urls(urls)
        spider.close()
    except Exception as e:
        logging.exception("An error occurred during scraping.")
        error_message = f"Scraping failed with the following error:\n\n{str(e)}"
        send_email_alert("Scraping Error", error_message)

if __name__ == "__main__":
    print("Running Selenium Scripts...")
    run_gov_uk_spider()
    print("Finished running Selenium Scripts.")
    run_scrapy_spiders()