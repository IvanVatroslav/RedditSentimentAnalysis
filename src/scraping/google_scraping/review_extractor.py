import re
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ReviewExtractor:
    REVIEW_XPATH = "//div[@class='OA1nbd']"
    RATING_XPATH = ("//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]//div[contains(@aria-label, "
                    "'Rated') and contains(@role, 'img')]")

    def __init__(self, driver):
        self.driver = driver
        self.reviews_df = pd.DataFrame(columns=['Review', 'Rating'])

    @staticmethod
    def collect_review_rating(aria_label):
        match = re.search(r"Ocijenjeno s (\d+,\d+|\d+) od ukupno 5", aria_label)
        if match:
            rating_str = match.group(1).replace(',', '.')
            return float(rating_str)
        return None

    def collect_reviews(self):
        common_parents = self.driver.find_elements(By.XPATH, self.REVIEW_XPATH)
        print(f"Found {len(common_parents)} common parent elements.")
        count_non_empty_reviews = 0

        for i, common_parent_element in enumerate(common_parents, start=1):
            try:
                review_element = common_parent_element
                rating_element = self.driver.find_element(By.XPATH, self.RATING_XPATH.format(i=i))

                review_text = review_element.text.strip()
                if review_text:  # Ensure review text is not empty
                    rating_text = rating_element.get_attribute('aria-label')
                    rating = self.extract_rating(rating_text)  # Extract numerical rating

                    if rating is not None:  # Check if rating extraction was successful
                        self.reviews_df.loc[len(self.reviews_df)] = [review_text, rating]
                        count_non_empty_reviews += 1

            except NoSuchElementException:
                print(f"Review or rating not found for block {i}. Skipping...")

        print(f"Collection completed. Total reviews collected: {count_non_empty_reviews}")
