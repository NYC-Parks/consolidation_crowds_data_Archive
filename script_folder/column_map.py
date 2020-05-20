def column_map(form_name):
    if isinstance(form_name, str):
        #Make the form_name parameter case insensitive
        form_name = form_name.lower()
    
    else:
        raise TypeError('The form_name parameter must be a string!')
        
    #This function is a helper function that returns usable name for the columns
    #captured through the multiple Google Forms deployed for Social Distancing
    if form_name == 'patrol_dpr':
        col_map = {'Timestamp': 'encounter_timestamp',
                   'Date & Time of Encounter/Patrol': 'encounter_datetime',
                   'Which site are you reporting on?': 'property',
                   'Additional Location Description/ Cross Street (optional)': 'location_adddesc',
                   'Name of Division': 'park_division',
                   'First name of Employee on Patrol - 1': 'firstname_1',
                   'Last name of Employee on Patrol - 1': 'lastname_1',
                   'First name of Employee on Patrol - 2': 'firstname_2',
                   'Last name of Employee on Patrol - 2': 'lastname_2',
                   'First name of Employee on Patrol - 3': 'firstname_3',
                   'Last name of Employee on Patrol - 3': 'lastname_3',
                   'What was your patrol method?': 'patrol_method',
                   'Did you encounter any patrons that were trespassing/violating rules, or needed to be educated on social distancing?': 'encounter_type',
                   'Where in a closed section of the park did you encounter the rule violator(s)?': 'closed_amenity',
                   'How many rule-violator(s) were present?': 'closed_patroncount',
                   'Did you educate the violator(s) on social distancing?': 'closed_education',
                   'Did the violator(s) leave the area after being approached?': 'closed_outcome',
                   'Did you issue a summons related to COVID-19?': 'sd_summonsissued',
                   'Do you think you will need NYPD assistance in this area in a future reporting period?': 'sd_pdassist',
                   'Encounters of 10+ patrons: Did you reach out to NYPD?': 'sd_pdcontact',
                   'Additional comments (optional)': 'sd_comments',
                   'How many patrons COMPLIED after receiving education/information?': 'sd_patronscomplied',
                   'How many patrons DID NOT COMPLY after receiving education/information?': 'sd_patronsnocomply',
                   'Where in the park did you encounter this group?': 'sd_amenity',
                   'How many Type A01 - "Unauthorized presence in a park when closed to the public" did you issue?(If none, put 0)': 'summonscount_a01',
                   'How many Type A03 - "Failure to comply with directives of police, park supervisor, lifeguard, peace officer" did you issue? (If none, put 0)': 'summonscount_a03',
                   'How many Type A04 - "Failure to comply with directions/prohibitions on signs" did you issue? (If none, put 0)': 'summonscount_a04',
                   'How many Type A22 - "Disorderly behavior- unauthorized access/trespass" did you issue? (If none, put 0)': 'summonscount_a22',
                   'What other type of summons did you issue? (If none, put N/A)': 'other_summonstype',
                   'How many of the other type of summons did you issue? (If none, put 0)': 'other_summonscount',
                   'Borough': 'borough'}

    elif form_name == 'ambassador_dpr':
        col_map = {'Timestamp': 'encounter_timestamp',
                   'Date & Time of Encounter': 'encounter_datetime',
                   'Which site are you reporting on?': 'property',
                   'Additional Location Description/ Cross Street (optional)': 'location_adddesc',
                   'Name of Division': 'parks_division',
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
