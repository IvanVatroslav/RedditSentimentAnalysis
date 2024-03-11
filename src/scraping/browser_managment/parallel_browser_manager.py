import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class ParallelBrowserManager:
    def __init__(self, df, csv_file_path, city, workers=5):
        self.workers = workers
        self.df = df
        self.csv_file_path = csv_file_path
        self.city = city

    def update_dataframe_with_single_result(self, single_result):
        if single_result:
            query, status, date, loaded_reviews, scraped_reviews, percentage = single_result
            restaurant_name = query.replace(f" {self.city}", "").strip()

            # Ensure the DataFrame columns exist
            self.ensure_columns_exist()

            # Update the DataFrame
            conditions = self.df['Restaurant Name'].str.strip() == restaurant_name
            if conditions.any():
                self.df.loc[conditions, ['Last scraping attempt', 'Last scraping attempt date', 'Loaded Reviews',
                                         'Scraped Reviews', 'Scraping Success Percentage']] = [
                    status, pd.to_datetime(date), loaded_reviews, scraped_reviews, percentage]
                print(f"Updated: {restaurant_name}")  # For debugging
            else:
                # If the restaurant is not found, you might want to add it as a new row. Adjust as needed.
                new_row = {
                    'Restaurant Name': restaurant_name,
                    'Last scraping attempt': status,
                    'Last scraping attempt date': pd.to_datetime(date),
                    'Loaded Reviews': loaded_reviews,
                    'Scraped Reviews': scraped_reviews,
                    'Scraping Success Percentage': percentage
                }
                self.df = self.df.append(new_row, ignore_index=True)
                print(f"Added new entry for: {restaurant_name}")  # For debugging

            # Save immediately after each update or addition
            self.df.to_csv(self.csv_file_path, index=False)

    def ensure_columns_exist(self):
        required_columns = ['Restaurant Name', 'Last scraping attempt', 'Last scraping attempt date',
                            'Loaded Reviews', 'Scraped Reviews', 'Scraping Success Percentage']
        for column in required_columns:
            if column not in self.df.columns:
                if 'date' in column:
                    self.df[column] = pd.NaT
                else:
                    self.df[column] = np.nan

    def perform_parallel_action(self, action, args_list):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [executor.submit(action, *args) for args in args_list]
            for future in as_completed(futures):
                try:
                    single_result = future.result()
                    self.update_dataframe_with_single_result(single_result)
                except Exception as exc:
                    print(f"Task generated an exception: {exc}")

# Your existing setup and execution code remains unchanged
