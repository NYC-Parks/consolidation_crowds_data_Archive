REM @echo off

REM Create the database
REM -------------------------------------------------------------------------
sqlcmd -S . -E -i create_db.sql

REM Run all the create table scripts
REM -------------------------------------------------------------------------
sqlcmd -S . -E -i tbl_ref_sites.sql

sqlcmd -S . -E -i tbl_dpr_patrol.sql

sqlcmd -S . -E -i tbl_dpr_ambassador.sql

sqlcmd -S . -E -i tbl_cw_ambassador.sql

