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

create or alter trigger dbo.trg_u_tbl_dpr_patrol
on crowdsdb.dbo.tbl_dpr_patrol
after update as

begin transaction
	insert into crowdsdb.dbo.tbl_dpr_patrol_audit(patrol_id,
												  encounter_timestamp, 
												  encounter_datetime, 
												  site_id,
												  location_adddesc, 
												  park_division, 
												  visit_reason,
												  firstname_1, 
												  lastname_1, 
												  firstname_2, 
												  lastname_2, 
												  firstname_3, 
												  lastname_3, 
												  patrol_method, 
												  encounter_type, 
												  closed_amenity, 
												  closed_patroncount, 
												  closed_education, 
												  closed_outcome,
												  closed_summonsissued,
												  closed_pdassist,
												  closed_pdcontact,
												  closed_comments,
												  sd_summonsissued, 
												  sd_pdassist, 
												  sd_pdcontact, 
												  sd_comments, 
												  sd_patronscomplied, 
												  sd_patronsnocomply, 
												  sd_amenity, 
												  summonscount_a01, 
												  summonscount_a03, 
												  summonscount_a04, 
												  summonscount_a22, 
												  other_summonstype, 
												  other_summonscount, 
												  borough)

		select patrol_id,
			   encounter_timestamp, 
			   encounter_datetime, 
			   site_id,
			   location_adddesc, 
			   park_division, 
			   visit_reason,
			   firstname_1, 
			   lastname_1, 
			   firstname_2, 
			   lastname_2, 
			   firstname_3, 
			   lastname_3, 
			   patrol_method, 
			   encounter_type, 
			   closed_amenity, 
			   closed_patroncount, 
			   closed_education, 
			   closed_outcome,
			   closed_summonsissued,
			   closed_pdassist,
			   closed_pdcontact,
			   closed_comments,
			   sd_summonsissued, 
			   sd_pdassist, 
			   sd_pdcontact, 
			   sd_comments, 
			   sd_patronscomplied, 
			   sd_patronsnocomply, 
			   sd_amenity, 
			   summonscount_a01, 
			   summonscount_a03, 
			   summonscount_a04, 
			   summonscount_a22, 
			   other_summonstype, 
			   other_summonscount, 
			   borough
		from deleted;
	commit;
