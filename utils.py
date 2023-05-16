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