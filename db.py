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

#creation de la table candidats
db.execute('drop table candidats')
db.execute("""
    create table if not exists candidats(
           idcand integer primary key autoincrement ,
           nomsCand varchar(50) , 
           phoneCand varchar(15),
           sexeCand varchar(15),
           communesCand varchar(30), 
           adresseCand varchar(50),
           photoCand longtext ,
           dateN date,
           dateR timestamp default current_timestamp ,
           userId integer ,
           foreign key(userId) references users(idUser))
""")
#creation de la table epreuves
db.execute("""
    create table if not exists epreuves(
           idE integer primary key autoincrement , 
           libelleE varchar(30) , 
           coteE integer 
           )

""") 

# creation de la table cotes 
#
db.execute("""
create table if not exists cotes(
           idCote integer primary key autoincrement, 
           idEpreuve integer , 
           idCandidat integer ,
           libelle integer , 
           foreign key(idEpreuve) references epreuves(idE) , 
           foreign key(idCandidat) references candidats(idcand))
""")

db.commit()