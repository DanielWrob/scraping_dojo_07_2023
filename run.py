import os
import time
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class QuoteScraper:
    def __init__(self, proxy, input_url, output_file):
        self.proxy = proxy
        self.input_url = input_url
        self.output_file = output_file
        self.driver = None
        self.quotes = []

    def initialize_driver(self):
        options = Options()
        # proxy disabled (not working)
        # if self.proxy:
        #     options.add_argument(f"--proxy-server={self.proxy}")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def scrape_quotes(self):
        self.initialize_driver()
        self.driver.get(self.input_url)

        while True:
            time.sleep(5)
            quote_elements = self.driver.find_elements(By.CLASS_NAME, "quote")

            for quote_element in quote_elements:
                quote_text = quote_element.find_elements(By.CLASS_NAME, "text")[0].text
                quote_author = quote_element.find_elements(By.CLASS_NAME, "author")[0].text
                quote_tags = [tag.text for tag in quote_element.find_elements(By.CLASS_NAME, "tag")]
                quote = {"text": quote_text, "by": quote_author, "tags": quote_tags}
                self.quotes.append(quote)

            try:
                next_button = self.driver.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a")
            except NoSuchElementException:
                break
            except:
                print("Something else went wrong")
                break
            else:
                next_button.click()
                time.sleep(3)

        self.driver.quit()
        self.save_quotes()

    def save_quotes(self):
        with open(self.output_file, "w", encoding='utf-8') as file:
            for quote in self.quotes:
                file.write(json.dumps(quote) + "\n")

# Load environment variables from .env file
load_dotenv()

# Get the proxy, input URL, and output file from environment variables
proxy = os.getenv("PROXY")
input_url = os.getenv("INPUT_URL")
output_file = os.getenv("OUTPUT_FILE")

# Create an instance of QuoteScraper and scrape the quotes
scraper = QuoteScraper(proxy, input_url, output_file)
scraper.scrape_quotes()
