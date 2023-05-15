import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from unidecode import unidecode
from fuzzywuzzy import process



def read(dataset='all'):
    '''
    dataset : '2020', '2019', '2018' ,'standardized','all'
    '''
    if dataset=='all':
        df_2020 = pd.read_csv('../Dataset/2020.csv')
        df_2019=pd.read_csv('../Dataset/2019.csv')
        df_2018=pd.read_csv('../Dataset/2018.csv')
        return df_2020,df_2019,df_2018
    else:
        return pd.read_csv(f'../Dataset/{dataset}.csv')



def rename_columns(df_2020,df_2019,df_2018):
    df_2020.rename(columns = {"Position ":'Position',
                               'Yearly brutto salary (without bonus and stocks) in EUR':'Salary'}
                              , inplace = True)
    
    df_2019.rename(columns = {"Position (without seniority)":'Position',
                               'Yearly brutto salary (without bonus and stocks)':'Salary'}
                              , inplace = True)

    df_2018.rename(columns = {'Current Salary':'Salary'}
                            , inplace = True)
    

def merge(data_frames, common_columns=[]):
    return pd.concat(data_frames, ignore_index=True)[common_columns]

def write_category_freq(column_name, file_name, df):
    value_counts = df[column_name].value_counts()

    with open(file_name, 'w', encoding='utf-8') as f:
        # Sort the unique values in ascending order
        sorted_values = sorted(value_counts.index)

        # Loop through sorted unique values and their counts
        for val in sorted_values:
            count = value_counts[val]
            # Write value and count to file
            f.write(f'{val}: {count}\n')

def write_to_txt(df1, df2, col_name, file_name):
    """
    Write the value of a certain column on the same line for two dataframes to a .txt file.

    :param df1: The first input dataframe
    :param df2: The second input dataframe
    :param col_name: The name of the column to write
    :param file_name: The name of the output .txt file
    """
    # Check that the dataframes have the same number of rows
    if len(df1) != len(df2):
        raise ValueError('The dataframes must have the same number of rows')

    # Open the output file in write mode with utf-8 encoding
    with open(file_name, 'w', encoding='utf-8') as f:
        # Loop over the row count
        for i in range(len(df1)):
            # Write the value of the column on the same line for the two dataframes
            f.write(f'{df1.iloc[i][col_name]} --> {df2.iloc[i][col_name]}\n')

def clean_cities(df,filter=None):
    '''

    filter: Numeric.    
            If filter is mentioned, cities with less than this filter number
            entries are removed from the dataframe.
    '''
    df_cpy=df.copy()

  
    # split the cities by comma
    df_cpy['City']=df_cpy['City']\
    .str.split(',')\
    
    df_cpy=df_cpy.explode('City')

    corrections = {
    'Koln': 'Cologne',
    'Duesseldorf': 'Dusseldorf',
    'Dusseldurf': 'Dusseldorf',
    'Saint petersburg':'Saint-petersburg',
    'Tampere (finland)':'Tampere',
    'Kiev':'Kyiv',
    'Konstanz area':'Konstanz',
    'Munchen':'Munich',
    'Nurnberg':'Nuremberg',
    }

    # remove leading and trailing whitespaces 
    # unidecode aims to (Zürich -> Zurich)
    # capitalize the first letter of each word
    # replacements are done for consistency
    df_cpy['City'] = df_cpy['City']\
    .str.strip()\
    .apply(unidecode)\
    .str.capitalize()\
    .replace(corrections)

    if filter:
        value_counts=df_cpy['City'].value_counts()
        mask = df_cpy['City'].isin(value_counts.index[value_counts < filter])
        df_cpy = df_cpy.loc[~mask]  


    return df_cpy


def clean_positions(df):

    POSITION='Position'
    job_titles = ['Software Engineer', 'Backend Developer', 'Frontend Developer',
                  'Fullstack Developer','Mobile Developer', 'DevOps','Designer (UI/UX)',
                   'Data Scientist','ML Engineer','QA Engineer','Product Manager',
                   'Data Engineer', 'Researcher','Security Engineer','Other']
    
    def replace_cloud_with_devops(x):
        '''
        By inspecting fuzzywuzzy results we see that cloud is often matched with devops.
        This function replaces cloud with devops to reduce false matching.
        '''
        if 'cloud' in x:
            return 'DevOps'
        else:
            return x
        
    df_cpy=df.copy()

    df_cpy[POSITION] = df_cpy[POSITION].str.lower().apply(replace_cloud_with_devops)
    
    
    df_cpy=standardize(df_cpy,POSITION,job_titles)
    
    return df_cpy


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
        best_match = process.extractOne(column, titles)
        return best_match[0]

    # Apply the find_best_match function to the position column
    df[col] = df[col].apply(find_best_match)

    return df


