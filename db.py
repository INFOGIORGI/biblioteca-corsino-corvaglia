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