import json
import datetime

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


def api_allOrders(mysql):
    cursor = mysql.connection.cursor()
    query = '''SELECT * FROM orders'''
    cursor.execute(query)
    row_headers=[x[0] for x in cursor.description]
    #print(row_headers)
    dati = cursor.fetchall()
    json_data=[]
    for result in dati:
        json_data.append(dict(zip(row_headers,result)))
    cursor.close()   
    #print(json_data) 
    return json.dumps(json_data,default=serialize_datetime)

def serialize_datetime(obj): #per serializzare delle date
    if isinstance(obj, datetime.date): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 

def details(mysql, id):
    cursor = mysql.connection.cursor()
    query = '''SELECT * FROM orders WHERE customerID = %s'''
    cursor.execute(query,(id,))
    dati = cursor.fetchall()
    cursor.close()
    return dati
     