def remove_outliers(df,column):
    # Calculate the IQR for the salary column
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define a multiplier (e.g., 1.5) to determine outliers
    multiplier = 1.5
    
    # Filter out rows where the salary is outside the IQR range
    df_without_outliers = df[(df[column] >= Q1 - multiplier * IQR) & (df[column] <= Q3 + multiplier * IQR)]
    
    return df_without_outliers


def correlation_ratio(df):
    POSITION='Position'
    SALARY='Salary'
    CITY='City'

    positions = df[POSITION].unique()
    # key: position, value: correlation ratio
    position_eta= {}

    # Calculate correlation ratio for each position
    for position in positions:
        position_df = df[df[POSITION] == position]
        grouped = position_df.groupby(CITY)[SALARY]

        city_means = grouped.mean()
        overall_mean = position_df[SALARY].mean()

        between_group = sum(grouped.count() * (city_means - overall_mean) ** 2)

        # position_df[CITY].map(city_means): 
        # it would map each city in the CITY column of position_df 
        # to its mean salary in the city_means Series
        within_group = sum((position_df[SALARY] - position_df[CITY].map(city_means)) ** 2)
        total = between_group + within_group

        eta_squared = between_group / total
        eta = np.sqrt(eta_squared)
        position_eta[position] = eta_squared
    
    data_tuples = [(k, v) for k, v in position_eta.items()]
    df = pd.DataFrame(data_tuples, columns=[POSITION, 'Correlation Ratio'])

    return df
 


def plot_single_histogram(df,column,title=None,figsize=(5,5)):
    # Calculate the frequencies of each unique value in the column
    frequencies = df[column].value_counts()

    # Sort the frequencies in descending order
    sorted_frequencies = frequencies.sort_values(ascending=False)

    # Create a figure and axis
    fig, ax = plt.subplots()

   

    # Set the background color to black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Set the axis label and tick colors to white
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Plot the sorted frequencies as a bar plot with the specified bar color and white edges
    ax.bar(sorted_frequencies.index, sorted_frequencies.values, color='#44c2b1', edgecolor='white', linewidth=1.5)


    # Add value labels to the top of each bar
    for i, value in enumerate(sorted_frequencies.values):
        x = i
        y = value
        percentage = f'{y / sum(sorted_frequencies.values) * 100:.1f}%'
        # label = f'{value}\n{percentage}'
        label = f'{value}'
        ax.text(x, y, label, ha='center', va='bottom', color='white',fontsize=10)

    # Rotate the x-axis labels by 90 degrees
    plt.xticks(rotation=90)
    
    if title:
        ax.set_title(title, color='white')
    # Show the plot
    plt.show()




def plot_box_plot(df, x_col, y_col, x_label, y_label, title):
    # Set the background color to black
    plt.style.use('dark_background')
    
    # Plot the box plot
    plt.figure(figsize=(8, 8))
    sns.boxplot(data=df, x=x_col, y=y_col, color='#44c2b1')
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=90)
    plt.show()


def plot_heatmap(df,x,y,value,title,x_label,y_label,aggfunc='mean'):

    '''
    df: dataframe
    x: first column included in the heatmap  e.g: City
    y: second column included in the heatmap  e.g: Position
    value: the value to be plotted in the heatmap e,g: Salary
    title: the title of the heatmap
    x_label: the label of the x-axis
    y_label: the label of the y-axis     
    '''
    df_cpy=df.copy()
    df_cpy.set_index(y, inplace=True)
   

    heatmap_data = df_cpy.pivot_table(values=value, index=y, columns=x, aggfunc=aggfunc)

    # Create a custom colormap
    colors = ['#ffffff', '#44c2b1']
    cmap = LinearSegmentedColormap.from_list('custom', colors,N=256)

    # Plotting the heatmap
    plt.figure(figsize=(15, 5))  # Adjust the figure size as needed
    sns.heatmap(heatmap_data, cmap=cmap, annot=True, fmt=".2f", annot_kws={'color': 'black', 'size': 8}) 
    plt.title(title)  # Add a title to the plot
    plt.xlabel(x_label)  # Add labels to the x-axis
    plt.ylabel(y_label)  # Add labels to the y-axis
    plt.show()

def plot_grid_of_bar_chart(df,col='Position', X='City', Y='Salary',col_wrap=3):
    g = sns.FacetGrid(df, col=col, col_wrap=col_wrap, sharex=False,height=4)

    # Map the sns.barplot function to each subplot to plot the bar charts
    g.map(sns.barplot, X, Y, color='#44c2b1')

    # Add titles and labels to the subplots
    g.set_titles(col_template="{col_name}", size=8, color='pink')
    g.set_axis_labels("City", "Salary",)
    g.set_xticklabels(rotation=90, size=8)


    # Show the plot
    plt.show()