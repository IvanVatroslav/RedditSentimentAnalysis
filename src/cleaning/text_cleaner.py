import pandas as pd
import re
import emoji


class TextCleaner:
    @staticmethod
    def clean_review(text, remove_emojis=False):
        pattern = r'Food: \d/\d\s+\|\s+Service: \d/\d\s+\|\s+Atmosphere: \d/\d'
        cleaned_text = re.sub(pattern, '', text)
        cleaned_text = cleaned_text.replace('\n', ' ')
        if remove_emojis:
            cleaned_text = emoji.replace_emoji(cleaned_text, replace='')
        return cleaned_text.strip()

    @staticmethod
    def count_content_chars(text):
        demojized_text = emoji.demojize(text)
        emoji_count = demojized_text.count(':') // 2
        alnum_count = sum(c.isalnum() for c in text.replace(" ", ""))
        return alnum_count + emoji_count

    def clean_csv_file(self, input_file_path, output_file_path, char_cutoff=20, remove_emojis=False):
        df = pd.read_csv(input_file_path)
        df = df.dropna(subset=['Review'])
        df = df[df['Review'].str.strip().astype(bool)]
        df['Review'] = df['Review'].apply(lambda x: self.clean_review(x, remove_emojis=remove_emojis))
        df = df[df['Review'].apply(self.count_content_chars) > char_cutoff]
        df = df[df['Review'].str.strip().astype(bool)]
        if remove_emojis:
            parts = output_file_path.rsplit('.', 1)
            output_file_path = f"{parts[0]}_no_emojis.{parts[1]}"
        df.to_csv(output_file_path, index=False)
        return output_file_path

    @staticmethod
    def clean_title(title):
        # Define specific cleaning rules for titles
        title = title.strip()
        # For example, remove common prefixes like 'Pizzeria'
        title = re.sub(r'^(Pizzeria|Restaurant)\s+', '', title, flags=re.IGNORECASE)
        # Further title-specific cleaning logic can be added here
        return title

    def save_cleaned_titles(self, titles, output_file_path):
        cleaned_titles = [self.clean_title(title) for title in titles]
        df_cleaned_titles = pd.DataFrame(cleaned_titles, columns=['Cleaned Title'])
        df_cleaned_titles.to_csv(output_file_path, index=False)
        return output_file_path
