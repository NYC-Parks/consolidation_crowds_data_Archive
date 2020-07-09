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
use crowdsdb
go

set ansi_nulls on;
go

set quoted_identifier on;
go

create or alter view dbo.vw_consolidated_socialdistancing_opendata as
	select l.source_survey,
		   l.encounter_datetime,
		   l.gispropnum,
		   l.reported_as,
		   l.site_id as park_area_id,
		   l.site_desc as park_area_desc,
		   l.park_borough,
		   l.city_agency,
		   l.encounter_type,
		   r.simplified_encounter_type,
		   l.amenity,
		   l.patroncount,
		   l.police_precinct,
		   l.police_boro_com,
		   l.communityboard
	from crowdsdb.dbo.vw_consolidated_socialdistancing as l
	left join
		 crowdsdb.dbo.tbl_ref_encounter_type as r
	on l.encounter_type = r.encounter_type;
