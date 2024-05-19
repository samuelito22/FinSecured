import boto3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64

class PrintableWebSpider:
    def __init__(self, bucket_name, access_key_id, secret_access_key):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
        self.driver = self._initialize_webdriver()

    def _initialize_webdriver(self):
        """
        Initialize the WebDriver with headless Chrome options and PDF print settings.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        appState = {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }
        prefs = {
            'printing.print_preview_sticky_settings.appState': appState
        }
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--kiosk-printing')

        return webdriver.Chrome(options=chrome_options)

    def download_url_as_pdf(self, url, filename):
        """
        Download the webpage at the given URL as a PDF and upload it to S3.
        """
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        result = self.driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,
            "withBackground": True,
            "preferCSSPageSize": True,
            "transferMode": "ReturnAsBase64",
        })

        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=filename,
            Body=base64.b64decode(result['data']),
            ContentType='application/pdf'
        )

    def close(self):
        """
        Close the WebDriver.
        """
        self.driver.quit()