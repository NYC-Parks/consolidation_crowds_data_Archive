#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


from column_map import column_map


# In[3]:


sys.path.append('../..')
from IPM_Shared_Code_public.Python.google_creds_functions import create_assertion_session
from IPM_Shared_Code_public.Python.utils import get_config
from IPM_Shared_Code_public.Python.delta_functions import *
from IPM_Shared_Code_public.Python.sql_functions import sql_update


# ### Use the config file to setup connections

# In[4]:


config = get_config('c:\Projects\config.ini')

driver = config['srv']['driver']
server = config['srv']['server']
dwh = config['db']['crowdsdb']
cred_file = config['google']['path_to_file']


# ### Create the dictionary to rename the columns

# In[5]:


col_rename = {'PROPERTY_I': 'site_id',
               'DESCRIPTIO': 'site_desc', 
               'DISTRICT': 'park_district', 
               'DESC_LOCAT': 'desc_location', 
               'Latitiude': 'latitude', 
               'Longitude': 'longitude',
               'Borough': 'borough'}


# In[6]:


cols = list(col_rename.values())


# ### Read the current data from SQL

# In[7]:


con_string = 'Driver={' + driver + '};Server=' + server +';Database=' + dwh + ';Trusted_Connection=Yes;'
params = urllib.parse.quote_plus(con_string)
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)


# In[8]:


sql = 'select * from crowdsdb.dbo.tbl_ref_sites'


# In[9]:


sites_sql = (pd.read_sql(con = engine, sql = sql)
             .fillna(value = np.nan, axis = 1))[cols]


# In[10]:


hash_rows(sites_sql, exclude_cols = ['site_id'], hash_name = 'row_hash')


# ### Read the latest data from Google Sheets

# In[11]:


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
client = gspread.authorize(creds)


# In[12]:


sheet = client.open('DailyTasks_WebMerc_Centroids')


# In[13]:


ws = sheet.worksheet('Sheet1')


# In[27]:


sites = (get_as_dataframe(ws, evaluate_formulas = True, header= 0)
         .rename(columns = col_rename)
         .fillna(value = np.nan, axis = 1))[cols]


# In[28]:


sites.head()


# In[29]:


hash_rows(sites, exclude_cols = ['site_id'], hash_name = 'row_hash')


# In[30]:


sites = sites.drop_duplicates(subset = ['site_id'], keep = False)


# ### Perform the delta check

# In[31]:


sites_deltas = (check_deltas(new_df = sites, old_df = sites_sql, on = 'site_id', 
                              hash_name = 'row_hash', dml_col = 'dml_verb'))


# In[32]:


sites_deltas.head()


# ### Slice the inserts and push them to SQL

# In[33]:


sites_inserts = sites_deltas[sites_deltas['dml_verb'] == 'I'][cols]


# In[36]:


sites_inserts.head()


# In[37]:


sites_inserts.to_sql('tbl_ref_sites', engine, index = False, if_exists = 'append')


# ### Slice the updates and push them to SQL

# In[38]:


sites_updates = sites_deltas[sites_deltas['dml_verb'] == 'U'][cols]


# In[39]:


sites_updates.head()


# In[40]:


sql_update(df = sites_updates, sql_table = 'tbl_ref_sites', engine = engine, where_col = 'site_id')

