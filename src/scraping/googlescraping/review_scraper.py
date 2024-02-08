from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import os

class ReviewScraper:
    FIRST_REVIEW_XPATH = "//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[1]//div[@class='OA1nbd']"
    REVIEW_ELEMENTS_XPATH = "//*[@data-hveid='2']/following-sibling::*//div[@class='OA1nbd']"
    TRANSLATE_BUTTON_XPATH = ("//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]/div[3]//button["
                              "contains(@class, 'qGGAec') and .//span[contains(text(), 'Translated by Google')]]")
    MORE_BUTTON_XPATH = ("//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]//div[@class='OA1nbd']//a["
                         "@role='button' and contains(text(), 'More')]")
    REVIEW_XPATH = "//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]//div[@class='OA1nbd']"
    RATING_XPATH = ("//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]//div[contains(@aria-label, "
                    "'Rated') and contains(@role, 'img')]")
    LOADING_INDICATOR = "//div[@data-loadingmessage='Loading…']"

    def __init__(self, driver_init):
        self.driver_init = driver_init
        self.driver = driver_init.driver
        self.wait = driver_init.wait
        self.short_wait = driver_init.short_wait
        self.previous_last_review_text = None
        self.reviews_df = pd.DataFrame(columns=['Review', 'Rating'])
        self.review_with_text_count = 0

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
            # Wait for loading indicator to disappear before looking for review elements
            self.short_wait.until(EC.invisibility_of_element_located((By.XPATH, self.LOADING_INDICATOR)))

            review_elements = self.driver.find_elements(By.XPATH, self.REVIEW_ELEMENTS_XPATH)

            if not review_elements:
                break  # Break if no reviews are found

            # Get the text of the last review element
            current_last_review_text = review_elements[-1].text.strip()

            # Check if the last review element is empty or the same as the previous
            if not current_last_review_text or current_last_review_text == self.previous_last_review_text:
                self.review_with_text_count = len(
                    [elem for elem in review_elements if elem.text.strip()])  # Store the filtered count
                print(self.review_with_text_count, "reviews found.")
                break

            # Use WebDriver-native method to scroll the last element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", review_elements[-1])

            # Wait for loading indicator to disappear again after scrolling
            self.short_wait.until(EC.invisibility_of_element_located((By.XPATH, self.LOADING_INDICATOR)))

            self.previous_last_review_text = current_last_review_text  # Update for next iteration

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
        count_non_empty_reviews = 0
        i = 1

        # Make sure to populate or update total_reviews_with_text before this loop
        while count_non_empty_reviews <= self.review_with_text_count:
            try:
                review_xpath = self.REVIEW_XPATH.format(i=i)
                rating_xpath = self.RATING_XPATH.format(i=i)

                review_element = self.driver.find_element(By.XPATH, review_xpath)
                rating_element = self.driver.find_element(By.XPATH, rating_xpath)

                review_text = review_element.text.strip()
                if review_text:
                    rating_text = rating_element.get_attribute('aria-label')
                    rating = self.extract_rating(rating_text)

                    if rating is not None:
                        self.reviews_df.loc[len(self.reviews_df)] = [review_text, rating]
                        count_non_empty_reviews += 1
                else:
                    # If a review is empty, we just continue to the next one without breaking the loop
                    pass

            except NoSuchElementException:
                print("No more reviews found. Ending collection.")

            i += 1

    def save_reviews_to_csv(self, filename='reviews_and_ratings.csv'):
        # Navigate up one directory level from 'notebooks' to the project root
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
