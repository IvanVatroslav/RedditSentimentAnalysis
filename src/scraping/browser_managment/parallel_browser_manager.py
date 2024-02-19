from concurrent.futures import ThreadPoolExecutor, as_completed
from src.scraping.browser_managment.browser_manager import BrowserManager

class ParallelBrowserManager:
    def __init__(self, num_workers):
        self.num_workers = num_workers

    def perform_search(self, numbers):
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = {executor.submit(self.search_number, number): number for number in numbers}
            for future in as_completed(futures):
                number = futures[future]
                try:
                    result = future.result()
                    print(f"Search for {number} completed with result: {result}")
                except Exception as exc:
                    print(f"Search for {number} generated an exception: {exc}")

    @staticmethod
    def search_number(number):
        browser_manager = BrowserManager()
        try:
            browser_manager.navigate_to_url(f"https://www.google.hr/search?q={number}")
            # Add logic to perform the search and extract results if necessary
            result = True  # Placeholder for actual result extraction logic
        finally:
            browser_manager.close_browser()
        return result
