CREATE TABLE Libri (
    id_libro INT PRIMARY KEY AUTO_INCREMENT,
    titolo VARCHAR(255),
    id_autore INT,
    data_pubblicazione DATE,
    isbn VARCHAR(20),
    prezzo DECIMAL(10, 2),
    quantita INT,
    FOREIGN KEY (id_autore) REFERENCES Autori(id_autore)
);
CREATE TABLE Autori (
    id_autore INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    cognome VARCHAR(100),
    data_nascita DATE,
    nazionalita VARCHAR(50),
    biografia VARCHAR(255)
);
CREATE TABLE Utente (
    id_utente INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    cognome VARCHAR(100),
    email VARCHAR(100),
    telefono VARCHAR(15),
    indirizzo VARCHAR(255)
    data_nascita DATE,
    eta int
);
CREATE TABLE Prestiti (
    id_prestito INT PRIMARY KEY ,
    id_utente INT,
    id_libro INT,
    data_prestito DATE,
    data_restituzione DATE,
    FOREIGN KEY (id_utente) REFERENCES Utente(id_utente),
    FOREIGN KEY (id_libro) REFERENCES Libri(id_libro)
);

CREATE TABLE Catalogo(
    id_libro INT,
    sezione VARCHAR(255),
    posizione INT,
    disponibile BOOLEAN,
    FOREIGN KEY (id_libro) REFERENCES Libri(id_libro)

)

CREATE TABLE Produzione(
    id_libro INT
    id_autore INT
    FOREIGN KEY (id_libro) REFERENCES Libri(id_libro)
    FOREIGN KEY (id_autore) REFERENCES Libri(id_autore)
)

INSERT INTO Libri(1,"Harry Pot", 1,1997, "9780747532743", 19.99, 100")
