from flask import Flask , render_template , session , redirect , request ,flash
import sqlite3 
import os


app = Flask("__name__") 
app.secret_key = 'eliteDev' 
app.config['photos'] = 'static/photos'



#login 
#
@app.route("/", methods = ['GET','POST']) 
@app.route("/login", methods = ['GET','POST'])  
def login():
    if request.method == 'POST':
          user = request.form['user']
          pwd  = request.form['pwd']

          with sqlite3.connect("elite.db") as con :
                cur = con.cursor()
                cur.execute("select * from users where username = ? and passwordUser = ?",[user,pwd])
                data = cur.fetchone()

                if data :
                      session['elite'] = True 
                      session['id']    = data[0]
                      session['username'] = data[1]

                      return redirect('/admin')
                else:
                      flash("mot de passe erronne")
	

    return render_template('html/dark/authentication-login1.html')

##
#
# page admin avec session 
@app.route('/admin')
def admin():
      if 'elite' in session:
            #compte le nombres 
            with sqlite3.connect('elite.db') as con :
                  #utilisateurs
                  user = con.cursor()
                  user.execute('select * from users')
                  dataUser = len(user.fetchall()) 

                  #candidat()s

                  candidat = con.cursor() 
                  candidat.execute("select * from candidats where sexeCand = 'M'")
                  dataCandidat = len(candidat.fetchall()) 

                  #candidate(s)

                  candidate = con.cursor() 
                  candidate.execute("select * from candidats where sexeCand = 'F'")
                  dataCandidate = len(candidate.fetchall()) 


                  return render_template('html/dark/index.html', dataUser = dataUser , dataCandidat = dataCandidat , dataCandidate = dataCandidate) 
      else:
            return redirect('/')

##
# 
# deconnexion 
# 
@app.route('/deco')
def deco():
      session.clear()
      return redirect('/') 


#
#
# enregistrement des candidats
#
@app.route('/candidat', methods = ['POST','GET'])
def candidat():
      if 'elite' in session:
            
            if request.method == 'POST':

                  noms       = request.form['noms']
                  telephone = request.form['phone']
                  sexe      = request.form['sexe']
                  communes   = request.form['communes']
                  adresse   = request.form['adresse']
                  photo      = request.files['photo']
                  datedenaissance= request.form['dn']

                  pt = os.path.join(app.config['photos'] , photo.filename)
                  photo.save(pt) 
                  #Enregistrement info
                  with sqlite3.connect('elite.db') as con:
                        #verification du numero dans la base de donne
                        num = con.cursor()
                        num.execute("select * from candidats where phoneCand = ?", [telephone])
                        data_num = num.fetchone()

                        if data_num:
                              flash(f"le numero {telephone} existe deja dans le systeme !!")
                        else:
                              cur = con.cursor()
                              cur.execute("insert into candidats(nomsCand,phoneCand,sexeCand,communesCand,adresseCand,photoCand,dateN ,userId) values(?,?,?,?,?,?,?,?)",[noms,telephone,sexe,communes,adresse,photo.filename,datedenaissance,session['id']])
                              con.commit()      


            return render_template('html/dark/form-basic.html')
      else:
            return redirect('/')
      
      

#Affichage d'info dans la table
@app.route('/lstCandidat',methods=['POST','GET'])
def afficher ():

      if 'elite' in session :

            # affichage info table
            with sqlite3.connect('elite.db') as con :

                  cur = con.cursor()
                  cur.execute('select * from candidats')
                  vue = cur.fetchall()

            return render_template('html/dark/table-datatable-basic.html',table=vue)
      else:
            return redirect('/')
      

#modification info dans table
@app.route('/modifier/<string:idcand>',methods=['POST','GET'])
def modifier(idcand):
      if 'elite' in session:

            if request.method == 'POST':

              noms = request.form['noms']
              telephone = request.form['phone']
              sexe =  request.form['sexe']
              communes = request.form['communes']
              adresse = request.form['adresse']
              photo = request.files['photo']
              datedenaissance = request.form['dn']

              pt = os.path.join(app.config['photos'] , photo.filename)
              photo.save(pt)

              with sqlite3.connect('elite.db') as con:
                    send = con.cursor()
                    send.execute('update candidats set nomscand=?, phonecand=?,  sexecand=?, communescand=?, adressecand=?, photocand=?, dateN=? where idcand=?',[noms,telephone,sexe,communes,adresse,photo.filename,datedenaissance,idcand])
                    con.commit()
                    send.close()
                    return redirect('/lstCandidat') 


            with sqlite3.connect('elite.db') as con:
                  cur= con.cursor()
                  cur.execute('select * from candidats where idcand=?',[idcand])
                  aff=cur.fetchone() 
                     

            return render_template('html/dark/modifier.html',aff=aff)

      else:
            return redirect('/')

