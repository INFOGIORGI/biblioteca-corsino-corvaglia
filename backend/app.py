from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
import db

app = Flask(__name__)
CORS(app, origins="*")
app.config["MYSQL_HOST"] = "138.41.20.102"
app.config["MYSQL_PORT"] = 53306
app.config["MYSQL_USER"] = "ospite"
app.config["MYSQL_DB"] = "corsino_corvaglia"
app.config["MYSQL_PASSWORD"] = "ospite"

mysql = MySQL(app)

@app.route("/addLibro/", methods=["POST"])
def addLibro():
    isbn = request.form.get("ISBN", "")
    titolo = request.form.get("titolo", "")
    genere = request.form.get("genere", "")
    autore = request.form.get("autore", "")
    corridoio = request.form.get("corridoio", "")
    scaffale = request.form.get("scaffale", "")
    ripiano = request.form.get("ripiano", "")
    stato = request.form.get("stato", "")

    if not all([isbn, titolo, genere, autore, corridoio, scaffale, ripiano, stato]):
        response = {"response": "missing data"}
        return jsonify(response)

    db.addLibro(mysql, isbn, titolo, genere, autore, corridoio, scaffale, ripiano, stato)
    response = {"response": "ok"}
    return jsonify(response)

@app.route("/cercaLibro/", methods=["POST"])
def cercaLibro():
    data = request.get_json()
    parola_chiave = data.get("parola_chiave", "")

    if not parola_chiave:
        response = {"error": "missing data"}
        return jsonify(response)

    print("Search keyword:", parola_chiave)
    # Assuming db.cercaLibro returns a list of tuples: (isbn, title, genre, id)
    libri = db.cercaLibro(mysql, parola_chiave)

    response = db.toDict(libri)
    print("Response:", response)
    return jsonify(response)

@app.route("/ordinaLibro/",methods=["POST"])
def ordinaLibro():
    data = request.get_json()
    attributo = data.get("attributo","")
    ordinamento = data.get("ordinamento","")
    print(attributo)
    print(ordinamento)
    if not all([ordinamento,attributo]):
        response = {"error":"missing data"}
        return jsonify(response)

    libri = db.ordinaLibro(mysql, attributo, ordinamento)
    
    response = db.toDict(libri)
    # print(response)
    return jsonify(response)


app.run(debug=True)
