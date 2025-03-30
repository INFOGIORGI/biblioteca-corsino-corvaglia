def getUsers(mysql):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM UTENTE"
    cursor.execute(query)
    query = cursor.fetchall()
    cursor.close()
    return query

def getSameNameUsers(mysql,nome,cognome):
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM UTENTE WHERE Nome = %s and Cognome = %s"
    cursor.execute(query,(nome,cognome))
    query = cursor.fetchone()
    cursor.close()
    return query

def getCredenziali(mysql, username):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM UTENTE WHERE username = %s"
        cursor.execute(query, (username,))
        account = cursor.fetchone()
        cursor.close()
        return account

def doRegister(mysql, user, nome, cognome, pw, data, email, tipo):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO UTENTE VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query,(user,nome,cognome,pw,data,email,tipo,1))
    mysql.connection.commit()
    
def updatePassword(mysql, username, password):
    cursor = mysql.connection.cursor()
    query = "UPDATE UTENTE SET PASSWORD = %s, firstLogin = false WHERE USERNAME = %s"
    cursor.execute(query,(password, username))
    mysql.connection.commit()
    cursor.close()


def getLibro(mysql, ISBN):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM LIBRO WHERE ISBN = %s"
    cursor.execute(query, (ISBN,))
    libro = cursor.fetchone()
    cursor.close()
    return libro


def insertCopia(mysql,ISBN, posizione, ncopie):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO CATALOGO (ISBN, Posizione, isDisponibile) VALUES (%s, %s, %s)"

    for i in range(ncopie):
        cursor.execute(query,(ISBN,posizione,True))
    mysql.connection.commit()
    cursor.close()

def isDisponibile(mysql, codicecopia):
    cursor = mysql.connection.cursor()
    query = "SELECT isDisponibile FROM CATALOGO WHERE ID_C = %s"
    cursor.execute(query, (codicecopia,))
    result = cursor.fetchone()
    cursor.close()
    return result

def dbAddPrestito(mysql, username, codicecopia, dataInizio):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO PRESTITO(username, ID_C, dataInizio) VALUES(%s,%s,%s)"
    cursor.execute(query,(username,codicecopia,dataInizio))
    query = "UPDATE CATALOGO SET isDisponibile = false WHERE ID_C = %s"
    cursor.execute(query,(codicecopia))
    mysql.connection.commit()
    
def dbModificaPrestito(mysql, codicecopia, datafine):
    cursor = mysql.connection.cursor()
    query = "UPDATE PRESTITO SET dataRestituzione = %s WHERE ID_C = %s AND dataRestituzione IS NULL"
    cursor.execute(query,(datafine,codicecopia))
    query = "UPDATE CATALOGO SET isDisponibile = true WHERE ID_C = %s"
    cursor.execute(query,(codicecopia))
    mysql.connection.commit()

def getAutore(mysql, nome, cognome):
    cursor = mysql.connection.cursor()
    query = "SELECT ID_A FROM AUTORE WHERE Nome = %s AND Cognome = %s"
    cursor.execute(query, (nome,cognome))
    result = cursor.fetchone()
    cursor.close()
    return result

def insertAutore(mysql, nome, cognome):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO AUTORE (Nome, Cognome) VALUES(%s,%s)"
    cursor.execute(query,(nome, cognome))
    mysql.connection.commit()

def insertComitato(mysql, id_autore, ISBN):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO COMITATO_DI_SCRITTURA VALUES(%s,%s)"
    cursor.execute(query,(ISBN, id_autore))
    mysql.connection.commit()


def insertLibro(mysql, ISBN, titolo, anno_pubbl, genere):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO LIBRO VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(query,(ISBN, titolo, genere, anno_pubbl,0))
    mysql.connection.commit()
    
def getBookData(mysql, isbn):
    cursor = mysql.connection.cursor()
    
    query = """
        SELECT Titolo, GROUP_CONCAT(CONCAT(Nome, ' ', Cognome)) AS Autori, Genere, AnnoPub, LIBRO.ISBN, LIBRO.nricerche
        FROM LIBRO
        INNER JOIN COMITATO_DI_SCRITTURA ON LIBRO.ISBN = COMITATO_DI_SCRITTURA.ISBN
        INNER JOIN AUTORE ON COMITATO_DI_SCRITTURA.ID_A = AUTORE.ID_A
        WHERE LIBRO.ISBN = %s
        GROUP BY Titolo, Genere, AnnoPub, LIBRO.ISBN, LIBRO.nricerche

    """
    cursor.execute(query, (isbn,))
    book_data = cursor.fetchall()
    cursor.close()
    return book_data

def updateLibroStats(mysql, isbn):
    cursor = mysql.connection.cursor()
    query = "UPDATE LIBRO SET nricerche = nricerche + 1 WHERE ISBN = %s"
    cursor.execute(query,(isbn,))
    mysql.connection.commit()