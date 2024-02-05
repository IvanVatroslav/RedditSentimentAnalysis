import pandas as pd
import re
import emoji


class ReviewCleaner:
    def clean_review(self, text):
        # Remove specific patterns like ratings
        pattern = r'Food: \d/\d\s+\|\s+Service: \d/\d\s+\|\s+Atmosphere: \d/\d'
        cleaned_text = re.sub(pattern, '', text)
        return cleaned_text.strip()

    def count_content_chars(self, text):
        # Convert emojis to a demojized form and count
        demojized_text = emoji.demojize(text)
        emoji_count = demojized_text.count(':') // 2  # Each emoji is represented by 2 colons
        # Count alphanumeric characters directly, excluding spaces for the count
        alnum_count = sum(c.isalnum() for c in text.replace(" ", ""))
        return alnum_count + emoji_count

    def clean_csv_file(self, input_file_path, char_cutoff=20):
        # Load the CSV file
        df = pd.read_csv(input_file_path)

        # Drop rows where 'Review' column is NaN or empty
        df = df.dropna(subset=['Review'])
        df = df[df['Review'].str.strip().astype(bool)]

        # Clean the reviews by removing the ratings pattern and other undesired content
        df['Review'] = df['Review'].apply(self.clean_review)

        # Filter out reviews based on content character count, considering emojis
        df = df[df['Review'].apply(self.count_content_chars) > char_cutoff]

        # Further filter out rows where 'Review' becomes empty after cleaning
        df = df[df['Review'].str.strip().astype(bool)]

        # Define the output file path
        output_file_path = input_file_path.rsplit('.', 1)[0] + '_cleaned.csv'

        # Save the cleaned DataFrame to a new CSV file
        df.to_csv(output_file_path, index=False)
        return output_file_path

# Example usage, this part would be in your main script:
# cleaner = DataCleaner()
# input_file_path = 'reviews_and_ratings.csv'  # Replace with your actual file path
# cleaned_file_path = cleaner.clean_csv_file(input_file_path)
# print(f"Cleaned file saved to: {cleaned_file_path}")
