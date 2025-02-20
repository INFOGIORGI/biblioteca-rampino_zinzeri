DROP TABLE IF EXISTS Libri;
DROP TABLE IF EXISTS Autori;
DROP TABLE IF EXISTS Utente;
DROP TABLE IF EXISTS Prestiti;
DROP TABLE IF EXISTS Catalogo;
DROP TABLE IF EXISTS Produzione;

CREATE TABLE IF NOT EXISTS Autori (
    id_autore INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    cognome VARCHAR(100),
    data_nascita DATE,
    nazionalita VARCHAR(50),
    biografia VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Libri (
    id_libro INT PRIMARY KEY AUTO_INCREMENT,
    titolo VARCHAR(255),
    id_autore INT,
    data_pubblicazione DATE,
    isbn VARCHAR(20),
    prezzo DECIMAL(10, 2),
    quantita INT,
    FOREIGN KEY (id_autore) REFERENCES Autori(id_autore)
);

CREATE TABLE IF NOT EXISTS Utente (
    id_utente INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    cognome VARCHAR(100),
    email VARCHAR(100),
    telefono VARCHAR(15),
    indirizzo VARCHAR(255),
    data_nascita DATE,
    eta INT
);

CREATE TABLE IF NOT EXISTS Prestiti (
    id_prestito INT PRIMARY KEY AUTO_INCREMENT,
    id_utente INT,
    id_libro INT,
    data_prestito DATE,
    data_restituzione DATE,
    FOREIGN KEY (id_utente) REFERENCES Utente(id_utente),
    FOREIGN KEY (id_libro) REFERENCES Libri(id_libro)
);

CREATE TABLE IF NOT EXISTS Catalogo (
    id_libro INT PRIMARY KEY,
    sezione VARCHAR(255),
    posizione INT,
    disponibile BOOLEAN,
    FOREIGN KEY (id_libro) REFERENCES Libri(id_libro)
);

CREATE TABLE IF NOT EXISTS Produzione (
    id_libro INT,
    id_autore INT,
    PRIMARY KEY (id_libro, id_autore),
    FOREIGN KEY (id_libro) REFERENCES Libri(id_libro),
    FOREIGN KEY (id_autore) REFERENCES Autori(id_autore)
);


-- Inserimento Autori
INSERT INTO Autori (nome, cognome, data_nascita, nazionalita, biografia) VALUES
('Dante', 'Alighieri', '1265-05-21', 'Italiana', 'Poeta italiano, autore della Divina Commedia.'),
('William', 'Shakespeare', '1564-04-23', 'Inglese', 'Drammaturgo e poeta inglese.'),
('Jane', 'Austen', '1775-12-16', 'Inglese', 'Scrittrice inglese di romanzi.'),
('Lev', 'Tolstoj', '1828-09-09', 'Russo', 'Autore di Guerra e Pace.');

-- Inserimento Libri
INSERT INTO Libri (titolo, id_autore, data_pubblicazione, isbn, prezzo, quantita) VALUES
('La Divina Commedia', 1, '1320-01-01', '978-1234567890', 25.50, 10),
('Amleto', 2, '1603-01-01', '978-2345678901', 15.75, 5),
('Orgoglio e Pregiudizio', 3, '1813-01-01', '978-3456789012', 20.00, 7),
('Guerra e Pace', 4, '1869-01-01', '978-4567890123', 35.99, 3);

-- Inserimento Utenti
INSERT INTO Utente (nome, cognome, email, telefono, indirizzo, data_nascita, eta) VALUES
('Mario', 'Rossi', 'mario.rossi@email.com', '1234567890', 'Via Roma 1, Milano', '1990-05-10', 34),
('Laura', 'Bianchi', 'laura.bianchi@email.com', '0987654321', 'Corso Venezia 5, Torino', '1985-07-20', 39),
('Giovanni', 'Verdi', 'giovanni.verdi@email.com', '1122334455', 'Piazza Duomo 10, Napoli', '2000-01-15', 24);

-- Inserimento Prestiti
INSERT INTO Prestiti (id_utente, id_libro, data_prestito, data_restituzione) VALUES
(1, 1, '2024-02-01', '2024-02-20'),
(2, 3, '2024-01-15', '2024-02-10'),
(3, 2, '2024-02-05', NULL);

-- Inserimento Catalogo
INSERT INTO Catalogo (id_libro, sezione, posizione, disponibile) VALUES
(1, 'Letteratura Italiana', 101, TRUE),
(2, 'Teatro Inglese', 202, FALSE),
(3, 'Romanzi Classici', 303, TRUE),
(4, 'Letteratura Russa', 404, TRUE);

-- Inserimento Produzione
INSERT INTO Produzione (id_libro, id_autore) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);
