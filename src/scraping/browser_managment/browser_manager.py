from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class BrowserManager:
    def __init__(self, wait_time=10, short_wait_time=5):
        self.driver, self.wait, self.short_wait = self._initialize_driver(wait_time, short_wait_time)

    def _initialize_driver(self, wait_time, short_wait_time):
        chrome_options = Options()

        chrome_options.add_argument("--lang=hr")
        # Update here: Change 'chrome_options=chrome_options' to 'options=chrome_options'
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        wait = WebDriverWait(driver, wait_time)
        short_wait = WebDriverWait(driver, short_wait_time)
        return driver, wait, short_wait

    def navigate_to_url(self, url):
        self.driver.get(url)
        # Perform additional actions like accepting cookies here

    def close_browser(self):
        self.driver.quit()
