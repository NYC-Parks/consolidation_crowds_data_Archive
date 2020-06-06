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
col_rename = column_map('patrol_dpr')


# In[7]:


#Because of duplicate column names these columns are renamed based on the column index and the keys and 
#values need to be switched
col_rename = {v[0]: k for k, v in col_rename.items()}


# In[8]:


cols = list(col_rename.values())


# ### Read the current data from SQL

# In[9]:


sql = 'select * from crowdsdb.dbo.tbl_dpr_patrol'


# In[10]:


patrol_sql = (pd.read_sql(con = engine, sql = sql)
              .drop(columns = ['patrol_id', 'patroncount'])
              .fillna(value = np.nan, axis = 1))


# In[11]:


format_datetime(patrol_sql, 'encounter_timestamp')
format_datetime(patrol_sql, 'encounter_datetime')


# In[12]:


sql_cols = list(patrol_sql.columns.values)


# In[13]:


float_cols = ['closed_education', 'closed_outcome', 'closed_summonsissued', 'closed_pdassist',
              'closed_pdcontact', 'sd_summonsissued', 'sd_pdassist', 'sd_pdcontact']
for c in float_cols:
    patrol_sql[c] = patrol_sql[c].astype(float)


# In[14]:


patrol_sql.head()


# In[15]:


hash_rows(patrol_sql, exclude_cols = ['site_id', 'encounter_timestamp'], hash_name = 'row_hash')


# ### Read the site reference list from SQL

# In[16]:


sql = 'select * from crowdsdb.dbo.tbl_ref_sites'


# In[17]:


site_ref = pd.read_sql(con = engine, sql = sql)[['site_id', 'site_desc', 'borough']]


# ### Read the latest data from Google Sheets

# In[18]:


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
client = gspread.authorize(creds)


# In[19]:


sheet = client.open('COMBINED Patrol Reporting Responses')


# In[20]:


ws = sheet.worksheet('MASTER')


# In[21]:


#Read the worksheet as a data frame, rename the columns and subset the columns to only include those
#in the column list
patrol = (get_as_dataframe(ws, evaluate_formulas = True, header= None)
          #Always remove row 0 with the column headers
          .iloc[1:]
          .rename(columns = col_rename)
          .fillna(value = np.nan, axis = 1))[cols]


# In[22]:


format_datetime(patrol, 'encounter_timestamp')
format_datetime(patrol, 'encounter_datetime')


# In[23]:


patrol.head()


# In[24]:


yesno = ['closed_education', 'closed_outcome', 'closed_summonsissued', 'closed_pdassist',
         'closed_pdcontact', 'sd_summonsissued', 'sd_pdassist', 'sd_pdcontact']


# In[25]:


yesno_cols(patrol, yesno)


# In[26]:


#Remove any rows with no data, presumably these are rows with no timestamp
patrol = patrol[patrol['encounter_timestamp'].notna()]


# In[27]:


patrol = patrol.merge(site_ref, how = 'left', on = ['site_desc', 'borough'])[sql_cols]


# In[28]:


hash_rows(patrol, exclude_cols = ['site_id', 'encounter_timestamp'], hash_name = 'row_hash')


# In[29]:


patrol_deltas = (check_deltas(new_df = patrol, old_df = patrol_sql, on = ['site_id', 'encounter_timestamp'], 
                              hash_name = 'row_hash', dml_col = 'dml_verb'))[sql_cols + ['dml_verb']]


# In[30]:


patrol_inserts = patrol_deltas[patrol_deltas['dml_verb'] == 'I'][sql_cols]


# In[31]:


patrol_inserts.head()


# In[32]:


patrol_inserts.to_sql('tbl_dpr_patrol', engine, index = False, if_exists = 'append')


# In[33]:


patrol_updates = patrol_deltas[patrol_deltas['dml_verb'] == 'U'][sql_cols]


# In[34]:


patrol_updates.head()


# In[35]:


sql_update(patrol_updates, 'tbl_dpr_patrol', engine, ['encounter_timestamp', 'site_id'])

