from flask import Flask, render_template,request , redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
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

#password dell'admin sicurissima
admin_pass = generate_password_hash("admin")
print(admin_pass)

@app.route("/")
def home():
    if not session.get("name"):
        return redirect(url_for("login"))
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

        account = getCredenziali(mysql,user, pw)
        if account == None:
            flash("L'account non esiste")
            return redirect(url_for("login"))
        
        else: 
            hash = account[0][3]
            if check_password_hash(hash, pw) == False:
                flash("La password inserita non è corretta")
                return redirect(url_for("login"))

        session["username"] = user
        session["userType"] = account[0][6]
        return redirect(url_for("home"))

@app.route("/bibliotecario/")
def bibliotecario():
    return render_template("bibliotecario.html")      

@app.route("/admin/")
def admin():
    return render_template("admin.html")      

@app.route("/catalogo/")
def catalogo():
    return render_template("catalogo.html")     

@app.route("/logout/")
def logout():
    return redirect(url_for("login"))        

            


app.run(debug=True)