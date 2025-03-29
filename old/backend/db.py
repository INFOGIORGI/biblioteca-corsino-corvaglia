import json
import datetime

def toDict(libri):
    keys = ["isbn", "title", "genre", "id"]
    return[dict(zip(keys, libro)) for libro in libri]

def addLibro(mysql,ISBN,titolo,genere,autore,corridoio,scaffale,ripiano,stato):
        cursor = mysql.connection.cursor()
        query = '''SELECT * FROM LIBRO WHERE ISBN=%s'''
        cursor.execute(query,(ISBN,))
        dati = cursor.fetchall() #torna il risultato della query
        if len(dati)==0:
            query = '''INSERT INTO LIBRO(ISBN, titolo, genere, autore) VALUES(%s,%s,%s,%s)'''
            cursor.execute(query,(ISBN,titolo,genere,autore))
            mysql.connection.commit()
        query = '''INSERT INTO CATALOGO(ISBN,corridoio,scaffale,ripiano,stato) VALUES(%s,%s,%s,%s,%s)'''
        cursor.execute(query,(ISBN,corridoio,scaffale,ripiano,stato))
        cursor.close()
        return 

def cercaLibro(mysql, parola_chiave):
    cursor = mysql.connection.cursor()
    query = '''SELECT * FROM LIBRO WHERE TITOLO LIKE %s UNION SELECT * FROM LIBRO WHERE ISBN LIKE %s '''
    cursor.execute(query, ("%" + parola_chiave + "%","%" + parola_chiave + "%"))
    dati = cursor.fetchall()
    cursor.close()
    print(dati)
    return dati


def ordinaLibro(mysql, attributo, ordinamento):
    cursor = mysql.connection.cursor()
    query = '''SELECT * FROM LIBRO ORDER BY '''+attributo+" "+ordinamento
    cursor.execute(query)
    dati = cursor.fetchall()
    cursor.close()
    print(dati)
    return dati


# def registrazione(mysql, cf, nome, cognome, pw, dataN, tel, admin)