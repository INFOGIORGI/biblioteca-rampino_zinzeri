import MySQLdb

# Configurazione della connessione al database
DB_CONFIG = {
    'host': '138.41.20.102',  # Inserisci l'host del database
    'port': 53306,   # Inserisci la porta del database
    'user': '5di',
    'password': 'colazzo',
    'database': 'rampino_zinzeri'
}

def create_tables():
    try:
        conn = MySQLdb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Creazione tabella Autori
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Autori (
                id_autore INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                cognome VARCHAR(255) NOT NULL
            )
        ''')
        
        # Creazione tabella Generi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Generi (
                id_genere INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL UNIQUE
            )
        ''')
        
        # Creazione tabella Libri
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Libri (
                id_libro INT AUTO_INCREMENT PRIMARY KEY,
                titolo VARCHAR(255) NOT NULL,
                id_autore INT,
                data_pubblicazione YEAR,
                isbn VARCHAR(20) UNIQUE,
                id_genere INT,
                quantita INT DEFAULT 1,
                FOREIGN KEY (id_autore) REFERENCES Autori(id_autore) ON DELETE SET NULL,
                FOREIGN KEY (id_genere) REFERENCES Generi(id_genere) ON DELETE SET NULL
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Tabelle create con successo.")
    except MySQLdb.Error as e:
        print(f"Errore durante la creazione delle tabelle: {e}")

if __name__ == "__main__":
    create_tables()
