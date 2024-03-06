import re
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ReviewExtractor:
    REVIEW_XPATH = "//div[@class='OA1nbd']"
    RATING_XPATH = ("//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]//div[contains(@aria-label, "
                    "'Rated') and contains(@role, 'img')]")
    LOADING_INDICATOR = "//div[@jscontroller='qAKInc'][string-length(@data-loadingmessage) > 0]"
    REVIEW_BLOCK_XPATH = "//div[contains(@class, 'bwb7ce')]"

    def __init__(self, driver):
        self.driver = driver
        self.reviews_df = pd.DataFrame(columns=['Review', 'Rating'])
        self.total_scraped_reviews = 0  # New attribute to track scraped reviews

    @staticmethod
    def extract_rating(aria_label):
        match = re.search(r"Ocijenjeno s (\d+,\d+|\d+) od ukupno 5", aria_label)
        if match:
            rating_str = match.group(1).replace(',', '.')
            return float(rating_str)
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
                #print(f"Review or rating not found for block {i}. Skipping...")
                pass
        self.total_scraped_reviews = count_non_empty_reviews
        print(f"Collection completed. Total reviews collected: {count_non_empty_reviews}")
        return self.reviews_df