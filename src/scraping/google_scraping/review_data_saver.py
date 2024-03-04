import os
import pandas as pd


class ReviewDataSaver:
    def __init__(self, data_frame):
        self.reviews_df = data_frame

    def save_reviews_to_csv(self, directory, filename='reviews_and_ratings.csv'):
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, filename)
        try:
            self.reviews_df.to_csv(filepath, index=False)
            print(f"Saved reviews to {filepath}")
        except Exception as e:
            print(f"Error saving reviews to CSV: {e}")
