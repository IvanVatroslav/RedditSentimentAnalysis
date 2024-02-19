from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.utils.config import BASE_URL


class BrowserManager:
    def __init__(self):
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def navigate_to_url(self, url=BASE_URL):
        self.driver.get(url)

    def close_browser(self):
        self.driver.quit()
