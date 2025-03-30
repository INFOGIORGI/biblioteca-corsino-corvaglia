from flask import Flask, render_template,request , redirect, url_for, session, flash, abort
from flask_mysqldb import MySQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from db import *
app = Flask(__name__)

#Configurazione credenziali DB
app.config["MYSQL_USER"] = "5di"
app.config["MYSQL_PASSWORD"] = "colazzo"
app.config["MYSQL_HOST"] = "138.41.20.102"
app.config["MYSQL_PORT"] = 53306
app.config["MYSQL_DB"] = "corsino_corvaglia"

mysql = MySQL(app)

#Configurazione sessione
app.config["SESSION_PERMANENT"] = False  
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

#URL cover libro



@app.route("/")
def home():
    if session.get("isFirstLogin"):
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
        
        insertUser(mysql, user, nome, cognome, pw, data, email, tipo)

        return redirect(url_for(session["userType"]))
   
@app.route("/updatePassword/", methods=["POST", "GET"])
def updatePasword():
    if request.method == "POST":
        if not session["isFirstLogin"]:
            flash("Non è il primo login")
            return redirect(url_for("home"))
        password = request.form.get("password","")
        password_confirm = request.form.get("confirm","")
        if password == "" or password_confirm == "":
                flash("Tutti i campi devono essere completi")
                return redirect(url_for("updatePasword"))
        if password_confirm != password:
            flash("Le password non corrispondono")
            return redirect(url_for("updatePasword"))

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
        #servono per l'add libro, il frontend si comporta diversamente in base a come sono settati
        book = session.pop("book", None)  # Remove from session after retrieving
        ISBN = session.pop("ISBN", None)  # Remove from session after retrieving
        
        copie = getCopie(mysql)
        prestiti = getPrestiti(mysql)
        return render_template("bibliotecario.html", book=book, ISBN=ISBN, copie=copie, prestiti=prestiti)
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
        
        insertLibro(mysql, ISBN, titolo, anno_pubbl, genere)    
        
        autori = autore.split(",")
        for a in autori:                                                #Scorrendo gli autori, otteniamo nome e cognome, poi verifichiamo se sono già presenti nel db
            autore = a.split(" ")                                  # altrimenti li aggiungiamo. Poi eseguo un altra query per ottenere l'id del'autore, e lo
            cognome_autore = autore[-1]                                 # colleghiamo al libro in comitato
            nome_autore = " ".join(autore[:-1])
           
            check_A = getAutore(mysql, nome_autore, cognome_autore)
            if check_A == None:
                insertAutore(mysql, nome_autore, cognome_autore)

            id_autore = getAutore(mysql, nome_autore, cognome_autore)[0]
            insertComitato(mysql, id_autore, ISBN)
                

        # Inserisce la prima copia del nuovo libro nel catalogo
        insertCopia(mysql, ISBN, posizione, 1)
        flash("Libro aggiunto con successo.")

        
        return redirect(url_for("bibliotecario"))

@app.route("/addPrestito/", methods=["GET", "POST"])
def addPrestito():
    if request.method == "GET":
        if session.get("userType") == "utente":
            abort(403)
        return redirect(url_for("bibliotecario"))
    
    username = request.form.get("username", "").strip()
    codicecopia = request.form.get("codicecopia", "").strip()
    
    if not (username and codicecopia):
        flash("Tutti i campi devono essere completi per aggiungere un prestito.")
        return redirect(url_for("bibliotecario"))
    
    user_info = getCredenziali(mysql, username)
    if not user_info:
        flash("L'username specificato non esiste.")
        return redirect(url_for("bibliotecario"))
    
    copy_info = getCopia(mysql, codicecopia)
    if not copy_info:
        flash("Il codice copia specificato non esiste.")
        return redirect(url_for("bibliotecario"))
    
    if not copiaDisponibile(mysql, codicecopia)[0]:
        flash("La copia non è disponibile per il prestito.")
        return redirect(url_for("bibliotecario"))
    
    dataInizio = date.today()
    insertPrestito(mysql, username, codicecopia, dataInizio)
    flash("Prestito aggiunto con successo.")
    
    return redirect(url_for("bibliotecario"))

