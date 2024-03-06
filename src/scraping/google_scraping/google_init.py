

from src.scraping.browser_managment import BrowserManager


class GoogleInit:

    def __init__(self, browser_manager):
        self.browser_manager = browser_manager
        self.driver = self.browser_manager.driver
        self.wait = self.browser_manager.wait
        self.short_wait = self.browser_manager.short_wait

    @staticmethod
    def construct_query(search_type, name="", city=""):
        if search_type == "list":
            return f"restorani {city}".replace(" ", "+")
        elif search_type == "review":
            return f"{name} {city}".replace(" ", "+")
        else:
            raise ValueError("Invalid search type specified.")

    def search(self, query):
        try:
            search_url = f"https://www.google.hr/search?q={query}"
            self.browser_manager.navigate_to_url(search_url)
            # Implement result extraction logic here
            result = True  # Placeholder for actual result extraction logic
        except Exception as e:
            print(f"An error occurred: {e}")
            result = False
        return result



