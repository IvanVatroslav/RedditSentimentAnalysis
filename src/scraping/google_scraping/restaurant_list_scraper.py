# Import necessary libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, \
    ElementClickInterceptedException
import time
import pandas as pd

from selenium import webdriver


# Define the scraping functionality
class RestaurantListScraper:
    def __init__(self, driver):
        self.driver = driver
        self.MORE_PLACES_XPATH = "//span[text()='Više rezultata' or text()='More places']"
        self.LOADING_ICON_XPATH = "//div[@data-hveid='CAQQAw']"
        self.TITLE_XPATH = "//span[@class='OSrXXb e62wic']"

    def get_last_element_text(self, xpath):
        try:
            elements = self.driver.find_elements(By.XPATH, xpath)
            if elements:
                return elements[-1].text
            else:
                return None
        except NoSuchElementException:
            return None

    def wait_for_loading_complete(self, loading_icon_xpath, timeout=10):
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                loading_icon_present = WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located((By.XPATH, loading_icon_xpath))
                )
                if loading_icon_present:
                    WebDriverWait(self.driver, 5).until(
                        EC.invisibility_of_element_located((By.XPATH, loading_icon_xpath))
                    )
            except TimeoutException:
                break

    def scrape_restaurants(self):
        restaurant_names = set()  # Use a set to store unique restaurant names
        last_unique_element_text = None
        while True:
            try:
                more_places_button = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, self.MORE_PLACES_XPATH))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_places_button)
                self.driver.execute_script("arguments[0].click();", more_places_button)

                self.wait_for_loading_complete(self.LOADING_ICON_XPATH)

                # Retrieve all restaurant names currently loaded on the page
                restaurant_elements = self.driver.find_elements(By.XPATH, self.TITLE_XPATH)
                for element in restaurant_elements:
                    restaurant_names.add(element.text)  # Adds to set, ignoring duplicates

                current_last_element_text = self.get_last_element_text(self.TITLE_XPATH)
                if current_last_element_text == last_unique_element_text:
                    print("No new content loaded. End of list reached.")
                    break
                else:
                    last_unique_element_text = current_last_element_text

                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, self.MORE_PLACES_XPATH))
                )

            except TimeoutException:
                print("Timeout occurred. Possibly all 'More Places' elements have been clicked, or no more are found.")
                break
            except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException):
                print("The 'More Places' button is no longer interactable or clickable. Assuming all content loaded.")
                break

        return pd.DataFrame(list(restaurant_names), columns=['Restaurant Name'])
