def getCredenziali(mysql, username):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM UTENTE WHERE username = %s"
        cursor.execute(query, (username,))
        account = cursor.fetchone()
        cursor.close()
        return account

def doRegister(mysql, nome, cognome, user, pw, data, email, tipo):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO UTENTE VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query,(nome,cognome,user,pw,data,email,tipo,1))
    mysql.connection.commit()