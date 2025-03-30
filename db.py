from flask import jsonify

def getUsers(mysql):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM UTENTE"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    print("PRINT",result)
    return result

def getUserList(mysql):
    cursor = mysql.connection.cursor()
    query = "SELECT Username, Nome, Cognome, Email FROM UTENTE WHERE tipo = 'utente'"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def getAnagrafica(mysql, username):
    cursor = mysql.connection.cursor()
    query = "SELECT Nome, Cognome, Email, DataNascita FROM UTENTE WHERE Username = %s"
    cursor.execute(query,(username,))
    result = cursor.fetchone()
    return result


def getSameNameUsers(mysql,nome,cognome):
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM UTENTE WHERE Nome = %s and Cognome = %s"
    cursor.execute(query,(nome,cognome))
    result = cursor.fetchone()
    cursor.close()
    return result

def getCredenziali(mysql, username):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM UTENTE WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    return result


def insertUser(mysql, user, nome, cognome, pw, data, email, tipo):
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
    result = cursor.fetchone()
    cursor.close()
    return result

def getLibri(mysql, keyword=None, sort="Titolo"):
    cursor = mysql.connection.cursor()
    query_base = """
        SELECT Titolo, GROUP_CONCAT(CONCAT(Nome, ' ', Cognome)) AS Autori, Genere, AnnoPub, LIBRO.ISBN, LIBRO.nricerche
        FROM LIBRO
        INNER JOIN COMITATO_DI_SCRITTURA ON LIBRO.ISBN = COMITATO_DI_SCRITTURA.ISBN
        INNER JOIN AUTORE ON COMITATO_DI_SCRITTURA.ID_A = AUTORE.ID_A
    """
    where = ""
    if keyword != None:
        keyword = "%" + keyword.lower() + "%"
        where += """ WHERE LOWER(LIBRO.Titolo) LIKE %s
            OR LOWER(AUTORE.Nome) LIKE %s
            OR LOWER(AUTORE.Cognome) LIKE %s
            OR LOWER(LIBRO.Genere) LIKE %s"""
    
    
    valori_consentiti= ["Titolo", "Genere", "Autori"]
    if sort not in valori_consentiti:
        sort = "Titolo"

    query = query_base + where + " GROUP BY Titolo, Genere, AnnoPub, LIBRO.ISBN, LIBRO.nricerche ORDER BY " + sort   

    
    if keyword == None:
        cursor.execute(query)
    else:
        cursor.execute(query, (keyword, keyword, keyword, keyword))
    
    result = cursor.fetchall()
    print(result)
    cursor.close()
    return result
    

def insertCopia(mysql,ISBN, posizione, ncopie):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO CATALOGO (ISBN, Posizione, isDisponibile) VALUES (%s, %s, %s)"

    for i in range(ncopie):
        cursor.execute(query,(ISBN,posizione,True))
    mysql.connection.commit()
    cursor.close()

def getCopia(mysql, codicecopia):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM CATALOGO WHERE ID_C = %s"
    cursor.execute(query, (codicecopia,))
    result = cursor.fetchone()
    cursor.close()
    return result

def getCopie(mysql):
    cursor = mysql.connection.cursor()
    query = """
            SELECT LIBRO.Titolo, CATALOGO.ISBN, GROUP_CONCAT(CONCAT(Nome, ' ', Cognome)) AS Autori, LIBRO.AnnoPub,  LIBRO.Genere, CATALOGO.ID_C, CATALOGO.Posizione, CATALOGO.isDisponibile
            FROM CATALOGO
            INNER JOIN LIBRO ON CATALOGO.ISBN = LIBRO.ISBN
            INNER JOIN COMITATO_DI_SCRITTURA ON LIBRO.ISBN = COMITATO_DI_SCRITTURA.ISBN
            INNER JOIN AUTORE ON COMITATO_DI_SCRITTURA.ID_A = AUTORE.ID_A
            GROUP BY LIBRO.Titolo, CATALOGO.ISBN, LIBRO.AnnoPub,  LIBRO.Genere, CATALOGO.ID_C, CATALOGO.Posizione, CATALOGO.isDisponibile
            """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def copiaDisponibile(mysql, codicecopia):
    cursor = mysql.connection.cursor()
    query = "SELECT isDisponibile FROM CATALOGO WHERE ID_C = %s"
    cursor.execute(query, (codicecopia,))
    result = cursor.fetchone()
    cursor.close()
    return result

