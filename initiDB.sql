DROP IF EXIST Libri
DROP IF EXIST Autori
DROP IF EXIST Utente
DROP IF EXIST Prestiti
DROP IF EXIST Catalogo
DROP IF EXIST Produzione

CREATE TABLE IF NOT EXIST Libri (
    id_libro INT PRIMARY KEY AUTO_INCREMENT,
    titolo VARCHAR(255),
    id_autore INT,
    data_pubblicazione DATE,
    isbn VARCHAR(20),
    prezzo DECIMAL(10, 2),
    quantita INT,
    FOREIGN KEY (id_autore) REFERENCES Autori(id_autore)
);
CREATE TABLE IF NOT EXIST Autori (
    id_autore INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    cognome VARCHAR(100),
    data_nascita DATE,
    nazionalita VARCHAR(50),
    biografia VARCHAR(255)
);
CREATE TABLE IF NOT EXIST Utente (
    id_utente INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    cognome VARCHAR(100),
    email VARCHAR(100),
    telefono VARCHAR(15),
    indirizzo VARCHAR(255)
    data_nascita DATE,
    eta int
);
CREATE TABLE IF NOT EXIST Prestiti (
    id_prestito INT PRIMARY KEY ,
    id_utente INT,
    id_libro INT,
    data_prestito DATE,
    data_restituzione DATE,
    FOREIGN KEY (id_utente) REFERENCES Utente(id_utente),
    FOREIGN KEY (id_libro) REFERENCES Libri(id_libro)
);

CREATE TABLE IF NOT EXIST Catalogo(
    id_libro INT,
    sezione VARCHAR(255),
    posizione INT,
    disponibile BOOLEAN,
    FOREIGN KEY (id_libro) REFERENCES Libri(id_libro)
);

CREATE TABLE IF NOT EXIST Produzione(
    id_libro INT,
    id_autore INT,
    FOREIGN KEY (id_libro) REFERENCES Libri(id_libro),
    FOREIGN KEY (id_autore) REFERENCES Libri(id_autore)
);

INSERT INTO Libri(1,"Harry Pot", 1,1997, "9780747532743", 19.99, 100);
INSERT INTO Autori(2, "J.K.", "Rowling", "1965-07-31", "Britannica","nata a Nociglia il 7 marzo");
INSERT INTO Utente(3,"marco","rampino","marco@gmail.com", "3334445555","via mussolini 19","30/10/2003","21");
INSERT INTO Prestiti(1,"Harry Pot", 1,1997, "9780747532743", 19.99, 100);
INSERT INTO Catalogo(1,"Harry Pot", 1,1997, "9780747532743", 19.99, 100);
INSERT INTO Produzione(1,"Harry Pot", 1,1997, "9780747532743", 19.99, 100);