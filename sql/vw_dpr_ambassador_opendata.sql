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

create or alter view dbo.vw_dpr_ambassador_opendata as
	select l.encounter_datetime,
		   l.site_id,
		   l.park_division,
		   l.encounter_type,
		   r.simplified_encounter_type,
		   l.sd_patronscomplied,
		   l.sd_patronsnocomply,
		   l.sd_amenity,
		   l.closed_amenity,
		   l.closed_patroncount,
		   case when l.closed_approach = 1 then 'Yes'
				when l.closed_approach = 0 then 'No'
				else null
		   end as closed_approach,
		   case when l.closed_outcome = 1 then 'Yes'
				when l.closed_outcome = 0 then 'No'
				else null
		   end as closed_outcome,
		   l.borough
	from crowdsdb.dbo.tbl_dpr_ambassador as l
	left join
		 crowdsdb.dbo.tbl_ref_encounter_type as r
	on l.encounter_type = r.encounter_type;
