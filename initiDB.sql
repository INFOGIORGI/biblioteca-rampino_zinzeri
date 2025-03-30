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
('0000000121464392', 'Alessandro', 'Manzoni', '1785-03-07', '1873-05-22'),
('0000000121456321', 'Giovanni', 'Verga', '1840-09-02', '1922-01-27'),
('0000000121459383', 'Italo', 'Calvino', '1923-10-15', '1985-09-19'),
('0000000121452790', 'Umberto', 'Eco', '1932-01-05', '2016-02-19'),
('0000000121467210', 'Gabriele', "D'Annunzio", '1863-03-12', '1938-03-01'),
('0000000121470000', 'Nuovo', 'Autore', '1975-06-15', NULL),
('0000000121471000', 'Marco', 'Bianchi', '1980-08-22', NULL);

-- Inserimento dati in Libri
INSERT INTO Libri (ISBN, Titolo, Categoria, NumCopie, Riassunto, Autore)
VALUES 
('9788804498122', 'I Promessi Sposi', 'Romanzo Storico', 10, 'Un classico della letteratura italiana che narra la storia di Renzo e Lucia nel contesto della Lombardia del XVII secolo.', 'Alessandro Manzoni'),
('9788804536571', 'Il Nome della Rosa', 'Romanzo Storico', 8, 'Un romanzo giallo ambientato in un monastero medievale, dove si indaga su una serie di misteriosi omicidi.', 'Umberto Eco'),
('9788804671531', 'Il Barone Rampante', 'Narrativa', 5, 'La storia di un giovane nobile che decide di vivere sugli alberi per protesta contro le imposizioni della società.', 'Italo Calvino'),
('9788804725525', 'Mastro-don Gesualdo', 'Romanzo', 6, 'Un romanzo verista che racconta la storia di un uomo che cerca di elevarsi socialmente attraverso il lavoro e il matrimonio.', 'Giovanni Verga'),
('9788804778472', 'Il Piacere', 'Narrativa', 4, 'Un romanzo decadente che segue la vita di un giovane aristocratico e il suo amore per l’estetica e il lusso.', 'Gabriele Annunzio'),
('9788804888888', 'I cambiamenti sociali', 'Saggio', 3, 'Un testo che esplora i cambiamenti sociali del XXI secolo e le loro implicazioni per il futuro.', 'Sconosciuto'),
('9788804999999', 'La tecnologia', 'Narrativa', 2, 'Un romanzo moderno che analizza il rapporto tra tecnologia e umanità in un mondo sempre più connesso.', 'Marco Bianchi');

-- Inserimento dati in Autorato
INSERT INTO Autorato (ISNI, ISBN)
VALUES 
('0000000121464392', '9788804498122'),
('0000000121456321', '9788804725525'),
('0000000121459383', '9788804671531'),
('0000000121452790', '9788804536571'),
('0000000121467210', '9788804778472'),
('0000000121470000', '9788804888888'),
('0000000121471000', '9788804999999');

-- Inserimento dati in Inventario
INSERT INTO Inventario (ISBN, X, Y, Z)
VALUES 
('9788804498122', 1, 1, 1),
('9788804536571', 1, 1, 2),
('9788804671531', 1, 2, 1),
('9788804725525', 2, 1, 1),
('9788804778472', 2, 2, 1),
('9788804888888', 3, 1, 1),
('9788804999999', 3, 2, 1);
