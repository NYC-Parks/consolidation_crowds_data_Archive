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
if object_id('tempdb..#allsites') is not null
	drop table #allsites
select *
into #allsites
from (select gisobjid, precinct, 'property' as gis_source
	  from parksgis.dpr.property_evw
	  union
	  select gisobjid, precinct, 'zone' as gis_source
	  from parksgis.dpr.zone_evw
	  union
	  select gisobjid, precinct, 'playground' as gis_source
	  from parksgis.dpr.playground_evw
	  union
	  select gisobjid, precinct, 'greenstreet' as gis_source
	  from parksgis.dpr.greenstreet_evw
	  union
	  /*These will be excluded, but are included for good measure because some of these sites have a 
	  obj_gisobjid/gisobjid in AMPS*/
	  select null as gisobjid, precinct, 'restrictivedeclarationsite' as gis_source
	  from parksgis.dpr.restrictivedeclarationsite_evw) as u
where gisobjid is not null and
	  gisobjid != 0

select l.gispropnum, 
	   coalesce(r3.parent_id, l.gispropnum) as reported_as,
	   l.omppropid as site_id, 
	   l.obj_gisobjid,
	   l.description as site_desc, 
	   l.location as site_loc, 
	   l.desc_location, 
	   case when left(district, 1) = 'X' then 'Bronx'
			when left(district, 1) = 'B' then 'Brooklyn'
			when left(district, 1) = 'M' then 'Manhattan'
			when left(district, 1) = 'Q' then 'Queens'
			when left(district, 1) = 'R' then 'Staten Island'
			else null
	   end as park_borough,
	   l.district as park_district, 
	   r2.police_precinct,
	   r2.police_boro_com,
	   r.gis_source,
	   l.active
--into crowdsdb.dbo.tbl_ref_park_sites
from [dataparks].dwh.dbo.vw_dailytask_property_dropdown as l
left join
	 #allsites as r
on l.obj_gisobjid = r.gisobjid
left join
	 crowdsdb.dbo.tbl_ref_precinct as r2
on r.precinct = r2.police_precinct
left join
	 dwh.dbo.tbl_ref_parent_property as r3
on l.gispropnum = r3.gispropnum
where obj_gisobjid is not null