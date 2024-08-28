import bcrypt
import sqlite3
import MyVal

conn = sqlite3.connect("GameData.db")
cursor = conn.cursor()



""" 
pswd = 'BaseLogin'
Useful commands
show DATABASE,
create table TABLENAME (CULUMNNAME COLMNVARIABLETYPE(),),
insert into TABLENAME (CULUMNNAMES) values (%s),
database.commit(),
cursor.execute(),
select * from TABLENAME,
delete from TABLENAME,
drop table TABLENAME,
update TABLENAME set COLUMNNAME = NEWVALUE where CULUMNNAME = VALUE,
alter table TABLENAME add column CULUMNNAME DATATYPE"""
