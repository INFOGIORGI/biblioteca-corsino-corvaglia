from flask import Flask, render_template,request , redirect, url_for, session, flash, abort
from flask_mysqldb import MySQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
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
        
        insertLibro(mysql, ISBN, titolo, anno_pubbl, genere)    
        
        autori = autore.split(",")
        for a in autori:                                                #Scorrendo gli autori, otteniamo nome e cognome, poi verifichiamo se sono già presenti nel db
            autore = a.split(" ")                                  # altrimenti li aggiungiamo. Poi eseguo un altra query per ottenere l'id del'autore, e lo
            cognome_autore = autore[-1]                                 # colleghiamo al libro in comitato
            nome_autore = " ".join(autore[:-1])
            print(nome_autore)
            print(cognome_autore)
            check_A = getAutore(mysql, nome_autore, cognome_autore)
            if check_A == None:
                insertAutore(mysql, nome_autore, cognome_autore)

            id_autore = getAutore(mysql, nome_autore, cognome_autore)[0]
            print(id_autore)
            insertComitato(mysql, id_autore, ISBN)
                

        # Inserisce la prima copia del nuovo libro nel catalogo
        insertCopia(mysql, ISBN, posizione, 1)
        flash("Libro aggiunto con successo.")

        
        return redirect(url_for("bibliotecario"))

@app.route("/addPrestito/", methods=["GET","POST"])
def addPrestito():
    if request.method == "GET":
            if session.get("userType") == "utente":
                abort(403)
            return redirect(url_for("bibliotecario"))
    
    username = request.form.get("username")
    codicecopia = request.form.get("codicecopia")

    
    
    if isDisponibile(mysql, codicecopia)[0]:
        dataInizio = date.today()        
        dbAddPrestito(mysql, username, codicecopia, dataInizio)
    else:
        flash("Copia non disponibile")
    
    return redirect(url_for("bibliotecario"))

@app.route("/modificaPrestito/", methods=["GET","POST"])
def modificaPrestito():
    if request.method == "GET":
            if session.get("userType") == "utente":
                abort(403)
            return redirect(url_for("bibliotecario"))
    
    codicecopia = request.form.get("codicecopia")
    print(isDisponibile(mysql, codicecopia))
    if not isDisponibile(mysql, codicecopia)[0]:
        dataFine = date.today()        
        dbModificaPrestito(mysql, codicecopia, dataFine)
    else:
        flash("Copia non prestata")
    
    return redirect(url_for("bibliotecario"))

@app.route("/libro/<isbn>")
def libro(isbn):
    
    book_data = getBookData(mysql, isbn)

    if not book_data:
        abort(404, description="Libro non trovato")

    updateLibroStats(mysql, isbn)

    cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

    book = {
        "title": book_data[0][0],
        "authors": [a[1] for a in book_data],
        "genre": book_data[0][2],
        "year": book_data[0][3],
        "isbn": book_data[0][4],
        "cover_url": cover_url,
        "nricerche":book_data[0][5]
    }

    return render_template("libro.html", book=book)

