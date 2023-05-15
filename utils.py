from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd


#TODO: Combine 2 datasets 

def data_pre(df):
    #read 2 datasets 
    df2020 = pd.read_csv('IT Salary Survey EU  2020.csv')
    df2019 = pd.read_csv('IT Salary Survey EU 2019.csv')

    # rename the data columns
    df2020.columns = ["Timestamp", "Age", "Gender", "City", "Position", "Experience_Years", "German_Experience", "Seniority",
    "Main_Tech", "Other_Tech", "Salary", "Salary_Bonus", "Last_Year_Salary", "Last_Year_Salary_Bonus", "Vacations",
    "Employee_Status", "Contract_Duration", "Main_Language_Work", "Company_Size", "Company_Type", "Covid_Unemploy", "Covid_Part", "Covid_Support"]
    df2019.columns = ["Timestamp", "Age", "Gender", "City","Seniority", "Position", "Experience_Years", 
    "Main_Tech","Salary", "Salary_Bonus","Salary_Stock", "Last_Year_Salary", "Last_Year_Salary_Bonus","Last_Year_Salary_Stocks", "Vacations",
    "Num_Home_Office_Days", "Main_Language_Work","Company_Name","Company_Size", "Company_Type", "Contract_Duration", "Company_Business","Null"]
    
    df2020.drop([
    # drop all columns not in 2019 dataset
    'German_Experience',
    'Covid_Unemploy', 
    'Covid_Part',
    'Covid_Support',
    'Employee_Status',
    "Other_Tech"
    ], axis=1, inplace=True)
    
    df2019.drop([
    # drop all columns not in 2020 dataset
    "Salary_Stock",
    "Last_Year_Salary_Stocks",
    "Num_Home_Office_Days",
    "Company_Name",
    "Company_Business",
    "Null"
    ], axis=1, inplace=True)
    print(df2019['Company_Type'].unique())
    df2019 = df2019[["Timestamp", "Age", "Gender", "City", "Position", "Experience_Years", "Seniority",
    "Main_Tech", "Salary", "Salary_Bonus", "Last_Year_Salary", "Last_Year_Salary_Bonus", "Vacations",
    "Contract_Duration", "Main_Language_Work", "Company_Size", "Company_Type"]]
    df = pd.concat([df2020, df2019])
    df = df.apply(lambda x: x.astype(str).str.lower())
    return df

# check if the column has nan value 
def count_nan_values(data,column_name):
    count = data[column_name].isna().sum()
    return count 


# def pre_columns_values(df):
#     df = df.apply(lambda x: x.astype(str).str.lower())

#     return 

def clean_pos_col(df):
# create a list of unique position names
    positions = df['Position'].unique()
    
    # create a dictionary to store the standardized position names
    standardized_positions = {}
    
    # use fuzzy string matching to identify similar position names
    for position in positions:
        # check if the position name is already standardized
        if position in standardized_positions:
            continue
        
        # find the best match for the position name among the remaining unique positions
        matches = process.extract(position, positions, scorer=fuzz.token_sort_ratio, limit=None)
        best_match, score = max(matches, key=lambda x: x[1])
        
        # if the best match has a high similarity score, add it as a synonym of the standardized name
        if score >= 80:
            standardized_positions[position] = best_match
            for synonym in matches:
                if synonym[1] >= 80:
                    standardized_positions[synonym[0]] = best_match
        else:
            standardized_positions[position] = position
    
    # map the standardized position names to the original survey data
    df['Position'] = df['Position'].map(standardized_positions)
    for i, row in df.iterrows():
        print(row['Position'])
        if row['Position'] in ['qa engineer' , 'qa lead' , 'qa manager' , 'working student(qa)']:
            df.at[i,'Position'] = 'qa'
        if row['Position'] in ['ну или software engineer']:
            df.at[i,'Position'] = 'software engineer'
        if row['Position'] in ['software developer in test']:
            df.at[i,'Position'] = 'software tester'
        if row['Position'] in ['lead software developer']:
            df.at[i,'Position'] = 'software developer'
        if row['Position'] in ['senior data engineer' , 'data science manager' , 'data science manager' , 'analyst']:
            df.at[i,'Position'] = 'data engineer'
        if row['Position'] in ['systemadministrator']:
            df.at[i,'Position'] = 'system administrator'
    df  = df[df['Position'] !='nan']
    return df 
