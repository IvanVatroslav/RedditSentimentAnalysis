import matplotlib.pyplot as plt


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

    average = df[column].mean()
    std = df[column].std()
    print(f"Average {column}: {average:.2f}")
    print(f"Standard Deviation of {column}: {std:.2f}")
