import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from unidecode import unidecode
from fuzzywuzzy import process


def clean_position(df,POSITION='Position'):
    df[POSITION]=df[POSITION].str.strip().str.lower()
    df[POSITION]=df[POSITION]\
    .str.replace('devops manager','DevOps')\
    .str.replace('cloud engineer','DevOps')\
    .str.replace('cloud architect','DevOps')\
    .str.replace('sre','DevOps')\
    .str.replace('devops','DevOps')\
    .str.replace('cloud platform engineer','DevOps')\
    .str.replace('bi consultant sap/ data engineer','Data Scientist')\
    .str.replace('db developer/data analyst','Data Scientist')\
    .str.replace('big data engineer','Data Scientist')\
    .str.replace('bi developer / data engineer','Data Scientist')\
    .str.replace('head of bi','Data Scientist')\
    .str.replace('bi developer / data scientist','Data Scientist')\
    .str.replace('senior data engineer','Data Scientist')\
    .str.replace('bi consultant','Data Scientist')\
    .str.replace('bi it consultant','Data Scientist')\
    .str.replace('bi analyst','Data Scientist')\
    .str.replace('analytics engineer','Data Scientist')\
    .str.replace('data analyst','Data Scientist')\
    .str.replace('dana analyst','Data Scientist')\
    .str.replace('data architect','Data Scientist')\
    .str.replace('product analyst','Data Scientist')\
    .str.replace('researcher/ consumer insights analyst','Data Scientist')\
    .str.replace('data scientist','Data Scientist')\
    .str.replace('data engineer','Data Scientist')\
    .str.replace('working student (qa)','Software Testing')\
    .str.replace('qa engineer','Software Testing')\
    .str.replace('test manager','Software Testing')\
    .str.replace('software developer in test','Software Testing')\
    .str.replace('qa manager','Software Testing')\
    .str.replace('qa automation engineer','Software Testing')\
    .str.replace('qa lead','Software Testing')\
    .str.replace('qa manager','Software Testing')\
    .str.replace('software tester','Software Testing')\
    .str.replace('testmanager','Software Testing')\
    .str.replace('embedded software engineer','Software Engineer')\
    .str.replace('fullstack developer','Software Engineer')\
    .str.replace('full-stack developer','Software Engineer')\
    .str.replace('staff engineer','Software Engineer')\
    .str.replace('fullstack engineer, ну или software engineer','Software Engineer')\
    .str.replace('software architekt','Software Engineer')\
    .str.replace('software architect','Software Engineer')\
    .str.replace('sw architect','Software Engineer')\
    .str.replace('tech lead / full-stack','Software Engineer')\
    .str.replace('tech lead','Software Engineer')\
    .str.replace('tech leader','Software Engineer')\
    .str.replace('sap developer','Software Engineer')\
    .str.replace('sap consultant','Software Engineer')\
    .str.replace('lead software developer','Software Engineer')\
    .str.replace('lead developer','Software Engineer')\
    .str.replace('software engineer','Software Engineer')\
    .str.replace('it operations manager','IT')\
    .str.replace('head of it','IT')\
    .str.replace('support','IT')\
    .str.replace('it consulting','IT')\
    .str.replace('it manager','IT')\
    .str.replace('it spezialist','IT')\
    .str.replace('erp consultant','IT')\
    .str.replace('mobile developer','Mobile Developer')\
    .str.replace('ios developer','Mobile Developer')\
    .str.replace('technical account manager','Product Manager')\
    .str.replace('technical project manager','Product Manager')\
    .str.replace('technical business analyst','Product Manager')\
    .str.replace('project manager','Product Manager')\
    .str.replace('business analyst','Product Manager')\
    .str.replace('engineering team lead','Product Manager')\
    .replace('engineering manager','Product Manager')\
    .replace('manager','Product Manager')\
    .replace('product manager','Product Manager')\
    .str.replace('backend developer','Backend Developer')\
    .str.replace('frontend developer','Frontend Developer')\
    .str.replace('designer (ui/ux)','Designer (UI/UX)')\
    .replace('cto (ceo, cfo)','CTO')\
    .str.replace('cto','CTO')\
    .str.replace('ml engineer','ML Engineer')\
    .str.replace('machine learning engineer','ML Engineer')
    vc= df[POSITION].value_counts()
    mask =df[POSITION].isin(vc.index[vc < 5])
    df.loc[mask, POSITION] = 'Other'
    return df


# cleaning 
'''
1- principal,lead,head can be mapped to senior 
2- remove senior levels < 5
'''
def clean_senior_col(df,filter = 5):
    df['Seniority level'] =df['Seniority level'].str.lower()
    meaninigless_values = ['nan','no idea, there are no ranges in the firm ','no level','no level ', 'self employed']
    df = df[~df['Seniority level'].isin(meaninigless_values)]
    for i, row in df.iterrows():
            if row['Seniority level'] in ['principal','c-level','manager','work center manager','c-level executive manager']:
                df.at[i,'Seniority level'] = 'senior'
            if row['Seniority level'] in ['lead','director','cto','vp','key']:
                df.at[i,'Seniority level'] = 'head'
            if row['Seniority level'] in ['junior','intern','student','working student','entry level']:
                df.at[i,'Seniority level'] = 'junior'
    seniority_counts = df['Seniority level'].value_counts()
    seniority_counts = seniority_counts[seniority_counts >= filter]
    df = df[df['Seniority level'].isin(seniority_counts.index)]
    return df

def clean_years(df):
    df['Years of experience']=df['Years of experience'].astype(str).str.lower()
    df['Years of experience']=df['Years of experience']\
    .replace('1,5','1.5')\
    .replace('1 (as qa engineer) / 11 in total','11')\
    .replace('2,5','2.5')\
    .replace('15, thereof 8 as cto','15')\
    .replace('6 (not as a data scientist, but as a lab scientist)','6')\
    .replace('less than year','0.5')\
    .replace('383','5').astype(float)

    return df