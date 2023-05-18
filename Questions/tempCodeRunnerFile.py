def rename_columns(df_2020,df_2019,df_2018):
    df_2020.rename(columns = {"Position ":'Position',
                               'Yearly brutto salary (without bonus and stocks) in EUR':'Salary',
                               'Seniority level':'Seniority level'}
                              , inplace = True)
    
    df_2019.rename(columns = {"Position (without seniority)":'Position',
                               'Yearly brutto salary (without bonus and stocks)':'Salary',
                               'Seniority level':'Seniority level'}
                              , inplace = True)
    print("info is",df_2018.info())
    df_2018.rename(columns = {'Current Salary':'Salary',
                              'Your level':'Seniority level'}
                            , inplace = True)
    print(df_2018.info())