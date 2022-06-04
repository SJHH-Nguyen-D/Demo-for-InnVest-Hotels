create user 'dennis'@'%' identified by 'foobar';
create database innvesthotels;
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, INDEX, DROP, ALTER, CREATE TEMPORARY TABLES, LOCK TABLES, REFERENCES ON innvesthotels.* to 'innvesthotels'@'%'
