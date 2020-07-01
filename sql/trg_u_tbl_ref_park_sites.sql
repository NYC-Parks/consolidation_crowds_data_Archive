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

create or alter trigger dbo.trg_u_tbl_ref_park_sites
on crowdsdb.dbo.tbl_ref_park_sites
after update as

begin transaction
	insert into crowdsdb.dbo.tbl_ref_park_sites_audit(site_id,
													  site_desc,
													  desc_location,
													  park_borough)
		select l.site_id,
			   case when l.site_desc != r.site_desc then l.site_desc
					when l.site_desc != r.site_desc and l.park_borough != r.park_borough then l.site_desc
				    else null
			   end as site_desc,
			   case when l.desc_location != r.desc_location then l.desc_location
					when l.desc_location != r.desc_location and l.park_borough != r.park_borough then l.desc_location
					else null
			   end as desc_location,
			   l.park_borough
		from deleted as l
		inner join
			 inserted as r
		on l.site_id = r.site_id
		where (l.site_desc != r.site_desc or
			   l.desc_location != r.desc_location or
			   l.park_borough != r.park_borough);
commit;
