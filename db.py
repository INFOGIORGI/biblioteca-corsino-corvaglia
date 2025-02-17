class DB:
    def __init__(self):
        from flask import Flask
        from flask_mysqldb import MySQL

        app = Flask(__name__)
        app.config["MYSQL_HOST"] = "138.41.20.102"
        app.config["MYSQL_PORT"] = 53306
        app.config["MYSQL_USER"] = "ospite"
        app.config["MYSQL_DB"] = "corsino_corvaglia"
        app.config["MYSQL_PASSWORD"] = "ospite"

        mysql = MySQL(app)
        #creare il db
        cursor = mysql.connection.cursor()
        query = """DROP TABLE IF EXISTS AUTORE;
                DROP TABLE IF EXISTS LIBRO;
                DROP TABLE IF EXISTS CATALOGO;
                DROP TABLE IF EXISTS COMITATO_DI_SCRITTURA;
                DROP TABLE IF EXISTS UTENTE;
                DROP TABLE IF EXISTS PRESTITI;
                DROP TABLE IF EXISTS TESSERA;

                CREATE TABLE AUTORE(
                    IDAutore VARCHAR(20),
                    nome VARCHAR(20) NOT NULL,
                    cognome VARCHAR(20) NOT NULL,
                    dataNascita DATE NOT NULL,
                    dataMorte DATE,
                    bio VARCHAR(255) NOT NULL,
                    PRIMARY KEY(IDAutore)
                );

                CREATE TABLE LIBRO(
                    ISBN CHAR(13),
                    titolo VARCHAR(20) NOT NULL,
                    genere VARCHAR(20) NOT NULL,
                    autore VARCHAR(20),
                    PRIMARY KEY(ISBN),
                    FOREIGN KEY(autore) REFERENCES AUTORE(IDAutore)
                );

                CREATE TABLE CATALOGO(
                    IDLibro VARCHAR(20),
                    ISBN CHAR(13) NOT NULL,
                    corridoio int NOT NULL,
                    scaffale int NOT NULL,
                    ripiano int NOT NULL,
                    stato VARCHAR(20) NOT NULL,
                    PRIMARY KEY(IDLibro),
                    FOREIGN KEY(ISBN) REFERENCES LIBRO(ISBN)
                );

                CREATE TABLE COMITATO_DI_SCRITTURA(
                    ISBN CHAR(13),
                    IDAutore VARCHAR(20),
                    PRIMARY KEY(ISBN),
                    PRIMARY KEY(IDAutore),
                    FOREIGN KEY(ISBN) REFERENCES LIBRO(ISBN),
                    FOREIGN KEY(IDAutore) REFERENCES AUTORE(IDAutore)
                );

                CREATE TABLE UTENTE(
                    IDUtente VARCHAR(20),
                    nome VARCHAR(20) NOT NULL,
                    cognome VARCHAR(20) NOT NULL,
                    dataNascita DATE NOT NULL,
                    telefono VARCHAR(13) NOT NULL,
                    isAdmin BOOLEAN NOT NULL,
                    PRIMARY KEY(IDUtente)
                );

                CREATE TABLE PRESTITI(
                    IDLibro VARCHAR(20),
                    IDUtente VARCHAR(20),
                    inizio DATE NOT NULL,
                    restituzione DATE,
                    PRIMARY KEY(IDLibro),
                    PRIMARY KEY(IDUtente),
                    FOREIGN KEY(IDLibro) REFERENCES CATALOGO(IDLibro),
                    FOREIGN KEY(IDUtente) REFERENCES UTENTE(IDUtente)
                );

                CREATE TABLE TESSERA(
                    IDTessera VARCHAR(20),
                    IDUtente VARCHAR(20),
                    creazione DATE NOT NULL, 
                    scadenza DATE NOT NULL,
                    PRIMARY KEY(IDTessera),
                    FOREIGN KEY(IDUtente) REFERENCES UTENTE(IDUtente)
                );"""
        cursor.execute(query)
        
def create_tables():
    
