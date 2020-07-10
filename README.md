# What's in this repository
This repo contains all scripts used to store, transform, pull and push data associated with COVID-19 social distancing Google Forms created by the Innovation and Performance Management (IPM) team at NYC Parks.

# Process Overview Light
1. User Submits Data to one of Four Google Forms
2. The Google Form Data responses are sent to Google Sheet
3. A series of [scheduled] Python Scripts pull the data from Google Sheets, processes it and insert and/or update it into a database inside of the NYC Parks network.
4. Views generate data products that are sent back to Google Sheets using python or published to the NYC Open Data Portal using python (not included in this repo).

# SQL
A SQL Server 14.0.3076.1 instance was used to create and run the database. This folder contains all the sql scripts necessary to recreate the database with the exception of the create_db.sql script. This script was excluded for security purposes. 

You may create the crowdsdb database using the SSMS (or you chosen GUI) or by writing your own create_db.sql script. If you choose the GUI remember to add REM to line 8 of the create_database.bat file. If you create your own script, make sure to both create the database and assign permissions. Once the database is created, you can execute the batchfile to deploy the entire database.

# Python
Anaconda version 4.8.1 and Python version 3.7.4 running on Windows 2012 R2 Server(yuck) were used to create and run the python scripts. 

Libraries required include:
- pandas
- numpy
- google-api-core
- google-api-python-client
- google-auth
- google-auth-httplib2
- google-auth-oauthlib
- googleapis-common-protos
- gspread


## script_folder
This folder contains .py functions that are specific to and required for this project.
- column_map.py translates (or maps) the column names from the Google Sheet to more programming friendly version of the column names used in both python and SQL. This script is required because if the same question is asked in multiple sections of a Google Form, the Google Sheet contains duplicate column names, which are admittedly not good.

- format_datetime.py allows for the consistent conversion to and formatting of datetime values throughout all of the scripts.

- yesno_functions.py allows for the consistent conversion of "Yes" and "No" column values into 0/1 integers througout all of the scripts.

- NotebookScheduler.py allows the notebooks in the daily folder to be scheduled and executed using papermill.

### daily
- exec_sp_m_tbl_ref_park_sites.ipynb executes a SQL side stored procedure that updates the list of NYC Parks areas that might be selected in the Google Forms. 

- ambassador_cw.ipynb reads the Inter-Agency Ambassador Google Forms responses and submits inserts and updates to the corresponding SQL table.

- ambassador_dpr reads the NYC Parks Ambassador Google Forms responses and submits inserts and updates to the corresponding SQL table.

- patrol_dpr reads the NYC Parks Urban Park Service Patrol, Education and Enforcement Google Forms responses and submits inserts and updates to the corresponding SQL table.

- crowds_dpr reads the NYC Parks Maintenance and Operations (M&O) Crowd Identification Google Forms responses and submits inserts and updates to the corresponding SQL table.

- consolidated_data_push.ipynb reads consoldidated data from a SQL view and pushes it to Google Sheets so that it can be utilized by the Mayor's Office of Data Analytics (MODA).
