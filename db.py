from datetime import datetime
from dateutil.relativedelta import relativedelta

def add_libro(mysql, ISBN, titolo, categoria, autori, x, y, z):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Libri WHERE ISBN=%s"
    cursor.execute(query, (ISBN,))
    dati = cursor.fetchall()
    ritorno = 1
    if not dati:
        query = "INSERT INTO Libri(ISBN, Titolo, Categoria, NumCopie, Autori) VALUES (%s, %s, %s, 0, %s)"
        cursor.execute(query, (ISBN, titolo, categoria, autori))
        mysql.connection.commit()
        ritorno = 2
    
    query = "SELECT * FROM Inventario WHERE x = %s AND y = %s AND z = %s"
    cursor.execute(query, (x, y, z))
    if cursor.fetchall():
        return 0
    
    query = "INSERT INTO Inventario(ISBN, x, y, z) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (ISBN, x, y, z))
    query = "UPDATE Libri SET NumCopie = NumCopie + 1 WHERE ISBN = %s"
    cursor.execute(query, (ISBN,))
    mysql.connection.commit()
    cursor.close()
    return ritorno

def get_libri_per_key(mysql, parola_chiave, genere):
    cursor = mysql.connection.cursor()
    parola_chiave = f"%{parola_chiave}%"
    
    query = "SELECT * FROM Libri WHERE (Titolo LIKE %s OR ISBN LIKE %s)"
    params = [parola_chiave, parola_chiave]
    
    if genere:
        query += " AND Categoria = %s"
        params.append(genere)
    
    cursor.execute(query, tuple(params))
    titoli = cursor.fetchall()
    cursor.close()
    return [{
        'ISBN': t[0], 'Titolo': t[1], 'Categoria': t[2], 'NumCopie': t[3], 'Autori': t[4], 'Riassunto': t[5]
    } for t in titoli]

def ordina_libri(libri, tipo):
    return sorted(libri, key=lambda x: x['Titolo'] if tipo else x['Autori'])

def get_statistiche_genere(mysql, genere):
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM Libri WHERE Categoria = %s"
    cursor.execute(query, (genere,))
    risultato = cursor.fetchone()
    cursor.close()
    return risultato[0] if risultato else 0

def registra_utente(mysql, nome, cognome, CF, email, telefono, username, password):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Utenti WHERE CF = %s"
    cursor.execute(query, (CF,))
    if cursor.fetchall():
        return False
    query = "INSERT INTO Utenti (CF, Nome, Cognome, Email, Telefono) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (CF, nome, cognome, email, telefono))
    query = "INSERT INTO Tessera (CF, Nprestiti, DataScadenza, username, Pwd, IsAdmin) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (CF, 0, datetime.now() + relativedelta(months=2), username, password, 0))
    mysql.connection.commit()
    return True

def get_hashed_pw(mysql, username):
    cursor = mysql.connection.cursor()
    query = "SELECT Pwd, DataScadenza FROM Tessera WHERE Username = %s"
    cursor.execute(query, (username,))
    risultato = cursor.fetchone()
    cursor.close()
    if not risultato:
        return 0
    if risultato[1] < datetime.now().date():
        return 2
    return risultato[0]

def is_admin(mysql, username):
    cursor = mysql.connection.cursor()
    query = "SELECT IsAdmin FROM Tessera WHERE Username = %s"
    cursor.execute(query, (username,))
    risultato = cursor.fetchone()
    cursor.close()
    return bool(risultato[0]) if risultato else False

def rinnova_tessera(mysql, username):
    cursor = mysql.connection.cursor()
    query = "UPDATE Tessera SET DataScadenza = %s WHERE Username = %s"
    cursor.execute(query, (datetime.now() + relativedelta(months=2), username))
    mysql.connection.commit()
    return cursor.rowcount > 0

def aggiungi_prestito(mysql, CF, data_inizio, data_scadenza, IDL):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Utenti WHERE CF = %s"
    cursor.execute(query, (CF,))
    if not cursor.fetchall():
        return False
    query = "INSERT INTO Prestiti (DataInizio, DataRestituzione, DataScadenza, CF, IDL) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (data_inizio, None, data_scadenza, CF, IDL))
    mysql.connection.commit()
    return True

def get_idl(mysql, x, y, z):
    cursor = mysql.connection.cursor()
    query = "SELECT IDL FROM Inventario WHERE x=%s AND y=%s AND z=%s"
    cursor.execute(query, (x, y, z))
    risultato = cursor.fetchone()
    cursor.close()
    return risultato[0] if risultato else "non esistente"
