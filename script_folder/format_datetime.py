import pandas as pd
import numpy as np
import datetime

def dt_fmt(x):
    try:
        dt = x.strftime('%m-%d-%Y %H:%M:%S')
    except:
        dt = np.datetime64('NaT')
    return(dt)

def format_datetime(df, col):
      df[col] = pd.to_datetime(df[col], infer_datetime_format = True, errors = 'coerce')
      df[col] = df.apply(lambda x: dt_fmt(x[col]), axis = 1)
