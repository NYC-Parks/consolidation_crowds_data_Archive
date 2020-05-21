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


# In[3]:


#Import shared functions
sys.path.append('../..')
from IPM_Shared_Code_public.Python.google_creds_functions import create_assertion_session
from IPM_Shared_Code_public.Python.utils import get_config
from IPM_Shared_Code_public.Python.delta_functions import *


# ### Use the config file to setup connections

# In[4]:


config = get_config('c:\Projects\config.ini')

driver = config['srv']['driver']
server = config['srv']['server']
dwh = config['db']['crowdsdb']
cred_file = config['google']['path_to_file']


# ### Execute the function to get the columns for this sheet

# In[5]:


#Call the column map function to get the dictionary to be used for renaming and subsetting the columns
col_rename = column_map('patrol_dpr')


# In[6]:


#Because of duplicate column names these columns are renamed based on the column index and the keys and 
#values need to be switched
col_rename = {v[0]: k for k, v in col_rename.items()}


# In[7]:


cols = list(col_rename.values())


# ### Read the current data from SQL

# In[8]:


con_string = 'Driver={' + driver + '};Server=' + server +';Database=' + dwh + ';Trusted_Connection=Yes;'
params = urllib.parse.quote_plus(con_string)
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)


# In[9]:


sql = 'select * from crowdsdb.dbo.tbl_dpr_patrol'


# In[10]:


patrol_sql = (pd.read_sql(con = engine, sql = sql)
              .drop(columns = ['patrol_id'])
              .fillna(value = np.nan, axis = 1))


# In[ ]:


sql_cols = list(patrol_sql.columns.values)


# In[11]:


patrol_sql.head()


# In[12]:


hash_rows(patrol_sql, exclude_cols = ['encounter_timestamp'], hash_name = 'row_hash')


# ### Read the site reference list from SQL

# In[26]:


sql = 'select * from crowdsdb.dbo.tbl_ref_sites'


# In[ ]:


site_ref = pd.read_sql(con = engine, sql = sql)


# ### Read the latest data from Google Sheets

# In[13]:


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
client = gspread.authorize(creds)


# In[14]:


sheet = client.open('COMBINED Patrol Reporting Responses')


# In[15]:


ws = sheet.worksheet('MASTER')


# In[16]:


#patrol_hist = client.open_by_url('https://docs.google.com/spreadsheets/d/name/edit#gid=0/revisions')


# In[17]:


#patrol_hist = (get_as_dataframe(hist.worksheet('MASTER'), evaluate_formulas = True, header= 0)
#               .rename(columns = col_rename))[list(col_rename.values())]


# In[18]:


#patrol_hist = patrol_hist[patrol_hist['encounter_timestamp'].notna()]


# In[19]:


#Read the worksheet as a data frame, rename the columns and subset the columns to only include those
#in the column list
patrol = (get_as_dataframe(ws, evaluate_formulas = True, header= None)
          #Always remove row 0 with the column headers
          .iloc[1:]
          .rename(columns = col_rename)
          .fillna(value = np.nan, axis = 1))[cols]


# In[20]:


patrol.head()


# In[21]:


yesno = ['closed_education', 'closed_outcome', 'closed_summonsissued', 'closed_pdassist',
         'closed_pdcontact', 'sd_summonsissued', 'sd_pdassist', 'sd_pdcontact']


# In[22]:


yesno_cols(patrol, yesno)


# In[24]:


#Remove any rows with no data, presumably these are rows with no timestamp
patrol = patrol[patrol['encounter_timestamp'].notna()]


# In[ ]:


patrol = patrol.merge(site_ref, how = 'left', on = 'site_desc')[sql_cols]


# In[25]:


patrol.to_sql('tbl_dpr_patrol3', engine, index = False, if_exists = 'append')


# In[78]:


hash_rows(patrol, exclude_cols = ['encounter_timestamp'], hash_name = 'row_hash')


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

