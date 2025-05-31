import sqlite3 


db = sqlite3.connect("elite.db")  


db.execute(""" 
            create table if not exists users (
           idUser integer primary key autoincrement ,
           username varchar(30), 
           passwordUser varchar(40))
           
           """)

# information par defaut 
#db.execute("insert into users(username,passwordUser) values('elite','elite')")

db.commit()