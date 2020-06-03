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

create or alter procedure dbo.sp_m_tbl_ref_park_sites as
begin
	if object_id('tempdb..#allsites') is not null
		drop table #allsites
	select *
	into #allsites
	from (select gisobjid, precinct, communityboard, 'property' as gis_source
		  from parksgis.dpr.property_evw
		  union
		  select gisobjid, precinct, communityboard, 'zone' as gis_source
		  from parksgis.dpr.zone_evw
		  union
		  select gisobjid, precinct, communityboard, 'playground' as gis_source
		  from parksgis.dpr.playground_evw
		  union
		  select gisobjid, precinct, communityboard, 'greenstreet' as gis_source
		  from parksgis.dpr.greenstreet_evw
		  union
		  /*These will be excluded, but are included for good measure because some of these sites have a 
		  obj_gisobjid/gisobjid in AMPS*/
		  select null as gisobjid, precinct, communityboard, 'restrictivedeclarationsite' as gis_source
		  from parksgis.dpr.restrictivedeclarationsite_evw) as u
	where gisobjid is not null and
		  gisobjid != 0;

	if object_id('tempdb..#siteref') is not null
		drop table #siteref;

	create table #ref_park_sites(gispropnum nvarchar(30),
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
								 active bit,
								 row_hash as hashbytes('SHA2_256', concat(gispropnum, reported_as, obj_gisobjid, 
													   site_desc, site_loc, desc_location, park_borough, 
													   park_district, police_precinct, police_boro_com, communityboard,
													   gis_source, active)) persisted);

	insert into #ref_park_sites(gispropnum,
								reported_as,
								site_id,
								obj_gisobjid,
								site_desc,
								site_loc,
								desc_location,
								park_borough,
								park_district,
								police_precinct,
								police_boro_com,
								communityboard,
								gis_source,
								active)
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
			   r.communityboard,
			   r.gis_source,
			   l.active
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
		where obj_gisobjid is not null;

		begin transaction	
				merge crowdsdb.dbo.tbl_ref_park_sites as tgt using #ref_park_sites as src
					on tgt.site_id = src.site_id
					/*Include rows that matched on parks_id, but had differing row hashes or shapes and had unique, non-null parks_id values.*/
					when matched and (tgt.row_hash != src.row_hash)
						then update set tgt.gispropnum = src.gispropnum,
										tgt.reported_as = src.reported_as,
										tgt.obj_gisobjid = src.obj_gisobjid,
										tgt.site_desc = src.site_desc,
										tgt.site_loc = src.site_loc,
										tgt.desc_location = src.desc_location,
										tgt.park_borough = src.park_borough,
										tgt.park_district = src.park_district,
										tgt.police_precinct = src.police_precinct,
										tgt.police_boro_com = src.police_boro_com,
										tgt.communityboard = src.communityboard,
										tgt.gis_source = src.gis_source,
										tgt.active = src.active

					when not matched by target
						then insert(gispropnum, reported_as, site_id, obj_gisobjid, site_desc, site_loc, desc_location,
									park_borough, park_district, police_precinct, police_boro_com, communityboard,
									gis_source, active)
									values(src.gispropnum, src.reported_as, src.site_id, src.obj_gisobjid, src.site_desc, src.site_loc, src.desc_location,
										   src.park_borough, src.park_district, src.police_precinct, src.police_boro_com, src.communityboard,
											src.gis_source, src.active)
					/*when not matched by source
						then delete*/;	
			commit;
end;