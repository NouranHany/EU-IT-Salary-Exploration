from matplotlib import pyplot as plt
import seaborn as sns

def plt_univariate_histogram(df, cat_colname, xlabel_rotation=90, show_percentage=False):
    col_counts = df[cat_colname].value_counts()
    total_count = len(df)
    percentages = col_counts / total_count * 100

    sns.countplot(data=df, x=cat_colname, order=col_counts.index)
    plt.xticks(rotation=xlabel_rotation)
    plt.title(f'{cat_colname} Distribution')

    if show_percentage:
        # Add percentage labels to the bars
        for i, count in enumerate(col_counts):
            percentage = percentages[i]
            plt.text(i, count, f'{percentage:.2f}%', ha='center', va='bottom')
