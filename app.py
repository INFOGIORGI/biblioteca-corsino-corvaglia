from flask import Flask, render_template,request , redirect, url_for
from flask_mysqldb import MySQL
from db import *
app = Flask(__name__)

app.config["MYSQL_USER"] = "5di"
app.config["MYSQL_PASSWORD"] = "colazzo"
app.config["MYSQL_HOST"] = "138.41.20.102"
app.config["MYSQL_PORT"] = 53306
app.config["MYSQL_DB"] = "corsino_corvaglia"

mysql = MySQL(app)


@app.route("/")
def home():
    return render_template("home.html", titolo ="Home")

@app.route("register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", titolo = "Registrati")

    else: 
                
            


app.run(debug=True)