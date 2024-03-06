import os
import pandas as pd

class ReviewDataSaver:
    def __init__(self, data_frame, query):
        self.reviews_df = data_frame
        self.query = query

    def save_reviews_to_csv(self, filename='reviews_and_ratings.csv'):
        parts = self.query.rsplit(' ', 1)
        if len(parts) == 2:
            restaurant_name, city = parts[0].replace(' ', '_'), parts[1]
        else:
            raise ValueError("Query format incorrect. Expected 'Restaurant Name City' format.")

        # Dynamically find the project root
        current_dir = os.getcwd()
        project_root = current_dir.split('RedditSentimentAnalysis', 1)[0] + 'RedditSentimentAnalysis'

        directory = os.path.join(project_root, 'data', city, restaurant_name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, filename)
        try:
            self.reviews_df.to_csv(filepath, index=False)
            print(f"Saved reviews to {filepath}")
        except Exception as e:
            print(f"Error saving reviews to CSV: {e}")
