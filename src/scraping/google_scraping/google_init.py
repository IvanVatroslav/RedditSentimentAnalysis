

from src.scraping.browser_managment import BrowserManager


class GoogleInit:

    def __init__(self, browser_manager):
        self.browser_manager = browser_manager
        self.driver = self.browser_manager.driver
        self.wait = self.browser_manager.wait
        self.short_wait = self.browser_manager.short_wait

    def search_restaurant(self, restaurant_name, city):
        browser_manager = BrowserManager()
        try:
            query = f"{restaurant_name} {city}".replace(" ", "+")
            search_url = f"https://www.google.hr/search?q={query}"
            browser_manager.navigate_to_url(search_url)
            # Implement result extraction logic here
            result = True  # Placeholder for actual result extraction logic
        except Exception as e:
            print(f"An error occurred: {e}")
            result = False
        return result


    def close_browser(self):
        self.driver.quit()
