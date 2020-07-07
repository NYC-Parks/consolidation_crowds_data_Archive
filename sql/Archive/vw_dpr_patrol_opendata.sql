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

create or alter view dbo.vw_dpr_patrol_opendata as
	select l.encounter_datetime,
		   l.site_id,
		   r.site_desc,
		   l.park_division,
		   l.visit_reason,
		   l.patrol_method,
		   l.encounter_type,
		   r2.simplified_encounter_type,
		   l.closed_amenity,
		   l.closed_patroncount,
		   case when l.closed_education= 1 then 'Yes'
				when l.closed_education = 0 then 'No'
				else null
		   end as closed_education,
		   case when l.closed_outcome= 1 then 'Yes'
				when l.closed_outcome = 0 then 'No'
				else null
		   end as closed_outcome,
		   case when l.closed_pdcontact= 1 then 'Yes'
				when l.closed_pdcontact = 0 then 'No'
				else null
		   end as closed_pdcontact,
		   l.sd_patronscomplied,
		   l.sd_patronsnocomply,
		   l.sd_amenity,
		   case when l.sd_pdcontact= 1 then 'Yes'
				when l.sd_pdcontact = 0 then 'No'
				else null
		   end as sd_pdcontact,
		   l.summonscount_a01,
		   l.summonscount_a03,
		   l.summonscount_a04,
		   l.summonscount_a22,
		   l.other_summonscount,
		   l.borough,
		   case when r.latitude is null or r.longitude is null then null
				else geography::STGeomFromText(concat('Point(', cast(r.longitude as nvarchar), ' ', cast(r.latitude as nvarchar), ')'), 4326)
		   end as point
	from crowdsdb.dbo.tbl_dpr_patrol as l
	left join
		 crowdsdb.dbo.tbl_ref_sites as r
	on l.site_id = r.site_id
	left join
		 crowdsdb.dbo.tbl_ref_encounter_type as r2
	on l.encounter_type = r2.encounter_type;