import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def plot_histogram(df, column='rating'):
    df = df.copy()
    df.replace([np.inf, -np.inf], np.nan, inplace=True)  # Replace infinities with NaN
    df.dropna(subset=[column], inplace=True)  # Drop NaN values in the column of interest

    # Calculate average and standard deviation
    average = df[column].mean()
    std = df[column].std()

    print(f"Average {column}: {average:.2f}")
    print(f"Standard deviation of {column}: {std:.2f}")

    # Set up the matplotlib figure
    plt.figure(figsize=(10, 6))

    # Generate a histogram of the data
    if pd.api.types.is_numeric_dtype(df[column]) and not pd.api.types.is_float_dtype(df[column]):
        # If the column is numeric and not float, assume it's discrete
        bins = range(int(df[column].min()), int(df[column].max()) + 2)
        sns.histplot(df[column], bins=bins, kde=False, color='skyblue', discrete=True)
        plt.xticks(bins)
    else:
        # For continuous data
        sns.histplot(df[column], kde=False, color='skyblue')
        plt.xticks()  # Let matplotlib handle the ticks

    # Add a title and labels
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')

    # Plot vertical lines for average and standard deviations
    plt.axvline(average, color='red', linestyle='--', label=f'Average: {average:.2f}')
    plt.axvline(average + std, color='green', linestyle='--', label=f'+1 STD: {average + std:.2f}')
    plt.axvline(average - std, color='blue', linestyle='--', label=f'-1 STD: {average - std:.2f}')

    # Show legend
    plt.legend()

    # Display the plot
    plt.show()
