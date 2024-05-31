import scrapy
from scrapy.http import Request
import os

class FCAHandbookSpider(scrapy.Spider):
    name = 'fca_handbook_spider'
    allowed_domains = ['handbook.fca.org.uk']
    start_urls = ['https://www.handbook.fca.org.uk/handbook']

    def __init__(self, *args, **kwargs):
        super(FCAHandbookSpider, self).__init__(*args, **kwargs)
        self.processed_urls = set()  # Set to track processed PDF URLs

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
            if 'handbook' in section and pdf_url not in self.processed_urls:
                self.processed_urls.add(pdf_url)
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
        # Final cleanup or error report handling; adapt as necessary
        '''
        if self.error_log:
            subject = "FCA Handbook Spider Error Report"
            message = "\n".join(self.error_log)
            #send_email_alert(subject, message)
        '''
