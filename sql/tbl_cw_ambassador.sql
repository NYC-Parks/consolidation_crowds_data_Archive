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
create table crowdsdb.dbo.tbl_cw_ambassador(ambassador_id int identity(1,1) primary key,
											encounter_timestamp datetime, 
											encounter_datetime datetime, 
											site_id nvarchar(30) foreign key references crowdsdb.dbo.tbl_ref_sites(site_id),
											location_adddesc nvarchar(1000), 
											city_agency nvarchar(80), 
											firstname_1 nvarchar(80), 
											lastname_1 nvarchar(80), 
											firstname_2 nvarchar(80), 
											lastname_2 nvarchar(80), 
											firstname_3 nvarchar(80), 
											lastname_3 nvarchar(80), 
											encounter_type nvarchar(50), 
											sd_patronscomplied int, 
											sd_patronsnocomply int, 
											sd_amenity nvarchar(100), 
											sd_pdcontact bit, 
											sd_comments nvarchar(1000),
											closed_amenity nvarchar(100), 
											closed_patroncount int, 
											closed_approach bit, 
											closed_outcome bit,
											closed_pdcontact bit,
											closed_comments nvarchar(1000),
											borough nvarchar(13))