from bs4 import BeautifulSoup
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, random, os

class TemplateBot(object):
    def __init__(self, show = False, debug = False):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options = options, executable_path=os.environ.get("CHROMEDRIVER_PATH"))
        self.debug = debug

    def protected_sleep(self, time_to_sleep = None):
        if not time_to_sleep:
            list_of_seconds = [x / 10 for x in range(1,11)]
            time.sleep(random.choice(list_of_seconds))
        else:
            time.sleep(time_to_sleep)
    
    def login(self, username: str, password: str):
        self.username = username
        self.password = password

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.close()

    def __str__(self):
        return f'{self.driver.title}\n{self.driver.current_url}'
    
    def close(self):
        self.driver.close()


class ParserBot(TemplateBot):
    def parse(self, url):
        self.driver.get(url)
        self.protected_sleep(1.5)

        while True:
            html = BeautifulSoup(self.driver.page_source, 'html.parser')

            yield (
                html.find('div', {
                    'class': "tv-symbol-price-quote__value js-symbol-last"
                }).text
            )

parser = ParserBot(show = False)
price = parser.parse('https://ru.tradingview.com/symbols/EURUSD/')
app = FastAPI()

@app.get("/")
def home():
    return {"price": "0"}
