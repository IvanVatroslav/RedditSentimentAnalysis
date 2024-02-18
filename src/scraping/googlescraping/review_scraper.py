from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import os

from selenium.webdriver.support.wait import WebDriverWait


class ReviewScraper:
    FIRST_REVIEW_XPATH = ("//*[@id='akp_tsuid_13']/div/div[1]/div/g-sticky-content-container/div/block-component/div"
                          "/div[1]/div/div/div/div[1]/div/div/div[6]/g-flippy-carousel/div/div/ol/li["
                          "3]/span/div/div/div/div[2]/c-wiz/div/div[2]/div[1]/div[1]")
    REVIEW_ELEMENTS_XPATH = "//*[@data-hveid='2']/following-sibling::*//div[@class='OA1nbd']"
    TRANSLATE_BUTTON_XPATH = ("//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]/div[3]//button["
                              "contains(@class, 'qGGAec') and .//span[contains(text(), 'Translated by Google')]]")
    MORE_BUTTON_XPATH = "//div[@class='OA1nbd']//a[@role='button' and contains(text(), 'Više')]"
    REVIEW_XPATH = "//div[@class='OA1nbd']"
    RATING_XPATH = ("//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]//div[contains(@aria-label, "
                    "'Rated') and contains(@role, 'img')]")
    #LOADING_INDICATOR = "//div[string-length(@data-loadingmessage) > 0]"
    LOADING_INDICATOR = "//div[@jscontroller='qAKInc'][string-length(@data-loadingmessage) > 0]"
    REVIEW_BLOCK_XPATH = "//div[contains(@class, 'bwb7ce')]"

    def __init__(self, driver_init=None, driver=None):
        self.previous_total_reviews = None
        if driver is not None:
            self.driver = driver
            self.wait = WebDriverWait(driver, 10)
            self.short_wait = WebDriverWait(driver, 5, poll_frequency=0.5)
        elif driver_init is not None:
            self.driver = driver_init.driver
            self.wait = driver_init.wait
            self.short_wait = driver_init.short_wait
        else:
            raise ValueError("Either driver_init or driver must be provided.")

        self.previous_last_review_text = None
        self.reviews_df = pd.DataFrame(columns=['Review', 'Rating'])
        self.review_with_text_count = 0

    def return_to_first_review(self):
        try:
            first_review_element = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.REVIEW_BLOCK_XPATH)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", first_review_element)
        except Exception as e:
            print(f"Error scrolling to first review: {e}")

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

            scroll_target_xpath = ".//div[4]"  # Adjust based on the precise element you need to scroll to
            scroll_target = review_elements[-1].find_element(By.XPATH, scroll_target_xpath)

            # Scroll to the specific target element to trigger loading more reviews
            self.driver.execute_script("arguments[0].scrollIntoView(true);", scroll_target)

            # Use WebDriverWait to explicitly wait for the number of reviews to increase
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.find_elements(By.XPATH, self.REVIEW_BLOCK_XPATH)) > self.previous_total_reviews)
                # Update current count after waiting
                current_total_reviews = len(self.driver.find_elements(By.XPATH, self.REVIEW_BLOCK_XPATH))
            except TimeoutException:
                # If no new reviews are loaded within the timeout, assume all reviews are loaded
                break

            self.previous_total_reviews = current_total_reviews
            self.short_wait.until(EC.invisibility_of_element((By.XPATH, self.LOADING_INDICATOR)))
        print(f"Final count of reviews loaded: {current_total_reviews}")

    def click_translate_buttons(self):
        try:
            review_elements = self.driver.find_elements(By.XPATH, self.REVIEW_ELEMENTS_XPATH)
            for i, _ in enumerate(review_elements, start=1):
                translate_button_xpath = self.TRANSLATE_BUTTON_XPATH.format(i=i)
                translate_buttons = self.driver.find_elements(By.XPATH, translate_button_xpath)
                if translate_buttons:
                    translate_buttons[0].click()
        except Exception as e:
            print(f"Error clicking translate buttons: {e}")

    def click_more_buttons(self):
        try:
            more_buttons = self.driver.find_elements(By.XPATH, self.MORE_BUTTON_XPATH)
            for button in more_buttons:
                if button.is_displayed():
                    self.driver.execute_script("arguments[0].scrollIntoView();", button)
                    try:
                        button.click()
                    except Exception as e:
                        print(f"Skipping a non-interactable 'More' button: {e}")
        except Exception as e:
            print(f"Error clicking 'More' buttons: {e}")

    @staticmethod
    def extract_rating(aria_label):
        # Assuming the format is "Ocijenjeno s 5,0 od ukupno 5"
        # Adjust the regular expression to match this format
        match = re.search(r"Ocijenjeno s (\d+,\d+|\d+) od ukupno 5", aria_label)
        if match:
            # Replace comma with dot for float conversion if necessary
            rating_str = match.group(1).replace(',', '.')
            return float(rating_str)
        else:
            return None

    def collect_reviews(self):
        common_parents = self.driver.find_elements(By.XPATH, self.REVIEW_BLOCK_XPATH)
        print(f"Found {len(common_parents)} common parent elements.")

        # Initialize count of non-empty reviews collected
        count_non_empty_reviews = 0

        for i, common_parent_element in enumerate(common_parents, start=1):
            try:
                review_element = common_parent_element.find_element(By.XPATH, ".//div[contains(@class, 'OA1nbd')]")
                rating_element = common_parent_element.find_element(By.XPATH,
                                                                    ".//div[@role='img'][contains(@aria-label, 'Ocijenjeno s')]")

                review_text = review_element.text.strip()
                if review_text:  # Ensure review text is not empty
                    rating_text = rating_element.get_attribute('aria-label')
                    rating = self.extract_rating(rating_text)  # Extract numerical rating

                    if rating is not None:  # Check if rating extraction was successful
                        # Append review and rating to DataFrame
                        self.reviews_df.loc[len(self.reviews_df)] = [review_text, rating]
                        count_non_empty_reviews += 1  # Increment count of collected reviews

            except NoSuchElementException:
                print(f"Review or rating not found for block {i}. Skipping...")

        print(f"Collection completed. Total reviews collected: {count_non_empty_reviews}")

    def save_reviews_to_csv(self, filename='reviews_and_ratings.csv'):
        project_root = os.path.dirname(os.getcwd())
        directory = os.path.join(project_root, 'data', 'raw')

        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, filename)

        try:
            self.reviews_df.to_csv(filepath, index=False)
            print(f"Saved reviews to {filepath}")
        except Exception as e:
            print(f"Error saving reviews to CSV: {e}")
