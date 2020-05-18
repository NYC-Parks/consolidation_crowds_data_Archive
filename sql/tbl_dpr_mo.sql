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
CREATE TABLE crowdsdb.dbo.tbl_dpr_mo
  ( 
     mo_id            INT IDENTITY(1, 1) PRIMARY KEY, 
     encounter_DateTime   DATETIME, 
     district             NVARCHAR(6),
     patroncount          INT,
     in_playground        BIT,
     actiontaken          NVARCHAR(100),
     amenity              NVARCHAR(100), 
     comments             NVARCHAR(1000)
     site_id              NVARCHAR(30) FOREIGN KEY REFERENCES crowdsdb.dbo.tbl_ref_sites(site_id), 
     location_adddesc     NVARCHAR(1000), 
     borough              NVARCHAR(13) 
  ) 
