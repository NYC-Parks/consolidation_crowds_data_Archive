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

create view dbo.vw_dpr_crowds_opendata as
	select l.encounter_timestamp,
		   l.park_district as district,
		   l.patroncount as numberofpeople,
		   case when l.in_playground = 1 then 'Yes'
				else 'No'
		   end as crowdinplayground,
		   l.action_taken as actiontakenbyparksemployee,
		   l.site_id as [site],
		   l.amenity as locationinpark,
		   case when r.latitude is null or r.longitude is null then null
				else geography::STGeomFromText(concat('Point(', cast(r.longitude as nvarchar), ' ', cast(r.latitude as nvarchar), ')'), 4326)
		   end as point
	from crowdsdb.dbo.tbl_dpr_crowds as l
	left join
		 crowdsdb.dbo.tbl_ref_sites as r
	on l.site_id = r.site_id