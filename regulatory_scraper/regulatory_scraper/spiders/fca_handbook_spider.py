import scrapy
from scrapy.http import Request
import os

class FCAHandbookSpider(scrapy.Spider):
    name = 'fca_handbook_spider'
    allowed_domains = ['handbook.fca.org.uk']
    start_urls = ['https://www.handbook.fca.org.uk/handbook']

    def __init__(self, *args, **kwargs):
        super(FCAHandbookSpider, self).__init__(*args, **kwargs)
        self.allowed_categories = [
            'PRIN', 'SYSC', 'COCON', 'COND', 'APER', 'FIT', 'FINMAR', 'TC', 'GEN', 'FEES',
            'GENPRU', 'INSPRU', 'MIFIDPRU', 'MIPRU', 'IPRU-FSOC', 'IPRU-INS', 'IPRU-INV',
            'COBS', 'ICOBS', 'MCOB', 'BCOBS', 'CMCOB', 'FPCOB', 'CASS', 'MAR', 'PROD', 'ESG',
            'SUP', 'DEPP', 'DISP', 'CONRED', 'COMP', 'COLL', 'CREDS', 'CONC', 'FUND', 'PROF',
            'RCB', 'REC', 'LR', 'PRR', 'DTR', 'DISC', 'EMPS', 'OMPS', 'SERV', 'BENCH', 'COLLG',
            'EG', 'FCG', 'FCTR', 'PERG', 'RFCCBS', 'RPPD', 'UNFCOG', 'WDPG', 'M2G', 'GLOSSARY'
        ]

    def parse(self, response):
        # Extract links to sections within the handbook
        section_links = response.css('a[href^="/handbook"]::attr(href)').getall()
        for link in section_links:
            section_url = response.urljoin(link)
            yield Request(section_url, callback=self.parse_section)

    def parse_section(self, response):
        pdf_links = response.css('a[href$=".pdf"]::attr(href)').getall()
        for link in pdf_links:
            pdf_url = response.urljoin(link)
            section = pdf_url.split('/')
            if 'handbook' in section:
                category_index = section.index('handbook') + 1
                category_name = section[category_index]
                if category_name in self.allowed_categories:
                    yield Request(pdf_url, callback=self.save_pdf, meta={'pdf_url': pdf_url})

    def save_pdf(self, response):
        pdf_url = response.meta['pdf_url']
        section = pdf_url.split('/')
        category_index = section.index('handbook') + 1
        category_name = section[category_index]
        filename = os.path.basename(pdf_url)
        file_path = f'handbook/{category_name}/{filename}'
        yield {
            'file_url': pdf_url,
            'file_path': file_path,
            'response_body': response.body,  # Now contains the actual PDF file content
            'category': category_name
        }

    def closed(self, reason):
        # Log the reason why the spider was closed
        self.logger.info(f"Spider closed because of: {reason}")

        # Log final statistics (if available)
        if hasattr(self, 'crawler'):
            stats = self.crawler.stats.get_stats()  # Retrieve stats collected during the crawl
            self.logger.info(f"Total requests made: {stats.get('downloader/request_count', 0)}")
            self.logger.info(f"Total requests received: {stats.get('downloader/response_count', 0)}")
            self.logger.info(f"Total PDFs collected: {stats.get('item_scraped_count', 0)}")

        # Perform any other cleanup necessary for the spider
        self.logger.info("Performing cleanup and releasing resources.")

        # Custom logic to handle specific cleanup or summary tasks
        if hasattr(self, 'error_count') and self.error_count > 0:
            self.logger.warning(f"Encountered {self.error_count} errors during scraping.")

