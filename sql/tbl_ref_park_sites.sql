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
create table crowdsdb.dbo.tbl_ref_park_sites(gispropnum nvarchar(30),
											 reported_as nvarchar(30),
											 site_id nvarchar(30) primary key,
											 obj_gisobjid numeric(38, 0),
											 site_desc nvarchar(80),
											 site_loc nvarchar(80),
											 desc_location nvarchar(113),
											 park_borough nvarchar(13),
											 park_district nvarchar(15),
											 police_precinct nvarchar(3),
											 police_boro_com nvarchar(15),
											 communityboard nvarchar(100),
											 gis_source nvarchar(26),
											 active bit)


