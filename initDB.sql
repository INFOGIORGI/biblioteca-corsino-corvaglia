DROP TABLE IF EXISTS PRESTITO;
DROP TABLE IF EXISTS RIASSUNTO;
DROP TABLE IF EXISTS CATALOGO;
DROP TABLE IF EXISTS COMITATO_DI_SCRITTURA;
DROP TABLE IF EXISTS LIBRO;
DROP TABLE IF EXISTS UTENTE;
DROP TABLE IF EXISTS AUTORE;

CREATE TABLE AUTORE(
        ID_A int AUTO_INCREMENT,
        Nome varchar(20) NOT NULL,
        Cognome varchar(20) NOT NULL,
        PRIMARY KEY(ID_A)
);

CREATE TABLE LIBRO(
        ISBN char(13),
        Titolo varchar(255) NOT NULL,
        Autore int NOT NULL,
        Genere varchar(20) NOT NULL,
        AnnoPub char(4) NOT NULL,
        NRicerche int NOT NULL,
        PRIMARY KEY(ISBN),
        FOREIGN KEY(Autore) REFERENCES AUTORE(ID_A)       
);


CREATE TABLE COMITATO_DI_SCRITTURA(
        ISBN char(13),
        ID_A int,
        PRIMARY KEY(ISBN, ID_A),
        FOREIGN KEY(ISBN) REFERENCES LIBRO(ISBN),
        FOREIGN KEY(ID_A) REFERENCES AUTORE(ID_A)
);

CREATE TABLE CATALOGO(
        ID_C int AUTO_INCREMENT,
        ISBN char(13) NOT NULL,
        Posizione char(6) NOT NULL UNIQUE,
        isDisponibile boolean NOT NULL,
        PRIMARY KEY(ID_C),
        FOREIGN KEY(ISBN) REFERENCES LIBRO(ISBN)
        
);


CREATE TABLE UTENTE(
        Nome varchar(20) NOT NULL,
        Cognome varchar(20) NOT NULL,
        Username varchar(20) NOT NULL,
        Password varchar(20) NOT NULL,
        DataNascita date NOT NULL,
        Email varchar(50),
        Tipo varchar(20) NOT NULL,
        PRIMARY KEY(Username)
);

CREATE TABLE RIASSUNTO(
        ISBN char(13),
        Username int,
        Contenuto varchar(4096) NOT NULL,
        PRIMARY KEY(ISBN, Username),
        FOREIGN KEY(ISBN) REFERENCES LIBRO(ISBN),
        FOREIGN KEY(Username) REFERENCES UTENTE(Username)
        
);

CREATE TABLE PRESTITO(
        Username int,
        ID_C int,
        DataInizio date NOT NULL,
        DataRestituzione date,
        PRIMARY KEY(Username, ID_C),
        FOREIGN KEY(Username) REFERENCES UTENTE(Username),
        FOREIGN KEY(ID_C) REFERENCES CATALOGO(ID_C)
);
