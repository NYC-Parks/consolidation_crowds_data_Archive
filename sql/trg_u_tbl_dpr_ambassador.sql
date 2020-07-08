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

create or alter trigger dbo.trg_u_tbl_dpr_ambassador
on crowdsdb.dbo.tbl_dpr_ambassador
after update as

begin transaction
	insert into crowdsdb.dbo.tbl_dpr_ambassador_audit(ambassador_id,
												      encounter_timestamp, 
												      encounter_datetime, 
												      site_id,
												      location_adddesc, 
												      park_division, 
												      firstname_1, 
												      lastname_1, 
												      firstname_2, 
												      lastname_2, 
												      firstname_3, 
												      lastname_3, 
												      encounter_type, 
												      sd_patronscomplied, 
												      sd_patronsnocomply, 
												      sd_amenity, 
												      sd_pdcontact, 
												      sd_comments,
												      closed_amenity, 
												      closed_patroncount, 
												      closed_approach, 
												      closed_outcome,
												      closed_pdcontact,
												      closed_comments,
												      borough)

		select ambassador_id,
			   encounter_timestamp, 
			   encounter_datetime, 
			   site_id,
			   location_adddesc, 
			   park_division, 
			   firstname_1, 
			   lastname_1, 
			   firstname_2, 
			   lastname_2, 
			   firstname_3, 
			   lastname_3, 
			   encounter_type, 
			   sd_patronscomplied, 
			   sd_patronsnocomply, 
			   sd_amenity, 
			   sd_pdcontact, 
			   sd_comments,
			   closed_amenity, 
			   closed_patroncount, 
			   closed_approach, 
			   closed_outcome,
			   closed_pdcontact,
			   closed_comments,
			   borough
		from deleted;
	commit;
