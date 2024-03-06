from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class ReviewLoader:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.REVIEW_BLOCK_XPATH = "//div[contains(@data-attrid, 'kc:/local:all reviews')]"  # Adjusted XPath for review blocks
        self.LOADING_INDICATOR_XPATH = "//div[@jscontroller='qAKInc'][string-length(@data-loadingmessage) > 0]"
        self.total_loaded_reviews = 0  # Initialize total_loaded_reviews attribute
    def load_reviews(self):
        empty_review_batches_counter = 0
        while empty_review_batches_counter < 3:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, self.REVIEW_BLOCK_XPATH)))
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, self.LOADING_INDICATOR_XPATH)))

            review_elements = self.driver.find_elements(By.XPATH, self.REVIEW_BLOCK_XPATH + "//div[3]")  # Specific review text container
            if not review_elements:
                print("No more reviews to load.")
                break

            scroll_target = review_elements[-1]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", scroll_target)

            try:
                new_reviews_loaded = WebDriverWait(self.driver, 60).until(
                    lambda driver: len(driver.find_elements(By.XPATH, self.REVIEW_BLOCK_XPATH + "//div[3]")) > len(review_elements))
                if new_reviews_loaded:
                    empty_reviews = [elem for elem in review_elements[-3:] if not elem.text.strip()]
                    if len(empty_reviews) == 3:
                        empty_review_batches_counter += 1
                    else:
                        empty_review_batches_counter = 0
            except TimeoutException:
                print("Timeout waiting for new reviews to load.")
                break

        self.total_reviews_loaded = len(self.driver.find_elements(By.XPATH, self.REVIEW_BLOCK_XPATH + "//div[3]"))
        print(f"Total reviews loaded: {self.total_reviews_loaded}")