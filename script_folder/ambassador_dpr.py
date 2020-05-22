#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[ ]:


#Import project specific functions
from column_map import column_map
from yesno_functions import *


# In[ ]:


#Import shared functions
sys.path.append('../..')
from IPM_Shared_Code_public.Python.google_creds_functions import create_assertion_session
from IPM_Shared_Code_public.Python.utils import get_config
from IPM_Shared_Code_public.Python.delta_functions import *


# ### Use the config file to setup connections

# In[ ]:


config = get_config('c:\Projects\config.ini')

driver = config['srv']['driver']
server = config['srv']['server']
dwh = config['db']['crowdsdb']
cred_file = config['google']['path_to_file']


# 

# In[ ]:


#Call the column map function to get the dictionary to be used for renaming and subsetting the columns
col_rename = column_map('ambassador_dpr')


# In[ ]:


#Because of duplicate column names these columns are renamed based on the column index and the keys and 
#values need to be switched
col_rename = {v[0]: k for k, v in col_rename.items()}


# In[ ]:


cols = list(col_rename.values())

