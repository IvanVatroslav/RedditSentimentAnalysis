from src.utils.stopwords_manager import StopwordsManager
from wordcloud import WordCloud
import advertools as adv
import matplotlib.pyplot as plt
croatian_stopwords = set(adv.stopwords['croatian'])
stopwords_manager = StopwordsManager(base_stopwords=croatian_stopwords)


def generate_wordcloud(df, column_name, additional_stopwords=None, max_words=100, width=800, height=400,
                       save_path=None):
    if df is None or column_name not in df.columns:
        print(f"DataFrame is None or column '{column_name}' does not exist.")
        return

    text = ' '.join(df[column_name].dropna().astype(str)).lower()

    # Update stopwords if needed
    if additional_stopwords:
        stopwords_manager.update_stopwords(additional_stopwords)

    # Get clean text using the stopwords manager
    clean_text = stopwords_manager.get_clean_text_for_wordcloud(text)

    wordcloud = WordCloud(stopwords=stopwords_manager.base_stopwords, background_color="white", max_words=max_words,
                          width=width, height=height).generate(clean_text)

    plt.figure(figsize=(width / 100, height / 100))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def generate_wordcloud_all(text, additional_stopwords=None, max_words=100, width=800, height=400):
    # Update stopwords if needed
    if additional_stopwords:
        stopwords_manager.update_stopwords(additional_stopwords)

    stopwords = stopwords_manager.base_stopwords

    interpolations = ['nearest', 'bilinear', 'bicubic', 'lanczos']

    for i, interp_method in enumerate(interpolations, start=1):
        wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=max_words,
                              width=width, height=height, contour_width=3, contour_color='steelblue').generate(text)

        plt.subplot(2, 2, i)
        plt.imshow(wordcloud, interpolation=interp_method)
        plt.title(f'Interpolation: {interp_method}')
        plt.axis('off')

    plt.tight_layout()
    plt.show()
