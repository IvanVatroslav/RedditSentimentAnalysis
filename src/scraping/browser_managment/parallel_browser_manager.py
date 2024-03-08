from concurrent.futures import ThreadPoolExecutor, as_completed


class ParallelBrowserManager:
    def __init__(self, df, csv_file_path, city, workers=5):
        self.workers = workers
        self.df = df
        self.csv_file_path = csv_file_path
        self.city = city

    def update_dataframe_with_results(self, query, status, date):
        restaurant_name_with_city = query.rsplit(' ', 1)[0]
        restaurant_name = restaurant_name_with_city.replace(f' {self.city}', '').strip()
        self.df.loc[self.df['Restaurant Name'].str.strip() == restaurant_name, 'Last scraping attempt'] = status
        self.df.loc[self.df['Restaurant Name'].str.strip() == restaurant_name, 'Last scraping attempt date'] = date
        # Save the updated DataFrame back to CSV
        self.df.to_csv(self.csv_file_path, index=False)

    def perform_parallel_action(self, action, args_list):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [executor.submit(action, *args) for args in args_list]
            for future in as_completed(futures):
                try:
                    query, status, date = future.result()
                    print(f"Task completed with result: {query, status, date}")
                    # Update DataFrame and save to CSV after each task
                    self.update_dataframe_with_results(query, status, date)
                except Exception as exc:
                    print(f"Task generated an exception: {exc}")