@app.route("/user", defaults={"username": None})
@app.route("/user/<username>")
def user_page(username):
    if session.get("userType") == "admin":
        # Admin View: Fetch All Users
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Username, Nome, Cognome, Email FROM UTENTE WHERE tipo = 'utente'")
        user_list = cursor.fetchall()
        print(user_list)

        # Selected User Details
        selected_user = None
        prestiti = []
        summaries = []
        if username:
            # Fetch Selected User's Info
            cursor.execute(
                "SELECT Nome, Cognome, Email, DataNascita FROM UTENTE WHERE Username = %s",
                (username,),
            )
            user_data = cursor.fetchone()
            selected_user = {
                "nome": user_data[0],
                "cognome": user_data[1],
                "email": user_data[2],
                "data_nascita": user_data[3],
            }

            # Loan History (Prestiti)
            cursor.execute(
                """
                SELECT LIBRO.Titolo, PRESTITO.DataInizio, PRESTITO.DataRestituzione
                FROM PRESTITO
                INNER JOIN CATALOGO ON PRESTITO.ID_C = CATALOGO.ID_C
                INNER JOIN LIBRO ON CATALOGO.ISBN = LIBRO.ISBN
                WHERE PRESTITO.Username = %s
                """,
                (username,),
            )
            prestiti = cursor.fetchall()

            # Fetch Summaries for Selected User
            cursor.execute(
                """
                SELECT LIBRO.Titolo, RIASSUNTO.Contenuto
                FROM RIASSUNTO
                INNER JOIN LIBRO ON RIASSUNTO.ISBN = LIBRO.ISBN
                WHERE RIASSUNTO.Username = %s
                """,
                (username,),
            )
            summaries = cursor.fetchall()
            print(summaries)

        cursor.close()
        return render_template(
            "user.html", user_list=user_list, selected_user=selected_user, prestiti=prestiti, summaries=summaries
        )

    elif session.get("userType") in ["utente", "bibliotecario"]:
        # Regular User View: Fetch Their Own Info
        username = session.get("username")
        cursor = mysql.connection.cursor()

        # Fetch User Info
        cursor.execute(
            "SELECT Nome, Cognome, Email, DataNascita FROM UTENTE WHERE Username = %s",
            (username,),
        )
        user_data = cursor.fetchone()
        user = {
            "nome": user_data[0],
            "cognome": user_data[1],
            "email": user_data[2],
            "data_nascita": user_data[3],
        }

        # Loan History (Prestiti)
        cursor.execute(
            """
            SELECT LIBRO.Titolo, LIBRO.ISBN, PRESTITO.DataInizio, PRESTITO.DataRestituzione
            FROM PRESTITO
            INNER JOIN CATALOGO ON PRESTITO.ID_C = CATALOGO.ID_C
            INNER JOIN LIBRO ON CATALOGO.ISBN = LIBRO.ISBN
            WHERE PRESTITO.Username = %s
            """,
            (username,),
        )
        prestiti = cursor.fetchall()

        # Fetch Summaries for the User
        cursor.execute(
            """
            SELECT LIBRO.Titolo, RIASSUNTO.Contenuto
            FROM RIASSUNTO
            INNER JOIN LIBRO ON RIASSUNTO.ISBN = LIBRO.ISBN
            WHERE RIASSUNTO.Username = %s
            """,
            (username,),
        )
        summaries = cursor.fetchall()
        cursor.close()
        print(prestiti)
        print(summaries)

        return render_template("user.html", user=user, prestiti=prestiti, summaries=summaries)

    else:
        abort(403)


@app.route("/addSummary", methods=["POST"])
def add_summary():
    isbn = request.form.get("isbn")
    summary = request.form.get("summary")
    username = session.get("username")
    if not isbn or not summary:
        flash("Il riassunto non può essere vuoto.")
        return redirect(url_for("libro", isbn=isbn))

    cursor = mysql.connection.cursor()
    query = "INSERT INTO RIASSUNTO VALUES(%s, %s, %s)"
    cursor.execute(query, (isbn, username, summary))
    mysql.connection.commit()
    cursor.close()

    flash("Riassunto aggiunto con successo!")
    return redirect(url_for("libro", isbn=isbn))

@app.route("/catalogo/")
def catalogo():
    # Get search query and sort options from request arguments
    search_query = request.args.get("q", "").lower()
    sort_option = request.args.get("sort", "title")

    cursor = mysql.connection.cursor()

    # Base Query
    query = """
        SELECT DISTINCT LIBRO.Titolo, GROUP_CONCAT(CONCAT(AUTORE.Nome, ' ', AUTORE.Cognome)) AS Autore, LIBRO.Genere, LIBRO.ISBN
        FROM LIBRO
        INNER JOIN COMITATO_DI_SCRITTURA ON LIBRO.ISBN = COMITATO_DI_SCRITTURA.ISBN
        INNER JOIN AUTORE ON COMITATO_DI_SCRITTURA.ID_A = AUTORE.ID_A
        GROUP BY Titolo, Genere, AnnoPub, LIBRO.ISBN;
    """

    # Search Filter
    if search_query:
        query += f"""
        WHERE LOWER(LIBRO.Titolo) LIKE %s
           OR LOWER(AUTORE.Nome) LIKE %s
           OR LOWER(AUTORE.Cognome) LIKE %s
           OR LOWER(LIBRO.Genere) LIKE %s
        """
        search_pattern = f"%{search_query}%"
        cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
    else:
        cursor.execute(query)

    # Fetch Data
    book_data = cursor.fetchall()

    # Sorting Logic
    if sort_option == "author":
        book_data = sorted(book_data, key=lambda x: x[1].lower())  # Sort by Author
    elif sort_option == "genre":
        book_data = sorted(book_data, key=lambda x: x[2].lower())  # Sort by Genre
    else:  # Default sort by Title
        book_data = sorted(book_data, key=lambda x: x[0].lower())

    cursor.close()

    # Format Data
    books = []
    for row in book_data:
        cover_url = f"https://covers.openlibrary.org/b/isbn/{row[3]}-L.jpg"  # Example API for cover images
        books.append({
            "title": row[0],
            "author": row[1],
            "genre": row[2],
            "isbn": row[3],
            "cover_url": cover_url
        })

    return render_template("catalogo.html", books=books)



@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("login"))        


app.run(debug=True)