# suppresion info table
@app.route('/supprimer/<string:idcand>', methods=['POST','GET'])
def supprimer(idcand):

      if 'elite' in session:
       
       with sqlite3.connect('elite.db') as con:
            cur = con.cursor()
            cur.execute('delete from candidats where idcand=?',[idcand])
            con.commit()
            flash('information supprimer avec succes')
            return redirect('/lstCandidat')
      

       return render_template('html/dark/table-datatable-basic.html')

      else:
            return redirect('/')

      
#enregistrement d'epreuves candidats
@app.route('/epreuves',methods=['POST','GET'])
def epreuves():
      if 'elite' in session:
            
            if request.method == 'POST':
               epreuve=request.form['epreuve']
               cotes=request.form['cotes']

               with sqlite3.connect('elite.db') as con:
                     
                     cur=con.cursor()
                     cur.execute('insert into epreuves(libelleE,coteE) values(?,?)',[epreuve,cotes])
                     con.commit()
                     flash('Enregistrement effectuer avec succes')


            return render_template('html/dark/form-epreuve.html')

      else:
      
            return render_template('')
            


# enregistrement info epreuve
@app.route('/affepreuve',methods=['POST','GET'])
def affepreuve():
      if 'elite' in session:

            with sqlite3.connect('elite.db') as con:
                 cur = con.cursor()
                 cur.execute('select * from epreuves')
                 vue = cur.fetchall()
               

            return render_template('html/dark/table-epreuve.html',datas=vue)

      else:
            return redirect('/')






#modification

@app.route('/modifEp/<string:idE>', methods=['POST','GET'])
def modifEp(idE):

      if 'elite' in session:
          
          if request.method == 'POST':
             
             epreuve = request.form['epreuve']
             cotes = request.form['cotes']

             with sqlite3.connect('elite.db') as con:
                  send = con.cursor()
                  send.execute('update epreuves set libelleE=?, coteE=? where idE=?',[epreuve,cotes,idE])
                  con.commit()
                  send.close()

                  return redirect('/affepreuve')
             

             #db
          with sqlite3.connect('elite.db') as con:
                   
                   cur = con.cursor()
                   cur.execute('select * from epreuves where idE=?',[idE])
                   aff = cur.fetchone()
                   

                  
                
          return render_template('html/dark/modifEp.html',aff = aff)
      
      else:
            return redirect('/')
       

#suppression 
@app.route('/suppEp/<string:idE>',methods = ['POST','GET'])
def suppEp(idE):

      if 'elite' in session:

            with sqlite3.connect('elite.db') as con:

                  cur = con.cursor()
                  cur.execute('delete from epreuves where idE=?',[idE])
                  con.commit()
                  flash('information supprimer avec succes')
            
            return render_template('html/dark/table-epreuve.html')
      else:
            return redirect('/')
      

##
# 
# formulaire de cote 
# 
@app.route('/cote/<string:idEp>' , methods = ['POST','GET'])
def cote(idEp):
      if 'elite' in session:
            
            if request.method == 'POST':
                  cote = request.form['cotes']
                  max  = request.form['max'] 
                  candidat = request.form['candidat'] 

                  if cote <= max:
                        flash("ce bon")
                  else:
                        flash(f"{cote} est supperieur a {max}")      

            with sqlite3.connect('elite.db') as con :
                  call = con.cursor()
                  call.execute("select * from epreuves where idE =?",[idEp])  
                  data = call.fetchone() 

                  cur = con.cursor()
                  cur.execute('select * from candidats')
                  vue = cur.fetchall()  

            return render_template('html/dark/coteForm.html',tabcot=vue, data = data) 
      else:
            return redirect('/')      

      
    

















if  __name__ == '__main__' :
	app.run(debug = True)
