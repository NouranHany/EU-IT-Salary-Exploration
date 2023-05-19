def clean_senior_col(df,filter = 5):
    df['Seniority level'] =df['Seniority level'].str.lower()
    meaninigless_values = ['nan','no idea, there are no ranges in the firm','no level','no level ']
    df = df[~df['Seniority level'].isin(meaninigless_values)]
    for i, row in df.iterrows():
            if row['Seniority level'] in ['principal','c-level']:
                df.at[i,'Seniority level'] = 'senior'
            if row['Seniority level'] in ['lead','director','cto','vp','key','manager','work center manager','C-level executive manager']:
                df.at[i,'Seniority level'] = 'head'
            if row['Seniority level'] in ['intern','working student','entry level','student']:
                df.at[i,'Seniority level'] = 'junior'
    seniority_counts = df['Seniority level'].value_counts()
    seniority_counts = seniority_counts[seniority_counts >= filter]
    df = df[df['Seniority level'].isin(seniority_counts.index)]
    return df


company_type = 'Company type'
company_type_mapping = {
    'insurance': 'Financial/Insurance',
    'finance': 'Financial/Insurance',
    'fintech': 'Financial/Insurance',
    'ipo': 'Financial/Insurance',
    'bank': 'Financial/Insurance',
    'fin tech': 'Financial/Insurance',
    'stock market': 'Financial/Insurance',
    'financial': 'Financial/Insurance',
    'university': 'University/Research',
    'hochschule/university': 'University/Research',
    'research': 'University/Research',
    'pharma':  'University/Research',
    'industry': 'Manufacturing/Industry',
    'manufacturing': 'Manufacturing/Industry',
    'nonit, manufacturing': 'Manufacturing/Industry',
    'automotive': 'Manufacturing/Industry',
    'oem': 'Manufacturing/Industry',
    'construction': 'Manufacturing/Industry',
    'energy': 'Manufacturing/Industry',
    'semiconductor': 'Manufacturing/Industry',
    'utilities': 'Manufacturing/Industry',
    'old industry': 'Manufacturing/Industry',
    'telecom operator': 'Telecom/Communication',
    'isp': 'Telecom/Communication',
    'telecommunications': 'Telecom/Communication',
    'media': 'Media/Publishing',
    'publishing and technology': 'Media/Publishing',
    'publisher': 'Media/Publishing',
    'ecom retailer': 'ecommerce',
    'big tech': 'corporate',
    'faang': 'corporate',
    'multinational': 'corporate',
    'enterprise': 'corporate'
}
def clean_company_types(df):
    for indx, row in df.iterrows():
        if row[company_type] is not None and type(row[company_type]) is not float:
            # remove leading and trailing spaces
            # change to lower case
            processed_value = row[company_type].strip().lower().replace("-", "")
            # normalize words by grouping those with same stem
            if ("consult" in processed_value):
                processed_value = 'consultancy'
            elif("research" in processed_value or "institut" in processed_value or "education" in processed_value):
                processed_value = 'research'
            elif ("commerc" in processed_value):
                processed_value = 'ecommerce'
            elif ("corporat" in processed_value):
                processed_value = 'corporate'
            elif ("outso" in processed_value): # most probably this is outsource but to also consider mis-spellings
                processed_value = 'outsource'
            
            # Map the responder's company type to coresponding more general company type
            if processed_value in company_type_mapping:
                processed_value = company_type_mapping[processed_value]

            df.loc[indx, company_type] = processed_value
    return df