from flask import Flask , render_template , session , redirect , request ,flash
import sqlite3 


app = Flask("__name__") 
app.secret_key = 'eliteDev' 


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
            return render_template('html/dark/form-basic.html')
      else:
            return redirect('/')
            



if  __name__ == '__main__' :
	app.run(debug = True)
