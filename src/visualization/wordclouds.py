from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


def generate_wordcloud(df, column_name, additional_stopwords=None, max_words=100, width=800, height=400):
    text = ' '.join(df[column_name].astype(str))

    if additional_stopwords is None:
        additional_stopwords = set()
    stopwords = set(STOPWORDS).union(additional_stopwords)
    wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=max_words,
                          width=width, height=height, contour_width=3, contour_color='steelblue').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def generate_wordcloud_all(text, additional_stopwords=None, max_words=100, width=800, height=400):
    if additional_stopwords is None:
        additional_stopwords = set()
    stopwords = set(STOPWORDS).union(additional_stopwords)

    interpolations = ['nearest', 'bilinear', 'bicubic', 'lanczos']

    for i, interp_method in enumerate(interpolations, start=1):
        wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=max_words,
                              width=width, height=height, contour_width=3, contour_color='steelblue').generate(text)

        # Create subplots
        plt.subplot(2, 2, i)
        plt.imshow(wordcloud, interpolation=interp_method)
        plt.title(f'Interpolation: {interp_method}')
        plt.axis('off')

    plt.tight_layout()
    plt.show()
