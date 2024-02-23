from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DriverInit:
    ACCEPT_COOKIES_XPATH = "//button[@id='L2AGLb']"
    REVIEWS_TAB_XPATH = "//span[text()='Reviews']"

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.short_wait = WebDriverWait(self.driver, 5, poll_frequency=0.5)
        self.driver.maximize_window()

    def navigate_to_url(self, url):
        self.driver.get(url)
        accept_cookies = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.ACCEPT_COOKIES_XPATH)))
        accept_cookies.click()

    def close_browser(self):
        self.driver.quit()