@app.route("/editPrestito/", methods=["GET","POST"])
def editPrestito():
    if request.method == "GET":
        if session.get("userType") == "utente":
            abort(403)
        return redirect(url_for("bibliotecario"))
    
    codicecopia = request.form.get("codicecopia","")

    if codicecopia == "":
        flash("Inserire codice copia")
        return redirect(url_for("bibliotecario"))
    
    if not getCopia(mysql, codicecopia):
        flash("Copia inesistente")
        return redirect(url_for("bibliotecario")) 
    if copiaDisponibile(mysql, codicecopia)[0]:
        flash("La copia è già disponibile")
        return redirect(url_for("bibliotecario"))
    
    updatePrestito(mysql,codicecopia, date.today())
    flash("Copia aggiornata con successo")
    return redirect(url_for("bibliotecario"))
    
@app.route("/libro/<isbn>")
def libro(isbn):
    
    book_data = getDatiLibro(mysql, isbn)

    if not book_data:
        abort(404, description="Libro non trovato")

    updateLibroStats(mysql, isbn)

    riassunti = getRiassuntiByLibro(mysql, isbn)

    book = {
        "title": book_data[0][0],
        "authors": [a[1] for a in book_data],
        "genre": book_data[0][2],
        "year": book_data[0][3],
        "isbn": book_data[0][4],
        "nricerche":book_data[0][5],
        "cover_url": f"https://covers.openlibrary.org/b/isbn/{book_data[0][4]}-L.jpg"
    }

    return render_template("libro.html", book=book, riassunti=riassunti)

@app.route("/user/")
def userData():
    if session.get("userType") == "admin":
        # Admin View: Fetch All Users
        user_list = getUserList(mysql)
        return render_template("user.html",user_list=user_list)
        
    username = session.get("username")
    if username:
        user_data = getAnagrafica(mysql, username )
        user = {
            "nome": user_data[0],
            "cognome": user_data[1],
            "email": user_data[2],
            "data_nascita": user_data[3],
        }

    
        prestiti = getPrestitiByUsername(mysql,username)

        riassunti = getRiassuntiByUsername(mysql, username)
        return render_template("user.html", user=user, prestiti=prestiti, riassunti=riassunti)
    abort(403)

@app.route("/user/<username>")
def getUsers(username):
    if session.get("userType") == "admin":
        
        if username:
            # Fetch Selected User's Info
            user_list= getUserList(mysql)
            user_data = getAnagrafica(mysql, username)
            
            selected_user = {
                "nome": user_data[0],
                "cognome": user_data[1],
                "email": user_data[2],
                "data_nascita": user_data[3],
            }

            
        
            prestiti = getPrestitiByUsername(mysql, username)

            riassunti = getRiassuntiByUsername(mysql, username)

        
        return render_template(
            "user.html", user_list=user_list, selected_user=selected_user, prestiti=prestiti, riassunti=riassunti
        )
    else:
        abort(403)


@app.route("/addRiassunto/", methods=["POST"])
def addRiassunto():
    
    isbn = request.form.get("isbn")
    riassunto = request.form.get("riassunto")
    username = session.get("username")
    if not isbn or not riassunto:
        flash("Il riassunto non può essere vuoto.")
        return redirect(url_for("libro", isbn=isbn))

    insertRiassunto(mysql, isbn, username, riassunto)

    flash("Riassunto aggiunto con successo!")
    return redirect(url_for("libro", isbn=isbn))

@app.route("/catalogo/")
def catalogo():
    
    keyword = request.args.get("keyword", "")
    sort = request.args.get("sort", "Titolo") #sort di default usa titolo

    
    book_data = getLibri(mysql,keyword,sort)
    books = []
    
    for b in book_data:
        books.append({
            "titolo": b[0],
            "autori": b[1],
            "genere": b[2],
            "isbn": b[4],
            "cover_url": f"https://covers.openlibrary.org/b/isbn/{b[4]}-L.jpg",
            "disponibile": len(isDisponibile(mysql, b[4]))
        })
    # Render the catalog template with the fetched books
    return render_template("catalogo.html", books=books)



@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("login"))        


app.run(debug=True)