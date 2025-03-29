def capocchia():
    print("ODIO I NEGRI")

def getCredenziali(mysql, username, password):
        cursor = mysql.connection.cursor()
        query = "SELECT username FROM UTENTE WHERE username = %s"
        cursor.execute(query, (username,))
        account = cursor.fetchone()
        cursor.close()
        return account