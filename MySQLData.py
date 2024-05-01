import bcrypt
import mysql.connector


mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Skyla1234',
    database='mydatabase'
)
x = ''
mycursor = mydb.cursor()

mycursor.execute('select * from Userdata')
for i in mycursor.fetchall():
    print(i)


''' 
column names: (Username VARCHAR(255), Password VARCHAR(255), Email VARCHAR(255), Admin INT(1), Salt VARCHAR(255)

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
alter table TABLENAME add column CULUMNNAME DATATYPE'''
