-- Eliminazione tabelle se esistono
DROP TABLE IF EXISTS Tessera;
DROP TABLE IF EXISTS Prestiti;
DROP TABLE IF EXISTS Inventario;
DROP TABLE IF EXISTS Utenti;
DROP TABLE IF EXISTS Autorato;
DROP TABLE IF EXISTS Autori;
DROP TABLE IF EXISTS Libri;

-- Creazione delle tabelle
CREATE TABLE IF NOT EXISTS Autori(
    ISNI CHAR(16) PRIMARY KEY,
    Nome VARCHAR(32) NOT NULL,
    Cognome VARCHAR(32) NOT NULL,
    DataNascita DATE NOT NULL,
    DataMorte DATE
);

CREATE TABLE IF NOT EXISTS Libri(
    ISBN CHAR(13) PRIMARY KEY,
    Titolo VARCHAR(32) NOT NULL,
    Categoria VARCHAR(32) NOT NULL,
    NumCopie INT DEFAULT 0,
    Riassunto TEXT,
    Autore VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS Autorato(
    ISNI CHAR(16) NOT NULL,
    ISBN CHAR(13) NOT NULL,
    PRIMARY KEY(ISNI, ISBN),
    FOREIGN KEY (ISNI) REFERENCES Autori(ISNI),
    FOREIGN KEY (ISBN) REFERENCES Libri(ISBN)
);

CREATE TABLE IF NOT EXISTS Utenti(
    CF CHAR(16) PRIMARY KEY,
    Nome VARCHAR(32) NOT NULL,
    Cognome VARCHAR(32) NOT NULL,
    Email VARCHAR(32) NOT NULL,
    Telefono VARCHAR(16) NOT NULL
);

CREATE TABLE IF NOT EXISTS Inventario(
    IDL INT NOT NULL AUTO_INCREMENT,
    ISBN CHAR(13) NOT NULL,
    X INT NOT NULL,
    Y INT NOT NULL,
    Z INT NOT NULL,
    PRIMARY KEY (IDL),
    FOREIGN KEY (ISBN) REFERENCES Libri(ISBN)
);

CREATE TABLE IF NOT EXISTS Prestiti(
    DataInizio DATE NOT NULL,
    DataRestituzione DATE,
    DataScadenza DATE NOT NULL,
    CF CHAR(16) NOT NULL,
    IDL INT NOT NULL,
    PRIMARY KEY (DataInizio, CF, IDL),
    FOREIGN KEY (CF) REFERENCES Utenti (CF),
    FOREIGN KEY (IDL) REFERENCES Inventario(IDL)
);

CREATE TABLE IF NOT EXISTS Tessera(
    CF CHAR(16) PRIMARY KEY,
    Nprestiti INT NOT NULL,
    DataScadenza DATE NOT NULL,
    Username VARCHAR(32) NOT NULL,
    Pwd VARCHAR(64) NOT NULL,
    IsAdmin TINYINT(1) NOT NULL,
    FOREIGN KEY (CF) REFERENCES Utenti(CF)
);

-- Inserimento dati in Autori
INSERT INTO Autori (ISNI, Nome, Cognome, DataNascita, DataMorte)
VALUES 
('0000000987654321', 'Dante', 'Alighieri', '1265-05-21', '1321-09-14'),
('0000000876543210', 'Francesco', 'Petrarca', '1304-07-20', '1374-07-19'),
('0000000765432109', 'Ludovico', 'Ariosto', '1474-09-08', '1533-07-06'),
('0000000654321098', 'Giovanni', 'Boccaccio', '1313-06-16', '1375-12-21'),
('0000000543210987', 'Torquato', 'Tasso', '1544-03-11', '1595-04-25'),
('0000000432109876', 'Niccolò', 'Machiavelli', '1469-05-03', '1527-06-21'),
('0000000321098765', 'Giuseppe', 'Parini', '1729-05-23', '1799-08-15');

-- Inserimento dati in Libri
INSERT INTO Libri (ISBN, Titolo, Categoria, NumCopie, Riassunto, Autore)
VALUES 
('9788817000257', 'La Divina Commedia', 'Poesia', 15, 'Il viaggio di Dante attraverso Inferno, Purgatorio e Paradiso.', 'Dante Alighieri'),
('9788817101234', 'Il Canzoniere', 'Poesia', 10, 'Una raccolta di poesie amorose dedicate a Laura.', 'Francesco Petrarca'),
('9788817204567', 'Orlando Furioso', 'Epica', 12, 'Le avventure cavalleresche e fantastiche di Orlando.', 'Ludovico Ariosto'),
('9788817307890', 'Decameron', 'Narrativa', 8, 'Cento novelle raccontate da un gruppo di giovani in fuga dalla peste.', 'Giovanni Boccaccio'),
('9788817410123', 'Gerusalemme Liberata', 'Epica', 7, 'Un poema epico sulla prima crociata.', 'Torquato Tasso'),
('9788817513456', 'Il Principe', 'Saggio', 6, 'Un trattato politico sulla natura del potere e del governo.', 'Niccolò Machiavelli'),
('9788817616789', 'Odi', 'Poesia', 5, 'Una raccolta di poesie di carattere morale e civile.', 'Giuseppe Parini');

-- Inserimento dati in Autorato
INSERT INTO Autorato (ISNI, ISBN)
VALUES 
('0000000987654321', '9788817000257'),
('0000000876543210', '9788817101234'),
('0000000765432109', '9788817204567'),
('0000000654321098', '9788817307890'),
('0000000543210987', '9788817410123'),
('0000000432109876', '9788817513456'),
('0000000321098765', '9788817616789');

-- Inserimento dati in Inventario
INSERT INTO Inventario (ISBN, X, Y, Z)
VALUES 
('9788817000257', 4, 2, 1),
('9788817101234', 4, 2, 2),
('9788817204567', 5, 1, 1),
('9788817307890', 5, 2, 1),
('9788817410123', 6, 1, 1),
('9788817513456', 6, 2, 2),
('9788817616789', 7, 1, 1);