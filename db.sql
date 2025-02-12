CREATE TABLE IF NOT EXISTS AUTORE(
    IDAutore INT AUTO_INCREMENT,
    nome VARCHAR(20) NOT NULL,
    cognome VARCHAR(20) NOT NULL,
    dataNascita DATE NOT NULL,
    dataMorte DATE,
    bio VARCHAR(255) NOT NULL,
    PRIMARY KEY(IDAutore)
);

CREATE TABLE IF NOT EXISTS(
    ISBN CHAR(13),
    titolo VARCHAR(20) NOT NULL,
    genere VARCHAR(20) NOT NULL,
    autore VARCHAR(20),
    PRIMARY KEY(ISBN),
    FOREIGN KEY(autore) REFERENCES AUTORE(IDAutore)
);

CREATE TABLE IF NOT EXISTS CATALOGO(
    IDLibro INT AUTO_INCREMENT,
    ISBN CHAR(13) NOT NULL,
    corridoio int NOT NULL,
    scaffale int NOT NULL,
    ripiano int NOT NULL,
    stato VARCHAR(20) NOT NULL,
    PRIMARY KEY(IDLibro),
    FOREIGN KEY(ISBN) REFERENCES LIBRO(ISBN)
);

CREATE TABLE IF NOT EXISTS COMITATO_DI_SCRITTURA(
    ISBN CHAR(13),
    IDAutore INT,
    PRIMARY KEY(ISBN),
    PRIMARY KEY(IDAutore),
    FOREIGN KEY(ISBN) REFERENCES LIBRO(ISBN),
    FOREIGN KEY(IDAutore) REFERENCES AUTORE(IDAutore)
);

CREATE TABLE IF NOT EXISTS UTENTE(
    cf VARCHAR(16),
    nome VARCHAR(20) NOT NULL,
    cognome VARCHAR(20) NOT NULL,
    pw varchar(16) NOT NULL
    dataNascita DATE NOT NULL,
    telefono VARCHAR(13) NOT NULL,
    isAdmin BOOLEAN NOT NULL,
    PRIMARY KEY(cf)
);

CREATE TABLE IF NOT EXISTS PRESTITI(
    IDLibro INT,
    cf VARCHAR(16),
    inizio DATE NOT NULL,
    restituzione DATE,
    PRIMARY KEY(IDLibro),
    PRIMARY KEY(cf),
    FOREIGN KEY(IDLibro) REFERENCES CATALOGO(IDLibro),
    FOREIGN KEY(cf) REFERENCES UTENTE(cf)
);

CREATE TABLE IF NOT EXISTS TESSERA(
    IDTessera INT,
    cf VARCHAR(16),
    creazione DATE NOT NULL, 
    scadenza DATE NOT NULL,
    PRIMARY KEY(IDTessera),
    FOREIGN KEY(cf) REFERENCES UTENTE(cf)
);

INSERT INTO AUTORE (nome, cognome, dataNascita, dataMorte, bio) VALUES 
('Giovanni', 'Rossi', '1950-05-20', NULL, 'Bio di Giovanni Rossi.'),
('Maria', 'Bianchi', '1965-11-10', '2006-05-04', 'Bio di Maria Bianchi.'),
('Luca', 'Verdi', '1980-01-15', NULL, 'Bio di Luca Verdi.'),
('Anna', 'Neri', '1975-07-05', '2023-03-17', 'Bio di Anna Neri.'),
('Paolo', 'Gialli', '1990-02-25', NULL, 'Bio di Paolo Gialli.');

INSERT INTO LIBRO (ISBN, titolo, genere, autore) VALUES 
('9781234567897', 'Il Grande Romanzo', 'Narrativa', '1'), 
('9781234567898', 'Avventure Epiche', 'Fantasia', '2'), 
('9781234567899', 'Misteri del Passato', 'Giallo', '3'), 
('9781234567900', 'Storie amorose', 'Romantico', '4'), 
('9781234567901', 'Rivoluzione Tecnologica', 'Saggio', '5');


INSERT INTO CATALOGO (ISBN, corridoio, scaffale, ripiano, stato) VALUES 
('9781234567897', 1, 2, 3, 'Nuovo'), 
('9781234567897', 1, 2, 4, 'Consumato'), 
('9781234567899', 1, 3, 1, 'Buono'), 
('9781234567900', 1, 3, 2, 'Buono'), 
('9781234567901', 2, 1, 1, 'Nuovo');


INSERT INTO UTENTE (cf, nome, cognome, pw, dataNascita, telefono, isAdmin) VALUES 
('RSSGNN50E20H501K', 'Giovanni', 'Rossi','aaaaaaaaaa','1950-05-20', '1234567890', FALSE), 
('BNCMRI65S50H501K', 'Maria', 'Bianchi', 'bbbbbbbb','1965-11-10', '0987654321', TRUE), 
('VRDLCA80A15H501K', 'Luca', 'Verdi', 'ccccccccc','1980-01-15', '1122334455', FALSE), 
('NRNAN75L50H501K', 'Anna', 'Neri', 'ddddddddd','1975-07-05', '2233445566', FALSE), 
('GLLPLO90B25H501K', 'Paolo', 'Gialli', 'eeeeeeee','1990-02-25', '3344556677', TRUE);


INSERT INTO TESSERA (IDTessera, cf, creazione, scadenza) VALUES 
(1, 'RSSGNN50E20H501K', '2025-01-01', '2025-12-31'), 
(2, 'BNCMRI65S50H501K', '2025-01-01', '2025-12-31'), 
(3, 'VRDLCA80A15H501K', '2025-01-01', '2025-12-31'), 
(4, 'NRNAN75L50H501K', '2025-01-01', '2025-12-31'), 
(5, 'GLLPLO90B25H501K', '2025-01-01', '2025-12-31');


INSERT INTO PRESTITI (IDLibro, cf, inizio, restituzione) VALUES 
(1, 'RSSGNN50E20H501K', '2025-02-01', NULL), 
(2, 'BNCMRI65S50H501K', '2025-02-02', NULL), 
(3, 'VRDLCA80A15H501K', '2025-02-03', '2025-02-10'), 
(4, 'NRNAN75L50H501K', '2025-02-04', NULL), 
(5, 'GLLPLO90B25H501K', '2025-02-05', NULL);


INSERT INTO COMITATO_DI_SCRITTURA (ISBN, IDAutore) VALUES 
('9781234567897', 1), 
('9781234567898', 2), 
('9781234567899', 3), 
('9781234567900', 4), 
('9781234567901', 5);


COMMIT;