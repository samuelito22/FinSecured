from selenium_scripts.spiders.printable_web_spider import PrintableWebSpider

class GovUKSpider(PrintableWebSpider):
    def download_urls(self, urls):
        """
        Download the webpages at the given URLs as PDFs and upload them to S3 with specific filenames.
        """
        for url in urls:
            filename = f"uk-government/{url.split('/')[-1]}.pdf"
            self.download_url_as_pdf(url, filename)
