import bcrypt
import sqlite3

conn = sqlite3.connect("GameData.db")

mycursor = conn.cursor()

username = input()
pswd = input()
mycursor.execute(f'select Salt from Login where Username="{username}"')
usersalt = mycursor.fetchall()[0][0]
mycursor.execute(
    "select UserID from Login where Password=?",
    (bcrypt.hashpw(pswd.encode(), usersalt),),
)
print(mycursor.fetchall())

print(bcrypt.hashpw(pswd.encode(), usersalt))


""" 
column names: (Username text, Password text, Email text, Admin integer, Salt text

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
