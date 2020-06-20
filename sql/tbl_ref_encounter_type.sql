/***********************************************************************************************************************
																													   	
 Created By: Dan Gallagher, daniel.gallagher@parks.nyc.gov, Innovation & Performance Management         											   
 Modified By: <Modifier Name>																						   			          
 Created Date:  <MM/DD/YYYY>																							   
 Modified Date: <MM/DD/YYYY>																							   
											       																	   
 Project: <Project Name>	
 																							   
 Tables Used: <Database>.<Schema>.<Table Name1>																							   
 			  <Database>.<Schema>.<Table Name2>																								   
 			  <Database>.<Schema>.<Table Name3>				
			  																				   
 Description: <Lorem ipsum dolor sit amet, legimus molestiae philosophia ex cum, omnium voluptua evertitur nec ea.     
	       Ut has tota ullamcorper, vis at aeque omnium. Est sint purto at, verear inimicus at has. Ad sed dicat       
	       iudicabit. Has ut eros tation theophrastus, et eam natum vocent detracto, purto impedit appellantur te	   
	       vis. His ad sonet probatus torquatos, ut vim tempor vidisse deleniti.>  									   
																													   												
***********************************************************************************************************************/
create table crowdsdb.dbo.tbl_ref_encounter_type(encounter_type nvarchar(80) primary key,
												 simplified_encounter_type nvarchar(80))

begin transaction
	insert into crowdsdb.dbo.tbl_ref_encounter_type(encounter_type,
													simplified_encounter_type)
	values ('Everyone at this site is in compliance with social distancing', 'No Encounter'),
		   ('No encounter', 'No Encounter'),
		   ('Patrons in an area closed to the public', 'Patrons in Closed Area'),
		   ('Social distancing', 'Social Distancing'),
		   ('Social distancing (groups of 3 or more)', 'Social Distancing'),
		   ('Yes, patrons educated on social distancing (not trespassing)', 'Social Distancing'),
		   ('Yes, patrons who trespassed/violated rules', 'Patrons in Closed Area')
commit;
