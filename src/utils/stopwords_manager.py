from typing import Set


class StopwordsManager:
    def __init__(self, base_stopwords: Set[str]):
        self.base_stopwords = set(base_stopwords)

    def update_stopwords(self, additional_stopwords: Set[str]):
        self.base_stopwords.update(additional_stopwords)

    def get_clean_text_for_wordcloud(self, text: str) -> str:
        return ' '.join([word for word in text.lower().split() if word not in self.base_stopwords])

    def get_clean_text_for_sentiment(self, text: str) -> str:
        return ' '.join([word for word in text.lower().split() if word not in self.base_stopwords])
