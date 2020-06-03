#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import required libraries
import gspread
import sys
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import urllib
import sqlalchemy
from gspread_dataframe import set_with_dataframe
from gspread_dataframe import get_as_dataframe
import datetime


# In[2]:


#Import project specific functions
from column_map import column_map
from yesno_functions import *
from format_datetime import *


# In[3]:


#Import shared functions
sys.path.append('../..')
from IPM_Shared_Code_public.Python.google_creds_functions import create_assertion_session
from IPM_Shared_Code_public.Python.utils import get_config
from IPM_Shared_Code_public.Python.delta_functions import *
from IPM_Shared_Code_public.Python.sql_functions import *


# ### Use the config file to setup connections

# In[4]:


config = get_config('c:\Projects\config.ini')

driver = config['srv']['driver']
server = config['srv']['server']
dwh = config['db']['crowdsdb']
cred_file = config['google']['path_to_file']


# In[5]:


con_string = 'Driver={' + driver + '};Server=' + server +';Database=' + dwh + ';Trusted_Connection=Yes;'
params = urllib.parse.quote_plus(con_string)
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)


# ### Execute the function to get the renamed columns for this sheet

# In[6]:


#Call the column map function to get the dictionary to be used for renaming and subsetting the columns
col_rename = column_map('crowds_dpr')


# In[7]:


#Because of duplicate column names these columns are renamed based on the column index and the keys and 
#values need to be switched
col_rename = {v[0]: k for k, v in col_rename.items()}


# In[8]:


cols = list(col_rename.values())


# ### Read the site reference list from SQL

# In[9]:


sql = 'select * from crowdsdb.dbo.tbl_ref_sites'


# In[10]:


site_ref = pd.read_sql(con = engine, sql = sql)[['site_id', 'desc_location']]


# ### Read the current data from SQL

# In[43]:


sql = 'select * from crowdsdb.dbo.tbl_dpr_crowds'


# In[44]:


crowds_sql = (pd.read_sql(con = engine, sql = sql)
              .drop(columns = ['crowds_id'])
              .fillna(value = np.nan, axis = 1))


# In[45]:


format_datetime(crowds_sql, 'encounter_timestamp')


# In[46]:


float_cols = ['patroncount', 'in_playground']
for c in float_cols:
    crowds_sql[c] = crowds_sql[c].astype(float)


# In[47]:


crowds_sql.head()


# In[48]:


sql_cols = list(crowds_sql.columns.values)


# In[49]:


hash_rows(crowds_sql, exclude_cols = ['site_id', 'encounter_timestamp'], hash_name = 'row_hash')


# ### Read the latest data from Google Sheets

# In[20]:


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
client = gspread.authorize(creds)


# In[21]:


sheet = client.open('Crowds_Combined')


# In[22]:


ws = sheet.worksheet('Sheet1')


# In[23]:


crowds = (get_as_dataframe(ws, evaluate_formulas = True, header= None)
          #Always remove row 0 with the column headers
          .iloc[1:]
          .rename(columns = col_rename)
          .fillna(value = np.nan, axis = 1))[cols]


# In[24]:


#Remove the rows where there timestamp is null because these sheets have extra rows full of nulls
crowds = crowds[crowds['encounter_timestamp'].notnull()]


# In[25]:


format_datetime(crowds, 'encounter_timestamp')


# In[26]:


crowds.head()


# In[27]:


yesno = ['in_playground']


# In[28]:


yesno_cols(crowds, yesno)


# In[29]:


crowds = crowds.merge(site_ref, how = 'left', on = 'desc_location')[sql_cols]


# In[30]:


hash_rows(crowds, exclude_cols = ['site_id', 'encounter_timestamp'], hash_name = 'row_hash')


# In[31]:


crowds.head()


# ### Find the deltas based on the row hashes

# In[50]:


crowds_deltas = (check_deltas(new_df = crowds, old_df = crowds_sql, on = ['encounter_timestamp', 'site_id'], 
                              hash_name = 'row_hash', dml_col = 'dml_verb'))[sql_cols + ['dml_verb']]


# In[51]:


crowds_deltas.head()


# In[52]:


crowds_inserts = crowds_deltas[crowds_deltas['dml_verb'] == 'I'][sql_cols]


# In[53]:


crowds_inserts.head()


# In[54]:


crowds_inserts.to_sql('tbl_dpr_crowds', engine, index = False, if_exists = 'append')


# In[55]:


crowds_updates = crowds_deltas[crowds_deltas['dml_verb'] == 'U'][sql_cols]


# In[56]:


crowds_updates.head()


# In[58]:


sql_update(crowds_updates, 'tbl_dpr_crowds', engine, ['encounter_timestamp', 'site_id'])

