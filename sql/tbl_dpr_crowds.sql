/***********************************************************************************************************************
                                                                
 created by: Annette Cheng, annette.cheng@parks.nyc.gov, innovation & performance management                                  
 modified by:                                                                 
 created date: 05/18/2020                                                   
 modified date:                                                   
                                                                   
 project: Social Distancing Data   
                                                   
 tables used: ..                                                  
         ..                                                    
         ..         
                                                    
 description: Raw data from M&O crowds apps                   
                                                                                      
***********************************************************************************************************************/
set ansi_nulls on;
go

set quoted_identifier on;
go

create table crowdsdb.dbo.tbl_dpr_crowds(crowds_id int identity(1, 1) primary key, 
										 encounter_timestamp datetime, 
										 park_district nvarchar(15),
										 patroncount int,
										 in_playground bit,
										 action_taken nvarchar(100),
										 amenity nvarchar(100), 
										 comments nvarchar(1000),
										 site_id nvarchar(30) foreign key references crowdsdb.dbo.tbl_ref_park_sites(site_id),
										 borough nvarchar(13)) 
