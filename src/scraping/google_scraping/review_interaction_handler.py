from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ReviewInteractionHandler:
    TRANSLATE_BUTTON_XPATH = ("//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]/div[3]//button["
                              "contains(@class, 'qGGAec') and .//span[contains(text(), 'Translated by Google')]]")
    MORE_BUTTON_XPATH = "//div[@class='OA1nbd']//a[@role='button' and contains(text(), 'Više')]"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_buttons(self):
        self.click_translate_buttons()
        self.click_more_buttons()

    def click_translate_buttons(self):
        review_elements = self.driver.find_elements(By.XPATH, self.TRANSLATE_BUTTON_XPATH.format(i='*'))
        for i, translate_button in enumerate(review_elements, start=1):
            try:
                self.wait.until(EC.visibility_of(translate_button))
                self.wait.until(EC.element_to_be_clickable(translate_button))
                translate_button.click()
            except (NoSuchElementException, ElementClickInterceptedException):
                print(f"Translation button not found or not clickable for review {i}. Skipping...")

    def click_more_buttons(self):
        more_buttons = self.driver.find_elements(By.XPATH, self.MORE_BUTTON_XPATH)
        for button in more_buttons:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", button)
                button.click()
            except (NoSuchElementException, ElementClickInterceptedException):
                print(f"More button not found or not clickable. Skipping...")
