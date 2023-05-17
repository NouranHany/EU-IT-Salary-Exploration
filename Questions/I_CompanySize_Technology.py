from statsmodels.stats.proportion import proportions_ztest
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def clean_company_size(df,company_size,filter=True):
    '''
    since dataframes are combined from several different years,
    the datasfame of 2020 is not unified with the dataframe of 2019
    in terms of company size. This function will clean the company size
    '''
    df=df.copy()
    if filter:
        df.dropna(subset=[company_size],inplace=True)
    df[company_size]=df[company_size]\
        .replace('11-50','10-50')\
        .replace('51-100','50-100')\
        .replace('101-1000','100-1000')
    
    return df


def clean_technology(df,column,filter=None):
    df=df.copy()

    df[column]=df[column]\
        .str.lower()\
        .str.split('[,/& ]')
    
  

    df=df.explode(column)
    df['id'] = df.index

    df.dropna(subset=[column],inplace=True)
    df[column]=df[column].str.strip()
    df=df[(df[column]!='') & (df[column]!='-')  
          & (df[column]!='--') &  (df[column]!='+')
          & (df[column]!='not') & (df[column]!='relevant')]

    technologies = ['java','javascript','react','c#','c++','c','.net',
                    'python','html/css','node.js','sql','typescript',
                    'angular','php','swift','bash/shell/powershell',
                    'go','kotlin','ruby','objective-c',
                    'scala','rust','elixir','clojure','kubernetes',
                    'pytorch','android','django','golang','perl']
    
    
    df=standardize(df,column,technologies)

    df[column]=df[column].replace('js','javascript')

    if filter:
        value_counts=df[column].value_counts()
        mask = df[column].isin(value_counts.index[value_counts < filter])
        df = df.loc[~mask]  
    return df

def standardize(df, col, titles):
    """
    Standardize the position column in a dataframe using fuzzy string matching.

    :df: The input dataframe
    :col: The name of the position column
    :job_titles: A list of standardized job titles
    :return: A new dataframe with standardized position column
    """
    # Create a copy of the input dataframe
    df = df.copy()

    # Define a function to find the best match for a given position
    def find_best_match(column):
        best_match = process.extractBests(column, titles)
        thresh_ratio=70
        thresh_confidence =80
        match=None
        ratios={}
        for i in range(len(best_match)):
                item=best_match[i][0] 
                confidence=best_match[i][1]
                ratio=fuzz.ratio(column,item)
                ratios[item]=ratio
                if ratio>thresh_ratio and confidence>thresh_confidence:
                     match=item
                     thresh_ratio=ratio
                     thresh_confidence=confidence
                     

        if match ==None: return column
        return match

    # Apply the find_best_match function to the position column
    df[col] = df[col].apply(find_best_match)

    return df




def plot_histogram_grid(df, column1, column2, n_cols=2, figsize=(10, 5), color='#44c2b1'):
    # Calculate the frequencies of each unique value in column1 for each unique value in column2
    frequencies = df.groupby(column2)[column1].value_counts()

    # Calculate the number of rows for the grid of subplots
    n_rows = (len(frequencies.index.levels[0]) + n_cols - 1) // n_cols

    # Create a figure and axes
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize, sharex=False, sharey=False)

    # Set the background color to black
    fig.patch.set_facecolor('black')

    plt.subplots_adjust(hspace=2.5)

    # Plot each histogram in a separate subplot
    for i, (value2, group) in enumerate(frequencies.groupby(level=0)):
        row = i // n_cols
        col = i % n_cols
        ax = axes[row][col] if n_rows > 1 else axes[col]

        # Set the facecolor and label colors to black and white
        ax.set_facecolor('black')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Plot the histogram with the specified bar color and white edges
        ax.bar(group.index.get_level_values(1), group.values, color=color, edgecolor='white', linewidth=1.5)

        # Add value labels to the top of each bar
        for j, count in enumerate(group.values):
            x = j
            y = count
            percentage = f'{y / sum(group.values) * 100:.1f}%'
            label = f'{y}\n'
            ax.text(x, y, label, ha='center', va='bottom', color='white', fontsize=10)

        # Set the title of the subplot to the value of column2
        ax.set_title(value2, color='white')

        # Rotate the x-axis labels by 90 degrees
        plt.setp(ax.get_xticklabels(), rotation=90)

    # Remove any unused subplots
    for j in range(i + 1, n_rows * n_cols):
        row = j // n_cols
        col = j % n_cols
        ax = axes[row][col] if n_rows > 1 else axes[col]
        fig.delaxes(ax)

    # Show the plot
    plt.show()


def z_test_proportion_companies(max_technology,df_cleaned,COMPANY_SIZE,BIG,MEDIUM,TECHNOLOGY):
    '''
    max_technology: the technology with the highest count in medium sized/ big sized companies
                    it is the technology we want to compare with other technologies
    '''

    df_big_companies= df_cleaned[df_cleaned[COMPANY_SIZE]==BIG]

    # Get the technology with the highest count in medium sized companies
    sample_size = len(df_big_companies)

    max_tech_count = len(df_big_companies[df_big_companies[TECHNOLOGY] == max_technology])

    # key: Technology 
    # val: True for reject Null Hypothesis 
    #      False for fail to reject Null Hypothesis
    my_dic={}
    another_dic={}
    for technology in df_big_companies[TECHNOLOGY].unique():
        if technology== max_technology:continue
        tech_count= len(df_big_companies[df_big_companies[TECHNOLOGY] == technology])
        if tech_count<10:continue

        # Perform a z-test of two proportions
        count = [max_tech_count, tech_count]
        nobs = [sample_size, sample_size]
        stat, pval = proportions_ztest(count, nobs)

        if pval/2 < 0.05 and stat>0:
            my_dic[technology]=True
            another_dic[technology]=pval/2
        else:
            my_dic[technology]=False
            another_dic[technology]=pval/2

        
    hypothesis_result=pd.DataFrame(my_dic,index=[0])
    pvals=pd.DataFrame(another_dic,index=[0])

    return hypothesis_result,pvals


