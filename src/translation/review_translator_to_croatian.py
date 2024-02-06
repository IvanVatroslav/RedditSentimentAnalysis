import pandas as pd
from googletrans import Translator


class ReviewTranslatorToCroatian:
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.translator = Translator()

    def detect_and_translate(self, text):
        try:
            # Detect the language of the text
            detected_lang = self.translator.detect(text).lang

            # Translate the text to Croatian if it's not already in Croatian
            translated_text = text
            if detected_lang not in ('hr', 'bs', 'sr'):
                translated_text = self.translator.translate(text, src=detected_lang, dest='hr').text

        except Exception as e:
            print(f"Error during translation: {e}")
            detected_lang = None
            translated_text = None

        return detected_lang, translated_text

    def translate_csv_file(self):
        # Load the cleaned CSV file
        df = pd.read_csv(self.input_file_path)

        # Apply detection and translation
        translations = df['Review'].apply(lambda x: self.detect_and_translate(x))

        # Split the translations into detected language and translated review
        df['Detected_Language'], df['Translated_Review'] = zip(*translations)

        # Save the DataFrame with translations to a new CSV file
        df.to_csv(self.output_file_path, index=False)
        print(f"Translated file saved to: {self.output_file_path}")


