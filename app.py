from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL
from db import DB
app = Flask(__name__)
app.config["MYSQL_HOST"] = "138.41.20.102"
app.config["MYSQL_PORT"] = 53306
app.config["MYSQL_USER"] = "ospite"
app.config["MYSQL_DB"] = "corsino_corvaglia"
app.config["MYSQL_PASSWORD"] = "ospite"

mysql = MySQL(app)
users = ['Alice', 'Bob', 'Charlie'] 

@app.route("/")
def hello():
    db = DB()
    return render_template("index.html", message='Ciao mondo!!')

@app.route("/users")
def user():
    return render_template('users.html', users=users)

@app.route("/user/<utente>")
def utente(utente):
    return render_template('profile.html', utente=utente)


app.run(debug=True)
