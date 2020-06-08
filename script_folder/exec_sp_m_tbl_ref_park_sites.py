#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib
import sys
import sqlalchemy


# In[2]:


#Import shared functions
sys.path.append('../..')
from IPM_Shared_Code_public.Python.utils import get_config


# In[3]:


config = get_config('c:\Projects\config.ini')

driver = config['srv']['driver']
server = config['srv']['server']
dwh = config['db']['crowdsdb']


# In[4]:


con_string = 'Driver={' + driver + '};Server=' + server +';Database=' + dwh + ';Trusted_Connection=Yes;'
params = urllib.parse.quote_plus(con_string)
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)


# In[7]:


con = engine.raw_connection()
cursor = con.cursor()
cursor.execute("exec crowdsdb.dbo.sp_m_tbl_ref_park_sites")
cursor.commit()
cursor.close()

