def column_map(form_name)
    #This function is a helper function that returns usable name for the columns
    #captured through the multiple Google Forms deployed for Social Distancing
    if form_name == 'Patrol_DPR'
        col_map = {r'Timestamp': 'Patrol_Timestamp',
                   r'Date & Time of Encounter/Patrol': 'Encounter_DateTime',
                   r'Which site are you reporting on?':	'Property',
                   r'Additional Location Description/ Cross Street (optional)':	'Location_AddDesc',
                   r'Name of Division':	'Division',
                   r'First name of Employee on Patrol - 1': 'Employee1_FirstName',
                   r'Last name of Employee on Patrol - 1':	'Employee1_LastName',
                   r'First name of Employee on Patrol - 2':	'Employee2_FirstName',
                   r'Last name of Employee on Patrol - 2':	'Employee2_LastName',
                   r'First name of Employee on Patrol - 3':	'Employee3_FirstName',
                   r'Last name of Employee on Patrol - 3':	'Employee3_LastName',
                   r'What was your patrol method?':	'Patrol_Method',
                   r'Did you encounter any patrons that were trespassing/violating rules, or needed to be educated on social distancing?':	'Encounter_Type',
                   r'Where in a closed section of the park did you encounter the rule violator(s)?':	'Trespass_Amenity',
                   r'How many rule-violator(s) were present?':	'Trespass_PatronCount',
                   r'Did you educate the violator(s) on social distancing?':	'Trespass_Education',
                   r'Did the violator(s) leave the area after being approached?':	'Trespass_Outcome',
                   r'Did you issue a summons related to COVID-19?':	'Trespass_SummonsIssued',
                   r'Do you think you will need NYPD assistance in this area in a future reporting period?': 'Trespass_PDAssist',
                   r'Encounters of 10+ patrons: Did you reach out to NYPD?': 'Trespass_PDContact,'
                   r'Additional comments (optional)': 'Trespass_Comments',
                   r'How many patrons COMPLIED after receiving education/information?': 'SD_PatronsComplied',
                   r'How many patrons DID NOT COMPLY after receiving education/information?': 'SD_PatronsNoComply',
                   r'Where in the park did you encounter this group?': 'SD_Amenity',
                   r'Did you issue a summons related to COVID-19?':	'SD_SummonsIssued',
                   r'Do you think you will need NYPD assistance in this area in a future reporting period?': 'SD_PDAssist',
                   r'Encounters of 10+ patrons: Did you reach out to NYPD?': 'SD_PDContact',
                   r'Additional comments (optional)': 'SD_Comments',
                   r'How many Type A01 - "Unauthorized presence in a park when closed to the public" did you issue?(If none, put 0)': 'SummonsCount_A01',
                   r'How many Type A03 - "Failure to comply with directives of police, park supervisor, lifeguard, peace officer" did you issue? (If none, put 0)':	'SummonsCount_A03',
                   r'How many Type A04 - "Failure to comply with directions/prohibitions on signs" did you issue? (If none, put 0)': 'SummonsCount_A04',
                   r'How many Type A22 - "Disorderly behavior- unauthorized access/trespass" did you issue? (If none, put 0)': 'SummonsCount_A22',
                   r'What other type of summons did you issue? (If none, put N/A)':	'Other_SummonsType'
                   r'How many of the other type of summons did you issue? (If none, put 0)': 'Other_SummonsCount'
                   r'Borough': 'Borough'}

    elif form_name == 'Ambassador_DPR':
        col_map = {}

    elif form_name == 'Ambassador_CW':
        col_map = {}
        
    elif form_name == 'Crowds_DPR':
        col_map = {}

    else:
        raise ValueError('The value provided for the form_name parameter must be one of the following: Patrol_DPR, Ambassador_DPR, Ambassador_CW, Crowds_DPR')
    return col_map
