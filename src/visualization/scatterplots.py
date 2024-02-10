import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def scatter_plot(df, text_column, y_column):
    df['text_length'] = df[text_column].astype(str).apply(len)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='text_length', y=y_column, data=df)
    plt.title(f'Relationship Between Length of {text_column} and {y_column}')
    plt.xlabel(f'Number of Characters in {text_column}')
    plt.ylabel(y_column)
    plt.show()
    correlation = df[['text_length', y_column]].corr()
    print(f"Correlation coefficient between Length of {text_column} and {y_column}:\n{correlation}")
