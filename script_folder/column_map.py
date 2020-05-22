def column_map(form_name):
    if isinstance(form_name, str):
        #Make the form_name parameter case insensitive
        form_name = form_name.lower()
    
    else:
        raise TypeError('The form_name parameter must be a string!')
        
    #This function is a helper function that returns usable name for the columns
    #captured through the multiple Google Forms deployed for Social Distancing
    if form_name == 'patrol_dpr':
        col_map = {'encounter_timestamp': [0, 'Timestamp'],
                   'encounter_datetime': [1, 'Date & Time of Encounter/Patrol'],
                   'site_desc': [2, 'Which site are you reporting on?'],
                   'location_adddesc': [3, 'Additional Location Description/ Cross Street (optional)'],
                   'park_division': [4, 'Name of Division'],
                   'firstname_1': [5, 'First name of Employee on Patrol - 1'],
                   'lastname_1': [6, 'Last name of Employee on Patrol - 1'],
                   'firstname_2': [7, 'First name of Employee on Patrol - 2'],
                   'lastname_2': [8, 'Last name of Employee on Patrol - 2'],
                   'firstname_3': [9, 'First name of Employee on Patrol - 3'],
                   'lastname_3': [10, 'Last name of Employee on Patrol - 3'],
                   'visit_reason':[11, 'Why were you visiting the park?'],
                   'patrol_method': [12, 'What was your patrol method?'],
                   'encounter_type': [13, 'Did you encounter any patrons that were trespassing/violating rules, or needed to be educated on social distancing?'],
                   'closed_amenity': [14,'Where in a closed section of the park did you encounter the rule violator(s)?'],
                   'closed_patroncount': [15, 'How many rule-violator(s) were present?'],
                   'closed_education': [16, 'Did you educate the violator(s) on social distancing?'],
                   'closed_outcome': [17, 'Did the violator(s) leave the area after being approached?'],
                   'closed_summonsissued': [18, 'Did you issue a summons related to COVID-19?'],
                   'closed_pdassist': [19, 'Do you think you will need NYPD assistance in this area in a future reporting period?'],
                   'closed_pdcontact': [20, 'Encounters of 10+ patrons: Did you reach out to NYPD?'],
                   'closed_comments': [21, 'Additional comments (optional)'],
                   'sd_patronscomplied': [22,'How many patrons COMPLIED after receiving education/information?'],
                   'sd_patronsnocomply': [23, 'How many patrons DID NOT COMPLY after receiving education/information?'],
                   'sd_amenity': [24, 'Where in the park did you encounter this group?'],
                   'sd_summonsissued': [25, 'Did you issue a summons related to COVID-19?'],
                   'sd_pdassist': [26, 'Do you think you will need NYPD assistance in this area in a future reporting period?'],
                   'sd_pdcontact': [27, 'Encounters of 10+ patrons: Did you reach out to NYPD?'],
                   'sd_comments': [28, 'Additional comments (optional)'],
                   'summonscount_a01': [29, 'How many Type A01 - "Unauthorized presence in a park when closed to the public" did you issue?(If none, put 0)'],
                   'summonscount_a03': [30, 'How many Type A03 - "Failure to comply with directives of police, park supervisor, lifeguard, peace officer" did you issue? (If none, put 0)'],
                   'summonscount_a04': [31, 'How many Type A04 - "Failure to comply with directions/prohibitions on signs" did you issue? (If none, put 0)'],
                   'summonscount_a22': [32, 'How many Type A22 - "Disorderly behavior- unauthorized access/trespass" did you issue? (If none, put 0)'],
                   'other_summonstype': [33, 'What other type of summons did you issue? (If none, put N/A)'],
                   'other_summonscount': [34, 'How many of the other type of summons did you issue? (If none, put 0)'],
                   'borough': [35, 'Borough']}

    elif form_name == 'ambassador_dpr':
        col_map = {'encounter_timestamp': [0, 'Timestamp'],
                   'encounter_datetime': [1, 'Date & Time of Encounter'],
                   'property': [2, 'Which site are you reporting on?'],
                   'location_adddesc': [3, 'Additional Location Description/ Cross Street (optional)'],
                   'parks_division': [4, 'Name of Division'],
                   'firstname_1': [5, 'First name of Ambassador - 1'],
                   'lastname_1': [6, 'Last name of Ambassador - 1'],
                   'firstname_2': [7, 'First name of Ambassador - 2'],
                   'lastname_2': [8, 'Last name of Ambassador - 2'],
                   'firstname_3': [9, 'First name of Ambassador - 3'],
                   'lastname_3': [10, 'Last name of Ambassador - 3'],
                   'encounter_type': [11, 'Is this report regarding social distancing or patrons in an area closed to the public?'],
                   'sd_patronscomplied': [12, 'How many patrons COMPLIED after receiving education/information?'],
                   'sd_patronsnocomply': [13, 'How many patrons DID NOT COMPLY after receiving education/information?'],
                   'sd_amenity': [14, 'Where in the park did you encounter this group?'],
                   'sd_pdcontact': [15, 'SD - Encounters of 10+ non-compliant patrons: Did you reach out to NYPD?'],
                   'sd_comments': [16, 'SD - Additional comments'],
                   'closed_amenity': [17, 'Where in a closed section of the park did you encounter the rule violator(s)?'],
                   'closed_patroncount': [18, 'How many patrons were present?'],
                   'closed_approach': [19, 'Did you approach them?'],
                   'closed_outcome': [20, 'Did they leave the area?'],
                   'closed_pdcontact': [21, 'Encounters of 10+ non-compliant patrons: Did you reach out to NYPD?'],
                   'closed_comments': [22, 'Trespass - Additional comments'],
                   'borough': [23, 'Borough']}
        
    elif form_name == 'ambassador_cw':
        col_map = {'Timestamp': 'encounter_timestamp',
                   'Date & Time of Encounter': 'encounter_datetime',
                   'Which site are you reporting on?': 'property',
                   'Additional Location Description/ Cross Street (optional)': 'location_adddesc',
                   'Name of City Agency': 'cityagency',
                   'First name of Ambassador - 1': 'firstname_1',
                   'Last name of Ambassador - 1': 'lastname_1',
                   'First name of Ambassador - 2': 'firstname_2',
                   'Last name of Ambassador - 2': 'lastname_2',
                   'First name of Ambassador - 3': 'firstname_3',
                   'Last name of Ambassador - 3': 'lastname_3',
                   'Is this report regarding social distancing or patrons in an area closed to the public?': 'encounter_type',
                   'How many patrons COMPLIED after receiving education/information?': 'sd_patronscomplied',
                   'How many patrons DID NOT COMPLY after receiving education/information? ': 'sd_patronsnocomply',
                   'Where in the park did you encounter this group?': 'sd_amenity',
                   'SD - Encounters of 10+ non-compliant patrons: Did you reach out to NYPD?': 'sd_pdcontact',
                   'SD - Additional comments': 'sd_comments',
                   'Where in a closed section of the park did you encounter the rule violator(s)?': 'closed_amenity',
                   'How many patrons were present?': 'closed_patroncount',
                   'Did you approach them?': 'closed_approach',
                   'Did they leave the area?': 'closed_outcome',
                   'Encounters of 10+ non-compliant patrons: Did you reach out to NYPD?': 'closed_pdcontact',
                   'Trespass - Additional comments': 'closed_comments',
                   'Borough': 'borough'}

    elif form_name == 'crowds_dpr':
        col_map = {'Timestamp': 'encounter_timestamp',
                   'District': 'park_district',
                   'NumberOfPeople': 'patroncount',
                   'CrowdInPlayground': 'inplayground',
                   'ActionTakenByParksEmployee': 'actiontaken',
                   'LocationInPark': 'amenity',
                   'AdditionalComments': 'comments',
                   'Site': 'property',
                   'Borough': 'borough'}

    else:
        raise ValueError('The value provided for the form_name parameter must be one of the following: Patrol_DPR, Ambassador_DPR, Ambassador_CW, Crowds_DPR')
    return col_map
