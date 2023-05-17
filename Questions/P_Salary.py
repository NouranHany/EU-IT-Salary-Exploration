import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error


def compute_missing_vals(df):
    return df.isna().sum().to_frame(name='Missing Values').T

def clean_gender(df, gender):
    df[gender] = df[gender].replace('Female', 'F')
    df[gender] = df[gender].replace('Male', 'M')
    df[gender] = df[gender].replace('Diverse', 'M')
    return df

def create_category_other(df, others_count_thresh=10):
    '''category count less than 10 will be other'''
    # Extract categorical variable names
    categorical_vars = df.select_dtypes(include=['object']).columns

    # Loop over each categorical variable
    for var in categorical_vars:
        # Find categories with count less than 10
        categories_to_replace = df[var].value_counts()[df[var].value_counts() < others_count_thresh].index
        # Replace categories with 'Others'
        df[var] = df[var].apply(lambda x: 'Other' if x in categories_to_replace else x)
    return df

def hot_encode(df):
    '''one hot encode categorical columns
       Except the target column
    '''
    dummy_cols = list(set(df.columns) - set(df._get_numeric_data().columns)-set(['Body_Level']))
    return pd.get_dummies(df, columns=dummy_cols)

def encode_categorical(df):
    '''
    takes a dataframe that has categorical columns and converts them to numerical values
    '''
    new_df = df.copy()
    for col in new_df.columns:
        if(new_df[col].dtype==object):
            new_df[col]=new_df[col].astype('category').cat.codes
    return new_df

def data_split(df,validation=True):
    '''split data into train , test and validation'''
    if validation:
        train, test = train_test_split(df, test_size=0.2, random_state=42)
        test, val = train_test_split(test, test_size=0.5, random_state=42)
        return train, val, test
    else:
        train, test = train_test_split(df, test_size=0.2, random_state=42)
        return train, test
    
def get_X_y(df, target='Salary'):
    '''get X and y from dataframe'''
    X = df.drop(target, axis=1)
    y = df[target]
    return X, y


def train_model(model, X_train, y_train, X_test, y_test, verbose=True):
    model.fit(X_train, y_train)

    # Make predictions on the training and testing data
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Evaluate the model
    train_mse = mean_squared_error(y_train, y_train_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)

    if verbose:
        # Print the evaluation metrics
        print("Training MAE:", train_mae)
        print("Testing MAE:", test_mae)
        print("Training MSE:", train_mse)
        print("Testing MSE:", test_mse)
        print("")
    return model