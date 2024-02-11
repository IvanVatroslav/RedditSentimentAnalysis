import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import advertools as adv

croatian_stopwords = set(adv.stopwords['croatian'])


def generate_wordcloud(df, column_name, additional_stopwords=None, max_words=100, width=800, height=400, save_path=None):
    if df is None or column_name not in df.columns:
        print(f"DataFrame is None or column '{column_name}' does not exist.")
        return

    text = ' '.join(df[column_name].dropna().astype(str)).lower()

    if additional_stopwords:
        croatian_stopwords.update(additional_stopwords)

    clean_text = ' '.join([word for word in text.split() if word not in croatian_stopwords])

    wordcloud = WordCloud(stopwords=croatian_stopwords, background_color="white", max_words=max_words, width=width, height=height).generate(clean_text)

    plt.figure(figsize=(width/100, height/100))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def generate_wordcloud_all(text, additional_stopwords=None, max_words=100, width=800, height=400):
    if additional_stopwords is None:
        additional_stopwords = set()
    stopwords = set(STOPWORDS).union(additional_stopwords)

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
