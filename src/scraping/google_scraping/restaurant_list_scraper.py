from .google_init import GoogleInit


class RestaurantListScraper(GoogleInit):
    def __init__(self, browser_manager, city):
        super().__init__(browser_manager)
        self.city = city

    def scrape_restaurants(self):
        # Placeholder for the method implementation
        pass
