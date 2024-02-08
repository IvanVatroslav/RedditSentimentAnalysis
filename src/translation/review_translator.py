import pandas as pd
from googletrans import Translator
import time


class ReviewTranslator:
    def __init__(self):
        self.translator = Translator()

    def detect_and_translate(self, text, dest_language='hr', retries=3):
        for attempt in range(retries):
            try:
                detected_lang = self.translator.detect(text).lang
                if detected_lang not in ('hr', 'bs', 'sr'):
                    return detected_lang, self.translator.translate(text, src=detected_lang, dest=dest_language).text
                return detected_lang, text
            except Exception as e:
                print(f"Error during translation attempt {attempt + 1}: {e}")
                time.sleep(1)
        return None, text

    def translate_csv_file(self, input_file_path, output_file_path, language='hr'):
        df = pd.read_csv(input_file_path)
        translations = df['Review'].apply(lambda x: self.detect_and_translate(x, dest_language=language))
        df['Detected_Language'], df['Translated_Review'] = zip(*translations)
        if 'no_emojis' in input_file_path:
            parts = output_file_path.rsplit('.', 1)
            output_file_path = f"{parts[0]}_no_emojis.{parts[1]}"
        df.to_csv(output_file_path, index=False)
        print(f"Translated file saved to: {output_file_path}")
