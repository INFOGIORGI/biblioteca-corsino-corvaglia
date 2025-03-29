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
        print(session)
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
        user = request.form.get("username")
        data = request.form.get("data")
        email = request.form.get("email")
        if session["userType"] == "admin":  
             tipo = "bibliotecario"
        elif session["userType"] == "bibliotecario":
            tipo = "utente"
       

        if(user == "" or nome =="" or cognome == "" or data == "" or email ==""):
            flash("Tutti i campi devono essere completi")
            return redirect(url_for("register"))
        
        check = getCredenziali(mysql, user)
        if check != None:
            flash("L'username è già utilizzato")
            return redirect(url_for("register"))
        str = nome + data + cognome #formata da nome, data di nascita, cognome (es. Alberto2006-08-20Corvaglia)
        pw = generate_password_hash(str)
        
        doRegister(mysql, nome, cognome, user,pw, data, email, tipo)

        return redirect(url_for("home"))
   

@app.route("/admin/")
def admin():
    return render_template("admin.html")      

@app.route("/catalogo/")
def catalogo():
    return render_template("catalogo.html")     

@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("login"))        


app.run(debug=True)