# review_translator_to_croatian.py

import pandas as pd
from googletrans import Translator


class ReviewTranslatorToCroatian:
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.translator = Translator()

    def detect_and_translate(self, text):
        try:
            detected_lang = self.translator.detect(text).lang
            translated_text = text
            if detected_lang not in ('hr', 'bs', 'sr'):
                translated_text = self.translator.translate(text, src=detected_lang, dest='hr').text
        except Exception as e:
            print(f"Error during translation: {e}")
            detected_lang = None
            translated_text = None
        return detected_lang, translated_text

    def translate_reviews(self):
        df = pd.read_csv(self.input_file_path)
        translations = df['Review'].apply(self.detect_and_translate)
        df['Detected_Language'], df['Translated_Review'] = zip(*translations)
        df.to_csv(self.output_file_path, index=False)
        print(f"Translated file saved to: {self.output_file_path}")
