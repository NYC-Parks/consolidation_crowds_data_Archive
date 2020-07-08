
# coding: utf-8

# In[1]:


# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime
import numpy as np
from gspread import Client
from gspread_dataframe import set_with_dataframe
import urllib
import sqlalchemy
import pyodbc
import sys
import geopandas as gpd
sys.path.append('../..')
from IPM_Shared_Code_public.Python.google_creds_functions import create_assertion_session
from IPM_Shared_Code_public.Python.utils import get_config


# In[2]:


config = get_config('c:\Projects\config.ini')
driver = config['srv']['driver']
server = config['srv']['server']
data_parks = config['srv']['data_parks']
dwh = config['db']['dwh']
cred_file = config['google']['path_to_file']


# # Read in Google Sheets

# In[3]:


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


# In[4]:


session = create_assertion_session(cred_file, scope)


# In[5]:


gc = Client(None, session)


# In[6]:


# gc = gspread.authorize(credentials)


# In[7]:


wks = gc.open("Crowds_Combined").sheet1


# In[8]:


wks2 = gc.open("DailyTasks_WebMerc_Centroids").sheet1


# In[9]:


# headers_wks = gc.open("Report_Headers").sheet1


# In[10]:


data = wks.get_all_values()
headers = data.pop(0)

df = pd.DataFrame(data, columns=headers)
df.head()


# In[11]:


geom = wks2.get_all_values()
headers_geom = geom.pop(0)

df2 = pd.DataFrame(geom, columns=headers_geom)
df2.head()


# In[12]:


df2.rename(columns = {'Latitiude':'Latitude'},inplace=True)


# In[13]:


df2['Latitude'] = df2['Latitude'].astype(float)


# In[14]:


df2['Longitude'] = df2['Longitude'].astype(float)


# In[15]:


geom_gdf = gpd.GeoDataFrame(df2,
                 geometry=gpd.points_from_xy(df2.Longitude, df2.Latitude),
                 crs={'init': 'epsg:4326'})


# In[16]:


geom_gdf.head()


# In[17]:


MO_Crowds = geom_gdf[['DESC_LOCAT','geometry']].merge(df, how = 'right', left_on = 'DESC_LOCAT', right_on = 'Site')


# In[18]:


MO_Crowds.head()


# # change datatype of Timestamp to datetime

# In[19]:


MO_Crowds['Timestamp'] = pd.to_datetime(MO_Crowds['Timestamp'], infer_datetime_format=True)


# In[20]:


MO_Crowds


# In[21]:


con_string = 'Driver={SQL Server};Server=dpr-vpipm001;Database=dwh;Trusted_Connection=Yes;'
params = urllib.parse.quote_plus(con_string)
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)


# In[22]:


def to_wkt(row):
    return row.wkt


# In[23]:


MO_Crowds.geometry


# In[24]:


len(df)


# In[25]:


len(MO_Crowds)


# In[26]:


MO_Crowds_to_publish = MO_Crowds[~pd.isnull(MO_Crowds['geometry'])].copy()


# In[27]:


MO_Crowds_to_publish['geometry'] = MO_Crowds_to_publish['geometry'].apply(to_wkt)


# In[28]:


MO_Crowds_to_publish.sort_values(by='Timestamp')


# In[29]:


MO_Crowds_to_publish.to_sql('tbl_MO_crowds', engine, if_exists='replace')


# In[30]:


con = pyodbc.connect('Driver={' + driver + '};Server=' + server +
                     ';Database=' + dwh + ';Trusted_Connection=Yes;')


# In[31]:


cursor = con.cursor()
cursor.execute("""
    alter table [dwh].[dbo].[tbl_MO_crowds] 
    alter column geometry geometry
    """)
con.commit()
cursor.close()

