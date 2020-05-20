#!/usr/bin/env python
# coding: utf-8

# In[2]:


import gspread
import sys
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import urllib
import sqlalchemy
from gspread_dataframe import set_with_dataframe
from gspread_dataframe import get_as_dataframe


# In[7]:


from column_map import column_map


# In[77]:


sys.path.append('../..')
from IPM_Shared_Code_public.Python.google_creds_functions import create_assertion_session
from IPM_Shared_Code_public.Python.utils import get_config
from IPM_Shared_Code_public.Python.delta_functions import *


# ### Use the config file to setup connections

# In[86]:


config = get_config('c:\Projects\config.ini')

driver = config['srv']['driver']
server = config['srv']['server']
dwh = config['db']['crowdsdb']
cred_file = config['google']['path_to_file']


# ### Execute the function to get the columns for this sheet

# In[97]:


#Call the column map function to get the dictionary to be used for renaming and subsetting the columns
col_rename = column_map('patrol_dpr')


# In[98]:


cols = list(col_rename.values())


# ### Read the current data from SQL

# In[100]:


con_string = 'Driver={' + driver + '};Server=' + server +';Database=' + dwh + ';Trusted_Connection=Yes;'
params = urllib.parse.quote_plus(con_string)
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)


# In[101]:


sql = 'select * from crowdsdb.dbo.tbl_dpr_patrol'


# In[113]:


patrol_sql = (pd.read_sql(con = engine, sql = sql)
              .drop(columns = ['patrol_id'])
              .fillna(value = np.nan, axis = 1))


# In[115]:


patrol_sql.head()


# In[90]:


hash_rows(patrol_sql, exclude_cols = ['encounter_timestamp'], hash_name = 'row_hash')


# ### Read the latest data from Google Sheets

# In[6]:


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
client = gspread.authorize(creds)


# In[8]:


sheet = client.open('COMBINED Patrol Reporting Responses')


# In[9]:


ws = sheet.worksheet('MASTER')


# In[84]:


#patrol_hist = client.open_by_url('https://docs.google.com/spreadsheets/d/name/edit#gid=0/revisions')


# In[85]:


#patrol_hist = (get_as_dataframe(hist.worksheet('MASTER'), evaluate_formulas = True, header= 0)
#               .rename(columns = col_rename))[list(col_rename.values())]


# In[65]:


#patrol_hist = patrol_hist[patrol_hist['encounter_timestamp'].notna()]


# In[69]:


#Read the worksheet as a data frame, rename the columns and subset the columns to only include those
#in the column list
patrol = (get_as_dataframe(ws, evaluate_formulas = True, header= 0)
          .rename(columns = col_rename)
          .fillna(value = np.nan, axis = 1))[cols]


# In[70]:


#Remove any rows with no data, presumably these are rows with no timestamp
patrol = patrol[patrol['encounter_timestamp'].notna()]


# In[78]:


hash_rows(patrol, exclude_cols = ['encounter_timestamp'], hash_name = 'row_hash')


# In[79]:


patrol.head()


# In[91]:


patrol_deltas = (check_deltas(new_df = patrol, old_df = patrol_sql, on = 'encounter_timestamp', 
                              hash_name = 'row_hash', dml_col = 'dml_verb'))


# In[92]:


patrol_inserts = patrol_deltas[patrol_deltas['dml_verb'] == 'I']


# In[94]:


patrol_inserts.head()


# In[93]:


patrol_updates = patrol_deltas[patrol_deltas['dml_verb'] == 'U']


# In[95]:


patrol_updates.head()

