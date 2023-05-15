from fuzzywuzzy import process
from fuzzywuzzy import fuzz
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