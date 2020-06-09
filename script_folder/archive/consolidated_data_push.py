#!/usr/bin/env python
# coding: utf-8

# In[11]:


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


# In[12]:


#Import shared functions
sys.path.append('../..')
from IPM_Shared_Code_public.Python.google_creds_functions import create_assertion_session
from IPM_Shared_Code_public.Python.utils import get_config
from IPM_Shared_Code_public.Python.delta_functions import *
from IPM_Shared_Code_public.Python.sql_functions import *


# ### Use the config file to setup connections

# In[13]:


config = get_config('c:\Projects\config.ini')

driver = config['srv']['driver']
server = config['srv']['server']
dwh = config['db']['crowdsdb']
cred_file = config['google']['path_to_file']


# In[14]:


con_string = 'Driver={' + driver + '};Server=' + server +';Database=' + dwh + ';Trusted_Connection=Yes;'
params = urllib.parse.quote_plus(con_string)
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)


# ### Send the data to the sheet

# In[15]:


sql = 'select * from crowdsdb.dbo.vw_consolidated_socialdistancing'


# In[16]:


consolidated_sql = (pd.read_sql(con = engine, sql = sql)
                    .fillna(value = np.nan, axis = 1))


# In[17]:


consolidated_sql.tail()


# In[18]:


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
client = gspread.authorize(creds)


# In[19]:


sheet = client.open('consolidated_social_distancing_data')


# In[20]:


ws = sheet.worksheet('Data')


# In[21]:


set_with_dataframe(ws, consolidated_sql, include_index = False, 
                   include_column_header = True, resize = True, allow_formulas = False)

