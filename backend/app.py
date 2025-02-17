from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import json
import db

app = Flask(__name__)
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

@app.route("/cercaLibro/", methods=["GET", "POST"])
def cercaLibro():
    data = request.get_json()
    parola_chiave = data.get("parola_chiave", "")

    if not parola_chiave:
        response = {"response": "missing data"}
        return jsonify(response)
    
    print(parola_chiave)
    libri = db.cercaLibro(mysql,parola_chiave)
    response = {"response": libri}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
