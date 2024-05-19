import os
import scrapy
import pdfkit

class GovUKSpider(scrapy.Spider):
    name = 'gov_uk_spider'
    allowed_domains = ['www.gov.uk']
    start_urls = [
        'https://www.gov.uk/topic/business-tax/import-export',
        # Add more GOV.UK URLs related to import-export regulations
    ]

    def parse(self, response):
        # Generate a filename for the PDF based on the URL
        filename = response.url.split('/')[-1] + '.pdf'
        filename = os.path.join('gov_uk_pdfs', filename)

        # Create the directory if it doesn't exist
        os.makedirs('gov_uk_pdfs', exist_ok=True)

        # Configure pdfkit options
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'no-outline': None
        }

        # Save the webpage as a PDF using pdfkit
        pdfkit.from_url(response.url, filename, options=options)

        self.log(f"Saved PDF: {filename}")

        # Follow links to other pages
        for link in response.css('a::attr(href)').getall():
            if link.startswith('/'):
                # Construct the absolute URL
                url = response.urljoin(link)
                yield scrapy.Request(url, callback=self.parse)