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

create or alter view dbo.vw_consolidated_socialdistancing as
	with surveys as(
	select 'DPR Patrol' as source_survey,
		   encounter_datetime,
		   site_id,
		   location_adddesc,
		   'DPR' as city_agency,
		   encounter_type,
		   coalesce(closed_amenity, sd_amenity) as amenity,
		   patroncount,
		   borough
	from crowdsdb.dbo.tbl_dpr_patrol
	union all
	select 'DPR Ambassador' as source_survey,
		   encounter_datetime,
		   site_id,
		   location_adddesc,
		   'DPR' as city_agency,
		   encounter_type,
		   coalesce(closed_amenity, sd_amenity) as amenity,
		   patroncount,
		   borough
	from crowdsdb.dbo.tbl_dpr_ambassador
	union all
	select 'CW Ambassador' as source_survey,
		   encounter_datetime,
		   site_id,
		   location_adddesc,
		   city_agency,
		   encounter_type,
		   coalesce(closed_amenity, sd_amenity) as amenity,
		   patroncount,
		   borough
	from crowdsdb.dbo.tbl_cw_ambassador
	union all
	select 'DPR Crowds' as source_survey,
		   encounter_timestamp as encounter_datetime,
		   site_id,
		   null location_adddesc,
		   'DPR' as city_agency,
		   null encounter_type,
		   amenity,
		   patroncount,
		   borough
	from crowdsdb.dbo.tbl_dpr_crowds)

	select l.source_survey,
		   l.encounter_datetime,
		   r.gispropnum,
		   r.reported_as,
		   l.site_id,
		   r.site_desc,
		   r.park_borough,
		   l.location_adddesc,
		   l.city_agency,
		   l.encounter_type,
		   l.amenity,
		   l.patroncount,
		   r.police_precinct,
		   r.police_boro_com,
		   r.communityboard
	from surveys as l
	left join
		 crowdsdb.dbo.tbl_ref_park_sites as r
	on l.site_id = r.site_id