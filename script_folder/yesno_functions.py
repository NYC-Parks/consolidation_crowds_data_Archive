import pandas as pd
import numpy as np

#Convert Yes/No values to 1/0 values
def yesno_to_bin(row):
    if row == 'Yes':
        bin_val = 1.0
    elif row == 'No':
        bin_val = 0.0
    else:
        bin_val = np.nan
    return bin_val

#Apply the yesno_to_bin function to the specified columns of the specified dataframe
def yesno_cols(df, cols):
    for col in cols:
        col_yesno = col + '_yesno'
        #Rename all of the character columns
        df.rename(columns = {col: col_yesno}, inplace = True)
        #Apply the yesno_to_bin function to all of the columns, giving it the original column name
        df[col] = df.apply(lambda row: yesno_to_bin(row[col_yesno]), axis = 1)
        #Drop the character columns
        df.drop(columns = [col_yesno], inplace = True)
