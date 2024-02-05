# src/visualization/visualizer.py

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Visualizer:
    @staticmethod
    def generate_wordcloud(text, additional_stopwords=set(), max_words=100, width=800, height=400):
        stopwords = set(STOPWORDS).union(additional_stopwords)
        wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=max_words,
                              width=width, height=height, contour_width=3, contour_color='steelblue').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

    @staticmethod
    def plot_histogram(df, column='Char_Count', bins=100):
        average_chars = df[column].mean()
        std_chars = df[column].std()

        print(f"Average {column}: {average_chars:.2f}")
        print(f"Standard deviation of {column}: {std_chars:.2f}")

        plt.figure(figsize=(10, 6))
        sns.histplot(df[column], bins=bins, kde=True)
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.axvline(average_chars, color='r', linestyle='--', label=f'Average: {average_chars:.2f}')
        plt.axvline(average_chars + std_chars, color='g', linestyle='--', label=f'+1 STD: {average_chars + std_chars:.2f}')
        plt.axvline(average_chars - std_chars, color='b', linestyle='--', label=f'-1 STD: {average_chars - std_chars:.2f}')
        plt.legend()
        plt.show()

    @staticmethod
    def scatter_plot(df, x_column, y_column):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=x_column, y=y_column, data=df)
        plt.title(f'Relationship Between {x_column} and {y_column}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.show()

        # Calculate the correlation coefficient
        correlation = df[[x_column, y_column]].corr()
        print(f"Correlation coefficient between {x_column} and {y_column}:\n{correlation}")

    @staticmethod
    def bar_plot(df, column='Rating'):
        plt.figure(figsize=(10, 6))
        df[column].value_counts().sort_index().plot(kind='bar', color='skyblue')
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Number of Reviews')
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

        # Print the average and standard deviation of the column
        average = df[column].mean()
        std = df[column].std()
        print(f"Average {column}: {average:.2f}")
        print(f"Standard Deviation of {column}: {std:.2f}")
