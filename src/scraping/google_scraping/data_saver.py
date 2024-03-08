import pandas as pd
from pathlib import Path


class DataSaver:
    def __init__(self, data_frame, city):
        self.data_frame = self.ensure_restaurant_name_first(data_frame)
        self.city = city

    @staticmethod
    def ensure_restaurant_name_first(data_frame):
        if 'Restaurant Name' in data_frame.columns:
            cols = ['Restaurant Name'] + [col for col in data_frame.columns if col != 'Restaurant Name']
            data_frame = data_frame[cols]
        return data_frame

    def read_existing_data(self, filepath):
        try:
            existing_data = pd.read_csv(filepath, parse_dates=['Last scraping attempt date'])
            return self.ensure_restaurant_name_first(existing_data)
        except FileNotFoundError:
            return pd.DataFrame(columns=self.data_frame.columns)

    def append_new_data(self, existing_data, new_data):
        # Ensure consistent data types for 'Last scraping attempt date'
        if 'Last scraping attempt date' in new_data.columns:
            new_data['Last scraping attempt date'] = pd.to_datetime(new_data['Last scraping attempt date'],
                                                                    errors='coerce')

        # Detect and report any misalignment before merging
        if len(existing_data.columns) != len(new_data.columns):
            print("Warning: Column count mismatch. Please check CSV formats.")

        # Append new data to existing data
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
        combined_data = combined_data.drop_duplicates(subset=['Restaurant Name'], keep='last')

        # Check for any 'Not attempted' in 'Restaurant Name' column after merge
        incorrect_entries = combined_data[combined_data['Restaurant Name'].str.contains('Not attempted', na=False)]
        if not incorrect_entries.empty:
            print("Warning: 'Not attempted' found in 'Restaurant Name' column. Review the following entries:")
            print(incorrect_entries)

        return self.ensure_restaurant_name_first(combined_data)

    def identify_new_restaurants(self, existing_data, new_data):
        existing_names = set(existing_data['Restaurant Name'])
        new_names = set(new_data['Restaurant Name'])
        new_restaurants = new_names - existing_names
        return new_restaurants

    def save_to_csv(self, filename='restaurant_list.csv'):
        project_root = (Path.cwd() / "..").resolve()
        data_directory = project_root / 'data' / self.city
        data_directory.mkdir(parents=True, exist_ok=True)
        filepath = data_directory / filename
        existing_data = self.read_existing_data(filepath)
        new_restaurants = self.identify_new_restaurants(existing_data, self.data_frame)

        if new_restaurants:
            print("New restaurants to add:")
            for restaurant in new_restaurants:
                print(f"- {restaurant}")

        updated_data = self.append_new_data(existing_data, self.data_frame)
        try:
            updated_data.to_csv(filepath, index=False)
            print(f"Saved data to {filepath}")
        except Exception as e:
            print(f"Error saving data to CSV: {e}")
