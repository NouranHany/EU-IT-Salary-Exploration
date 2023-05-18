import pandas as pd
import re
def clean_contract(df):
    cleaned_df = pd.DataFrame(columns=['Сontract duration', 'Salary'])
    for _, row in df.iterrows():
        if row['Сontract duration'] is not None :
            # split string using , / &
            values = re.split("[,&/]", row['Сontract duration'])
            for value in values:
                # remove leading and trailing spaces
                # change to lower case
                processed_value = value.strip().lower().replace(".", "")
                if ("unlimited" in processed_value):
                    cleaned_df.loc[len(cleaned_df.index)] = ['unlimited', row['Salary']]
                else:
                    cleaned_df.loc[len(cleaned_df.index)] = [processed_value, row['Salary']]
    return cleaned_df