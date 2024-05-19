import os
import scrapy
import win32print

class GovUKSpider(scrapy.Spider):
    name = 'gov_uk_spider'
    allowed_domains = ['www.gov.uk']
    start_urls = [
        'https://www.gov.uk/topic/business-tax/import-export',
        # Add more GOV.UK URLs related to import-export regulations here
    ]

    def parse(self, response):
        # Generate a filename for the PDF based on the URL
        filename = response.url.split('/')[-1] + '.pdf'
        filename = os.path.join('gov_uk_pdfs', filename)

        # Create the directory if it doesn't exist
        os.makedirs('gov_uk_pdfs', exist_ok=True)

        # Find the "Microsoft Print to PDF" printer
        for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
            if "Microsoft Print to PDF" in printer[2]:
                pdf_printer = printer[2]
                break

        # Print the webpage HTML to PDF using the "Microsoft Print to PDF" printer
        job_id = win32print.StartDocPrinter(pdf_printer, 1, (response.text, None, "RAW"))
        win32print.WritePrinter(job_id, response.text.encode())
        win32print.EndDocPrinter(job_id)

        self.log(f'Saved PDF: {filename}')