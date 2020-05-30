#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import sqlalchemy
import urllib
import sys


# In[2]:


#Import shared functions
sys.path.append('../..')
from IPM_Shared_Code_public.Python.utils import get_config


# ### Use the config file to setup connections

# In[3]:


config = get_config('c:\Projects\config.ini')

driver = config['srv']['driver']
server = config['srv']['server']
dwh = config['db']['crowdsdb']
cred_file = config['google']['path_to_file']


# In[4]:


con_string = 'Driver={' + driver + '};Server=' + server +';Database=' + dwh + ';Trusted_Connection=Yes;'
params = urllib.parse.quote_plus(con_string)
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)


# ### Read in the excel file

# In[8]:


precincts = (pd.read_excel('C:\Data\precinct_borough.xlsx')
             .rename(columns = {'Precinct': 'police_precinct',
                                'Bureau Patrol': 'police_boro_com'}))


# In[9]:


precincts.to_sql('tbl_ref_precinct', engine, index = False, if_exists = 'append')

