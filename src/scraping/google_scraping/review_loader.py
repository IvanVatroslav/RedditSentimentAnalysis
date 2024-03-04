from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ReviewLoader:
    REVIEW_BLOCK_XPATH = "//div[contains(@class, 'bwb7ce')]"
    LOADING_INDICATOR = "//div[@jscontroller='qAKInc'][string-length(@data-loadingmessage) > 0]"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.short_wait = WebDriverWait(driver, 5, poll_frequency=0.5)
        self.previous_total_reviews = 0

    def load_reviews(self):
        self.previous_total_reviews = 0
        # Ensure visibility of initial reviews
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.REVIEW_BLOCK_XPATH)))
        while True:
            # Wait for any loading indicators to disappear, ensuring the page is ready
            self.short_wait.until(EC.invisibility_of_element((By.XPATH, self.LOADING_INDICATOR)))

            review_elements = self.driver.find_elements(By.XPATH, self.REVIEW_BLOCK_XPATH)
            current_total_reviews = len(review_elements)

            if not review_elements or current_total_reviews == self.previous_total_reviews:
                # If no new reviews are loaded or if the count hasn't changed, exit the loop
                break

            # Scroll to the specific target element to trigger loading more reviews
            self.driver.execute_script("arguments[0].scrollIntoView(true);", review_elements[-1])

            # Use WebDriverWait to explicitly wait for the number of reviews to increase
            try:
                self.wait.until(
                    lambda driver: len(
                        driver.find_elements(By.XPATH, self.REVIEW_BLOCK_XPATH)) > self.previous_total_reviews)
                # Update current count after waiting
                current_total_reviews = len(self.driver.find_elements(By.XPATH, self.REVIEW_BLOCK_XPATH))
            except TimeoutException:
                # If no new reviews are loaded within the timeout, assume all reviews are loaded
                break

            self.previous_total_reviews = current_total_reviews
            self.short_wait.until(EC.invisibility_of_element((By.XPATH, self.LOADING_INDICATOR)))

        print(f"Final count of reviews loaded: {current_total_reviews}")
