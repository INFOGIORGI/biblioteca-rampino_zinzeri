DROP TABLE IF EXISTS tessera;
DROP TABLE IF EXISTS prestiti;
DROP TABLE IF EXISTS inventario;
DROP TABLE IF EXISTS utenti;
DROP TABLE IF EXISTS libri;


CREATE TABLE utenti (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    cf VARCHAR(16) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE tessera (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_utente INT NOT NULL,
    data_scadenza DATE NOT NULL,
    FOREIGN KEY (id_utente) REFERENCES utenti(id) ON DELETE CASCADE
);

CREATE TABLE libri (
    ISBN VARCHAR(13) PRIMARY KEY,
    titolo VARCHAR(255) NOT NULL,
    categoria VARCHAR(100),
    autori VARCHAR(255) NOT NULL
);

CREATE TABLE inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ISBN VARCHAR(13) NOT NULL,
    x INT NOT NULL,
    y INT NOT NULL,
    z INT NOT NULL,
    UNIQUE (x, y, z),
    FOREIGN KEY (ISBN) REFERENCES libri(ISBN) ON DELETE CASCADE
);

CREATE TABLE prestiti (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_libro INT NOT NULL,
    id_utente INT NOT NULL,
    data_inizio DATE NOT NULL,
    data_scadenza DATE NOT NULL,
    FOREIGN KEY (id_libro) REFERENCES inventario(id) ON DELETE CASCADE,
    FOREIGN KEY (id_utente) REFERENCES utenti(id) ON DELETE CASCADE
);

-- Inserimento di utenti
INSERT INTO utenti (nome, cognome, cf, email, telefono, username, password_hash, is_admin) VALUES
('Mario', 'Rossi', 'RSSMRA80A01H501Z', 'mario.rossi@example.com', '1234567890', 'mrossi', 'hashedpassword1', FALSE),
('Luca', 'Bianchi', 'BNCPLC85B02F205X', 'luca.bianchi@example.com', '0987654321', 'lbianchi', 'hashedpassword2', TRUE),
('Giulia', 'Verdi', 'VRDGLI90C03L219Y', 'giulia.verdi@example.com', '1122334455', 'gverdi', 'hashedpassword3', FALSE),
('Laura', 'Neri', 'NRILRA75D04M345T', 'laura.neri@example.com', '2233445566', 'lneri', 'hashedpassword4', FALSE),
('Andrea', 'Gialli', 'GLLAND85E05P432J', 'andrea.gialli@example.com', '3344556677', 'agialli', 'hashedpassword5', TRUE),
('Sara', 'Blu', 'BLUSRA95F06Q567L', 'sara.blu@example.com', '4455667788', 'sblu', 'hashedpassword6', FALSE),
('Marco', 'Viola', 'VIOMAR88G07R678P', 'marco.viola@example.com', '5566778899', 'mviola', 'hashedpassword7', FALSE);

-- Inserimento di tessere
INSERT INTO tessera (id_utente, data_scadenza) VALUES
(1, '2025-12-31'),
(2, '2026-06-30'),
(3, '2025-09-15'),
(4, '2026-03-20'),
(5, '2025-11-10'),
(6, '2026-01-05'),
(7, '2025-07-25');

-- Inserimento di autori e libri
INSERT INTO libri (ISBN, titolo, categoria, autori) VALUES
('9780141439600', 'Pride and Prejudice', 'Romanzo', 'Jane Austen'),
('9780140449136', 'Crime and Punishment', 'Romanzo', 'Fyodor Dostoevsky'),
('9780061120084', 'To Kill a Mockingbird', 'Romanzo', 'Harper Lee'),
('9780451524935', '1984', 'Distopia', 'George Orwell'),
('9780679783268', 'The Great Gatsby', 'Romanzo', 'F. Scott Fitzgerald'),
('9780743273565', 'Moby-Dick', 'Avventura', 'Herman Melville'),
('9780141182803', 'Ulysses', 'Modernismo', 'James Joyce');

-- Inserimento di libri nell'inventario
INSERT INTO inventario (ISBN, x, y, z) VALUES
('9780141439600', 1, 1, 1),
('9780140449136', 1, 2, 1),
('9780061120084', 1, 3, 1),
('9780451524935', 2, 1, 1),
('9780679783268', 2, 2, 1),
('9780743273565', 2, 3, 1),
('9780141182803', 3, 1, 1);

-- Inserimento di prestiti
INSERT INTO prestiti (id_libro, id_utente, data_inizio, data_scadenza) VALUES
(1, 2, '2025-03-01', '2025-04-01'),
(2, 3, '2025-03-05', '2025-04-05'),
(3, 4, '2025-03-10', '2025-04-10'),
(4, 5, '2025-03-15', '2025-04-15'),
(5, 6, '2025-03-20', '2025-04-20'),
(6, 7, '2025-03-25', '2025-04-25'),
(7, 1, '2025-03-30', '2025-04-30');
