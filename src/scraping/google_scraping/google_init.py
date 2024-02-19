from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GoogleInit:
    def __init__(self, browser_manager):
        self.browser_manager = browser_manager

    def open_google_homepage(self):
        self.browser_manager.navigate_to_url('https://www.google.hr')

    def accept_cookies(self):
        try:
            accept_button = WebDriverWait(self.browser_manager.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='I agree']"))
            )
            accept_button.click()
        except Exception as e:
            print("Could not find the 'I agree' button for cookies.")

    def search_query(self, query):
        search_box = self.browser_manager.driver.find_element(By.NAME, 'q')
        search_box.send_keys(query)
        search_box.submit()