def insertPrestito(mysql, username, codicecopia, dataInizio):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO PRESTITO(username, ID_C, dataInizio) VALUES(%s,%s,%s)"
    cursor.execute(query,(username,codicecopia,dataInizio))
    query = "UPDATE CATALOGO SET isDisponibile = false WHERE ID_C = %s"
    cursor.execute(query,(codicecopia))
    mysql.connection.commit()

def getPrestiti(mysql):
    cursor = mysql.connection.cursor()
    query = """
            SELECT PRESTITO.username, ISBN, PRESTITO.ID_C, DataInizio, DataRestituzione
            FROM PRESTITO
            INNER JOIN CATALOGO ON PRESTITO.ID_C = CATALOGO.ID_C
            """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def getPrestitiByUsername(mysql, username):
    cursor = mysql.connection.cursor()
    query = """
            SELECT LIBRO.Titolo, LIBRO.ISBN, PRESTITO.DataInizio, PRESTITO.DataRestituzione
            FROM PRESTITO
            INNER JOIN CATALOGO ON PRESTITO.ID_C = CATALOGO.ID_C
            INNER JOIN LIBRO ON CATALOGO.ISBN = LIBRO.ISBN
            WHERE PRESTITO.Username = %s
            """
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    cursor.close()
    return result
    
def updatePrestito(mysql, codicecopia, datafine):
    cursor = mysql.connection.cursor()
    query = "UPDATE PRESTITO SET dataRestituzione = %s WHERE ID_C = %s AND dataRestituzione IS NULL"
    cursor.execute(query,(datafine,codicecopia))
    query = "UPDATE CATALOGO SET isDisponibile = true WHERE ID_C = %s"
    cursor.execute(query,(codicecopia,))
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
    
def getDatiLibro(mysql, isbn):
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
    result = cursor.fetchall()
    cursor.close()
    return result

def updateLibroStats(mysql, isbn):
    cursor = mysql.connection.cursor()
    query = "UPDATE LIBRO SET nricerche = nricerche + 1 WHERE ISBN = %s"
    cursor.execute(query,(isbn,))
    mysql.connection.commit()
    return

def insertRiassunto(mysql, isbn, username, riassunto):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO RIASSUNTO VALUES(%s, %s, %s)"
    cursor.execute(query, (isbn, username, riassunto))
    mysql.connection.commit()
    cursor.close()

def getRiassuntiByUsername(mysql, username):
    cursor = mysql.connection.cursor()
    query = """
            SELECT LIBRO.Titolo, RIASSUNTO.Contenuto
            FROM RIASSUNTO
            INNER JOIN LIBRO ON RIASSUNTO.ISBN = LIBRO.ISBN
            WHERE RIASSUNTO.Username = %s
            """
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    cursor.close()
    return result

def getRiassuntiByLibro(mysql, isbn):
    cursor = mysql.connection.cursor()
    query = """
            SELECT RIASSUNTO.username, RIASSUNTO.Contenuto
            FROM RIASSUNTO
            WHERE RIASSUNTO.ISBN = %s
            """
    cursor.execute(query, (isbn,))
    result = cursor.fetchall()
    cursor.close()
    return result

def isDisponibile(mysql, isbn):
    cursor = mysql.connection.cursor()
    query = """
            SELECT isDisponibile FROM CATALOGO WHERE ISBN = %s AND isDisponibile = true
            """
    cursor.execute(query, (isbn,))
    result = cursor.fetchall()
    cursor.close()
    return result