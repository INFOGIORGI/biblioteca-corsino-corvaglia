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
    if session.get("isFirstLogin"):
        session["isFirstLogin"] = getCredenziali(mysql, session["username"])[-1]
    return render_template("home.html", titolo ="Home")

# -------------------------------------------------------------- GESTIONE UTENTI --------------------------------------------------------------------------------------


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
    if request.method == "POST":
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

    else:
        abort(403)
    
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
    if session.get("userType") == "bibliotecario":
        book = session.pop("book", None)  # Remove from session after retrieving
        ISBN = session.pop("ISBN", None)  # Remove from session after retrieving
        return render_template("bibliotecario.html", book=book, ISBN=ISBN)
    else:
        return abort(403)
  

#------------------------------------------------------------------------GESTIONE LIBRI-------------------------------------------------------------------------------------
@app.route("/addLibro/", methods=["GET", "POST"])
def addLibro():
    
    if request.method == "GET":
        if session.get("userType") == "utente":
            abort(403)
        return redirect(url_for("bibliotecario"))
    
    
    mod = request.form.get("mod", "") #All'inizio non specifichiamo il tipo di modale
    
    ISBN = request.form.get("ISBN", "")
    if ISBN == "":
            flash("Il campo ISBN è obbligatorio.")
            return redirect(url_for("bibliotecario"))
    
    if mod == "":
        session["ISBN"] = ISBN
        if getLibro(mysql, ISBN):
            session["book"] = "esiste"
            
        else:
            session["book"] = "nonesiste"# Il valore book serve nel frontend, per capire in quale caso ci troviamo
                      # e cambierà il valore "mod" 
        return redirect(url_for("bibliotecario"))
    
    
    elif mod == "addCopia":
        ncopie = request.form.get("ncopie", "")
        posizione = request.form.get("posizione", "")
        
        if "" in (ncopie, posizione):
            flash("Tutti i campi devono essere completi per aggiungere copie.")
            return redirect(url_for("bibliotecario"))
        
        if ncopie.isnumeric() == False:
            flash("Il numero di copie non può essere formato da lettere")
        
        ncopie = int(ncopie)
        insertCopia(mysql, ISBN, posizione, ncopie)
        flash("Copie aggiunte con successo.")
        return redirect(url_for("bibliotecario"))
    
    elif mod == "addLibro":
        titolo = request.form.get("titolo", "")
        autore = request.form.get("autore", "")
        anno_pubbl = request.form.get("anno_pubbl", "")
        genere = request.form.get("genere", "")
        posizione = request.form.get("posizione", "")
        
        
        if "" in (ISBN, titolo, autore, anno_pubbl, genere, posizione):
            flash("Tutti i campi devono essere completi per aggiungere un nuovo libro.")
            return redirect(url_for("bibliotecario"))
        
        # Gestione dell'autore: separa nome e cognome (formato "Nome Cognome")
    
        nome_autore, cognome_autore = autore.strip().split(" ", 1)
      
        

        # Verifica se l'autore esiste già nella tabella AUTORE
        cursor = mysql.connection.cursor()
        query = "SELECT ID_A FROM AUTORE WHERE Nome = %s AND Cognome = %s"
        cursor.execute(query, (nome_autore, cognome_autore))
        res = cursor.fetchone()
        if res:
            id_autore = res[0]
        else:
            # Se l'autore non esiste, lo inserisce
            query = "INSERT INTO AUTORE (Nome, Cognome) VALUES (%s, %s)"
            cursor.execute(query, (nome_autore, cognome_autore))
            mysql.connection.commit()
            id_autore = cursor.lastrowid
        cursor.close()
    
        # Inserisce il nuovo libro nel database
    
        cursor = mysql.connection.cursor()
        query = """
            INSERT INTO LIBRO (ISBN, Titolo, Autore, Genere, AnnoPub, NRicerche)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        # Inserisce l'ID dell'autore nel campo Autore
        cursor.execute(query, (ISBN, titolo, id_autore, genere, anno_pubbl, 0))
        mysql.connection.commit()
        cursor.close()
    
        
        # Inserisce il collegamento nella tabella COMITATO_DI_SCRITTURA
    
        cursor = mysql.connection.cursor()
        query = "INSERT INTO COMITATO_DI_SCRITTURA (ISBN, ID_A) VALUES (%s, %s)"
        cursor.execute(query, (ISBN, id_autore))
        mysql.connection.commit()
        cursor.close()


        # Inserisce la prima copia del nuovo libro nel catalogo
        insertCopia(mysql, ISBN, posizione, 1)
        flash("Libro aggiunto con successo.")

        
        return redirect(url_for("bibliotecario"))

        

@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("login"))        


app.run(debug=True)