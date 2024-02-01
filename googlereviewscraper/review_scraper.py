from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from driver_init import DriverInit  # Assuming the DriverInit class is saved in driver_init.py
import pandas as pd
import re


class ReviewScraper:
    FIRST_REVIEW_XPATH = "//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[1]//div[@class='OA1nbd']"
    REVIEW_ELEMENTS_XPATH = "//div[@class='review-element-class']"
    TRANSLATE_BUTTON_XPATH = ("//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]/div[3]//button["
                              "contains(@class, 'qGGAec') and .//span[contains(text(), 'Translated by Google')]]")
    MORE_BUTTON_XPATH = ("//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]//div[@class='OA1nbd']//a["
                         "@role='button' and contains(text(), 'More')]")
    REVIEW_XPATH = "//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]//div[@class='OA1nbd']"
    RATING_XPATH = ("//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]//div[contains(@aria-label, "
                    "'Rated') and contains(@role, 'img')]")

    def __init__(self, driver_init):
        self.driver_init = driver_init
        self.driver = driver_init.driver
        self.wait = driver_init.wait
        self.short_wait = driver_init.short_wait
        self.previous_last_review_text = None
        self.reviews_df = pd.DataFrame(columns=['Review', 'Rating'])

    def return_to_first_review(self):
        try:
            first_review_element = self.driver.find_element(By.XPATH, self.FIRST_REVIEW_XPATH)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", first_review_element)
        except Exception as e:
            print(f"Error scrolling to first review: {e}")

    def load_reviews(self):
        self.previous_last_review_text = None
        self.return_to_first_review()

        while True:
            self.short_wait.until(
                lambda driver: self.driver.find_elements(By.XPATH, self.REVIEW_ELEMENTS_XPATH))

            review_elements = self.driver.find_elements(By.XPATH, self.REVIEW_ELEMENTS_XPATH)

            if not review_elements:
                break

            current_last_review_text = review_elements[-1].text.strip()

            if current_last_review_text == self.previous_last_review_text:
                break

            self.previous_last_review_text = current_last_review_text
            self.driver.execute_script("arguments[0].scrollIntoView(true);", review_elements[-1])

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
            review_elements = self.driver.find_elements(By.XPATH, self.REVIEW_ELEMENTS_XPATH)
            for i in range(1, len(review_elements) + 1):
                more_button_xpath = self.MORE_BUTTON_XPATH.format(i=i)
                more_buttons = self.driver.find_elements(By.XPATH, more_button_xpath)
                if more_buttons and more_buttons[0].is_displayed():
                    self.driver.execute_script("arguments[0].scrollIntoView();", more_buttons[0])
                    try:
                        more_buttons[0].click()
                    except Exception as e:
                        print(f"Skipping a non-interactable 'More' button at index {i}: {e}")
        except Exception as e:
            print(f"Error clicking 'More' buttons: {e}")

    @staticmethod
    def extract_rating(aria_label):
        match = re.search(r"Rated (\d+(\.\d+)?) out of 5", aria_label)
        return float(match.group(1)) if match else None

    def collect_reviews(self):
        self.reviews_df = pd.DataFrame(columns=['Review', 'Rating'])

        try:
            review_elements = self.driver.find_elements(By.XPATH, self.REVIEW_ELEMENTS_XPATH)
            for i, element in enumerate(review_elements, start=1):
                try:
                    review_xpath = self.REVIEW_XPATH.format(i=i)
                    rating_xpath = self.RATING_XPATH.format(i=i)

                    review_element = self.driver.find_element(By.XPATH, review_xpath)
                    rating_element = self.driver.find_element(By.XPATH, rating_xpath)

                    review_text = review_element.text.strip()
                    rating_text = rating_element.get_attribute('aria-label')

                    rating = self.extract_rating(rating_text)

                    if review_text and rating is not None:
                        self.reviews_df = pd.concat(
                            [self.reviews_df, pd.DataFrame.from_records([{'Review': review_text, 'Rating': rating}])],
                            ignore_index=True)
                except NoSuchElementException:
                    print(f"No more reviews or ratings found at index {i}.")
                    break
        except Exception as e:
            print(f"Error collecting reviews: {e}")

    def save_reviews_to_csv(self, filename='reviews_and_ratings.csv'):
        try:
            self.reviews_df.to_csv(filename, index=False)
            print(f"Saved reviews to {filename}")
        except Exception as e:
            print(f"Error saving reviews to CSV: {e}")
