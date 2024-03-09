from concurrent.futures import ThreadPoolExecutor, as_completed


class ParallelBrowserManager:
    def __init__(self, df, csv_file_path, city, workers=5):
        self.workers = workers
        self.df = df
        self.csv_file_path = csv_file_path
        self.city = city

    def update_dataframe_with_results(self, results):
        for result in results:
            if result:
                query, status, date, loaded_reviews, scraped_reviews, percentage = result
                restaurant_name_with_city = query.rsplit(' ', 1)[0]
                restaurant_name = restaurant_name_with_city.replace(f' {self.city}', '').strip()

                conditions = self.df['Restaurant Name'].str.strip() == restaurant_name
                self.df.loc[conditions, ['Last scraping attempt', 'Last scraping attempt date', 'Loaded Reviews',
                                         'Scraped Reviews', 'Scraping Success Percentage']] = [status, date,
                                                                                               loaded_reviews,
                                                                                               scraped_reviews,
                                                                                               percentage]

    def perform_parallel_action(self, action, args_list):
        results = []
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [executor.submit(action, *args) for args in args_list]
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as exc:
                    print(f"Task generated an exception: {exc}")
        self.update_dataframe_with_results(results)
