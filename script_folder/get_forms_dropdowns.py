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
from bs4 import BeautifulSoup
import requests


# In[2]:


#Import shared functions
sys.path.append('../..')
from IPM_Shared_Code_public.Python.google_creds_functions import create_assertion_session
from IPM_Shared_Code_public.Python.utils import get_config
from IPM_Shared_Code_public.Python.delta_functions import *
from IPM_Shared_Code_public.Python.sql_functions import *


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


# In[ ]:





# In[8]:


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
client = gspread.authorize(creds)


# In[49]:


sheet = client.open('Social Distancing Form URLs')


# In[50]:


ws = sheet.worksheet('Sheet1')


# In[51]:


urls = get_as_dataframe(ws, evaluate_formulas = True, header= 0)[['Form Type', 'Borough', 'URL']].iloc[0:20]


# In[36]:


#urls['URL'] = urls.apply(lambda x: x['URL'] + '/edit?usp=drive_web', axis = 1)


# In[65]:


def get_urls(urls):
    final_sites = []
    for i, v in urls.iterrows():
        #print(v['URL'])
        #Make a GET request to fetch the raw HTML content
        html_content = requests.get(v['URL']).text
    
        #Parse the html content
        html_content = BeautifulSoup(html_content)
        #print(html_content)
        sites = [[c.contents[0],
                  v['Form Type'],
                  v['Borough']] for c in html_content.find_all('span', class_='quantumWizMenuPaperselectContent exportContent')]
        #print(sites)
        final_sites = final_sites + sites
    return final_sites


# In[70]:


sites = pd.DataFrame(get_urls(urls),
                     columns = ['site_desc', 'app', 'app_borough'])   


# In[77]:


sites = sites[sites['site_desc'] != 'Choose']


# In[74]:


sites.to_sql('tbl_forms_sites', engine, index = False, if_exists = 'append')

