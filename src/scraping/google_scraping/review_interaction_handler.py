import time

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ReviewInteractionHandler:
    TRANSLATE_BUTTON_XPATH = ("//div[@data-attrid='kc:/local:all reviews']//div[3]/div/div[{i}]/div[3]//button["
                              "contains(@class, 'qGGAec') and .//span[contains(text(), 'Translated by Google')]]")
    MORE_BUTTON_XPATH = "//div[@class='OA1nbd']//a[@role='button' and contains(text(), 'Više')]"
    ACCEPT_COOKIES_XPATH = "//button[@id='L2AGLb']"
    # RESTAURANT_REVIEWS_REDIRECT_XPATH = '//a[contains(text(), " recenzij")]'
    # RESTAURANT_REVIEWS_REDIRECT_XPATH = '//div[@data-md="101"]//a'
    RESTAURANT_REVIEWS_REDIRECT_XPATH = '//a[contains(text(), " recenzij")] | //div[@data-md="101"]//a'
    RESTAURANT_REVIEWS_LINK_XPATH = '//a[@class="Ky0SRd"]'
    GO_TO_RESTAURANT_LIST_XPATH = "//span[text()='Više mjesta']"
    REVIEWS_TAB_XPATH = "//span[text()='Reviews']"

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

    def accept_cookies(self):
        try:
            accept_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.ACCEPT_COOKIES_XPATH)))
            accept_button.click()
        except Exception as e:
            print("Cookies acceptance button not found or not clickable.")

    def navigate_to_reviews(self):
        retries = 3  # Number of retries for clicking the element
        for attempt in range(retries):
            try:
                reviews_redirect = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, self.RESTAURANT_REVIEWS_REDIRECT_XPATH)))
                reviews_count_text = reviews_redirect.text.replace('.', '').split()[0]
                reviews_count = int(reviews_count_text)
                print(f"Found {reviews_count} reviews.")
                reviews_redirect.click()
                reviews_link = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, self.RESTAURANT_REVIEWS_LINK_XPATH)))
                reviews_link.click()
                break  # Click succeeded; break out of the retry loop
            except (StaleElementReferenceException, NoSuchElementException):
                # Element is stale or not found, wait a bit and try again
                if attempt < retries - 1:  # Avoid sleeping on the last attempt
                    time.sleep(2)  # Wait 1 second before retrying
                continue  # Retry the loop
            except TimeoutException:
                # Element not clickable within the wait time
                print(f"Timeout waiting for the reviews to become clickable.")
                if attempt == retries - 1:
                    raise  # Raise exception if all retries have failed
            except Exception as e:
                print(f"Failed to navigate to reviews: {e}")
                if attempt == retries - 1:
                    raise  # Raise exception if all retries have failed

    def navigate_to_restaurant_list(self):
        more_places_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.GO_TO_RESTAURANT_LIST_XPATH)))
        more_places_button.click()


