DROP TABLE IF EXISTS PRESTITO;
DROP TABLE IF EXISTS RIASSUNTO;
DROP TABLE IF EXISTS CATALOGO;
DROP TABLE IF EXISTS COMITATO_DI_SCRITTURA;
DROP TABLE IF EXISTS LIBRO;
DROP TABLE IF EXISTS UTENTE;
DROP TABLE IF EXISTS AUTORE;

CREATE TABLE AUTORE(
        ID_A int AUTO_INCREMENT,
        Nome varchar(100) NOT NULL,
        Cognome varchar(100) NOT NULL,
        PRIMARY KEY(ID_A)
);

CREATE TABLE LIBRO(
        ISBN char(13),
        Titolo varchar(255) NOT NULL,
        Genere varchar(100) NOT NULL,
        AnnoPub char(4) NOT NULL,
        NRicerche int NOT NULL,
        PRIMARY KEY(ISBN)    
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
        Posizione char(4) NOT NULL,
        isDisponibile boolean NOT NULL,
        PRIMARY KEY(ID_C),
        FOREIGN KEY(ISBN) REFERENCES LIBRO(ISBN)
        
);


CREATE TABLE UTENTE(
        Username varchar(100),
        Nome varchar(100) NOT NULL,
        Cognome varchar(100) NOT NULL,
        Password varchar(200) NOT NULL,
        DataNascita date NOT NULL,
        Email varchar(50),
        Tipo varchar(100) NOT NULL,
        firstLogin boolean NOT NULL,
        PRIMARY KEY(Username)
);

CREATE TABLE RIASSUNTO(
        ISBN char(13),
        Username varchar(100),
        Contenuto varchar(4096) NOT NULL,
        PRIMARY KEY(ISBN, Username),
        FOREIGN KEY(ISBN) REFERENCES LIBRO(ISBN),
        FOREIGN KEY(Username) REFERENCES UTENTE(Username)
        
);

CREATE TABLE PRESTITO(
        Username varchar(100),
        ID_C int,
        DataInizio date,
        DataRestituzione date,
        PRIMARY KEY(Username, ID_C, DataInizio),
        FOREIGN KEY(Username) REFERENCES UTENTE(Username),
        FOREIGN KEY(ID_C) REFERENCES CATALOGO(ID_C)
);

INSERT INTO UTENTE VALUES("admin", "Alberto", "Corvaglia", "scrypt:32768:8:1$ahaotWVFLUko04Xu$04a7e78c5a5c50fbd91201416edfd8fb0949f65303d3e935bf26b34a4ea42d3da8772c4a6b30c3b3f72e46af4b2a9258f3bb8a3440885922f58707a79ded3515", "2006-08-20", "albertocorvaglia@ittgiogi.edu.it", "admin", false);
INSERT INTO UTENTE VALUES("biblio", "Alberto", "Corvaglia", "scrypt:32768:8:1$ahaotWVFLUko04Xu$04a7e78c5a5c50fbd91201416edfd8fb0949f65303d3e935bf26b34a4ea42d3da8772c4a6b30c3b3f72e46af4b2a9258f3bb8a3440885922f58707a79ded3515", "2006-08-20", "albertocorvaglia@ittgiogi.edu.it", "bibliotecario", false);
INSERT INTO UTENTE VALUES("user", "Alberto", "Corvaglia", "scrypt:32768:8:1$ahaotWVFLUko04Xu$04a7e78c5a5c50fbd91201416edfd8fb0949f65303d3e935bf26b34a4ea42d3da8772c4a6b30c3b3f72e46af4b2a9258f3bb8a3440885922f58707a79ded3515", "2006-08-20", "albertocorvaglia@ittgiogi.edu.it", "utente", false);