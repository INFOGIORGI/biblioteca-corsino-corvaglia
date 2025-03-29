from flask import Flask, render_template,request , redirect, url_for, session, flash, abort
from flask_mysqldb import MySQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from db import *
app = Flask(__name__)

#MySql DB config
app.config["MYSQL_USER"] = "5di"
app.config["MYSQL_PASSWORD"] = "colazzo"
app.config["MYSQL_HOST"] = "138.41.20.102"
app.config["MYSQL_PORT"] = 53306
app.config["MYSQL_DB"] = "corsino_corvaglia"

mysql = MySQL(app)

#Session config
app.config["SESSION_PERMANENT"] = False     # Sessions expire when the browser is closed
app.config["SESSION_TYPE"] = "filesystem"     # Store session data in files

Session(app)

@app.route("/")
def home():
    if session.get("username"):
        session["isFirstLogin"] = getCredenziali(mysql, session["username"])[-1]
    return render_template("home.html", titolo ="Home")

@app.route("/login/", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", titolo = "Accesso")

    else: 
        user = request.form.get("username")
        pw = request.form.get("password")
        
        if(user == "" or pw == ""):
            flash("Tutti i campi devono essere completi")
            return redirect(url_for("login"))

        account = getCredenziali(mysql,user)
        if account == None:
            flash("L'account non esiste")
            return redirect(url_for("login"))
        
        else: 
            hash = account[3]
            print(hash,pw,account)
            if check_password_hash(hash, pw) == False:
                flash("La password inserita non è corretta")
                return redirect(url_for("login"))
        session["username"] = user
        session["userType"] = account[6]
        session["isFirstLogin"] = account[-1]
        
        return redirect(url_for("home"))
    

@app.route("/register/", methods = ["GET","POST"])
def register():
    if request.method == "GET":
        if session["userType"] == "utente":  
            abort(403)
        else: 
            return render_template("register.html")
    else:
        nome = request.form.get("nome")
        cognome = request.form.get("cognome")
        data = request.form.get("data")
        email = request.form.get("email")
        if session["userType"] == "admin":  
             tipo = "bibliotecario"
        elif session["userType"] == "bibliotecario":
            tipo = "utente"
       

        if nome == "" or cognome == "" or data == "" or email =="":
            flash("Tutti i campi devono essere completi")
            return redirect(url_for("register"))
        
        genPwd = nome.lower() + cognome.lower() + data.lower() #formata da nome, data di nascita, cognome (es. AlbertoCorvaglia2006-08-20)
        pw = generate_password_hash(genPwd)
        
        user = nome+cognome
        
        sameNameUsers = getSameNameUsers(mysql, nome,cognome)[0]
        if sameNameUsers>0:
            user+=str(sameNameUsers)
        
        print(user)
        doRegister(mysql, user, nome, cognome, pw, data, email, tipo)

        return redirect(url_for(session["userType"]))
   
@app.route("/password-update/", methods=["POST", "GET"])
def passwordUpdate():
    
    if not session["isFirstLogin"]:
        flash("Non è il primo login")
        return redirect(url_for("home"))
    password = request.form.get("password","")
    password_confirm = request.form.get("confirm","")
    print(password, password_confirm)
    if password == "" or password_confirm == "":
            flash("Tutti i campi devono essere completi")
            return redirect(url_for("passwordUpdate"))
    if password_confirm != password:
        flash("Le password non corrispondono")
        return redirect(url_for("passwordUpdate"))

    username = session["username"]
    password = generate_password_hash(password)
    updatePassword(mysql, username, password)

    
    return redirect(url_for("home"))

@app.route("/admin/")
def admin():
    
    if session.get("userType")=="admin":
        users = getUsers(mysql)
        return render_template("admin.html",users=users) 
    else:
        return abort(403)    
   
@app.route("/bibliotecario/")
def bibliotecario():
    if session.get("userType")=="bibliotecario":
        users = getUsers(mysql)
        return render_template("bibliotecario.html",users=users) 
    else:
        return abort(403)    
   
@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("login"))        


app.run(debug=True)