from datetime import datetime
from dateutil.relativedelta import relativedelta

def addLibro(mysql, ISBN, titolo, categoria, autori, x, y, z):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Libri WHERE ISBN=%s"
    cursor.execute(query, (ISBN,))
    dati = cursor.fetchall()
    ritorno = 1
    if len(dati) == 0:
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

def getLibriPerKey(mysql, parolaChiave, genere):
    cursor = mysql.connection.cursor()
    parolaChiave = f"%{parolaChiave}%"
    
    if genere:
        query = "SELECT * FROM Libri WHERE (Titolo LIKE %s OR ISBN LIKE %s) AND Categoria = %s"
        cursor.execute(query, (parolaChiave, parolaChiave, genere))
    else:
        query = "SELECT * FROM Libri WHERE Titolo LIKE %s OR ISBN LIKE %s"
        cursor.execute(query, (parolaChiave, parolaChiave))
    
    titoli = cursor.fetchall()
    cursor.close()
    return [
        {'ISBN': t[0], 'Titolo': t[1], 'Categoria': t[2], 'NumCopie': t[3], 'Autori': t[4], 'Riassunto': t[5]}
        for t in titoli
    ]

def ordinaLibri(libri, tipo):
    return sorted(libri, key=lambda x: x['Titolo'] if tipo else x['Autori'])

def getStatisticheGenere(mysql, genere):
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM Libri WHERE Categoria = %s"
    cursor.execute(query, (genere,))
    risultato = cursor.fetchone()
    cursor.close()
    return risultato[0] if risultato else 0

def registraUtente(mysql, nome, cognome, CF, email, telefono, username, password):
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

def getHashedPw(mysql, username):
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

def isAdmin(mysql, username):
    cursor = mysql.connection.cursor()
    query = "SELECT IsAdmin FROM Tessera WHERE Username = %s"
    cursor.execute(query, (username,))
    risultato = cursor.fetchone()
    cursor.close()
    return risultato[0] == 1 if risultato else False

def rinnovaTessera(mysql, username):
    cursor = mysql.connection.cursor()
    query = "UPDATE Tessera SET DataScadenza = %s WHERE Username = %s"
    cursor.execute(query, (datetime.now() + relativedelta(months=2), username))
    mysql.connection.commit()
    return cursor.rowcount > 0

def aggiungiPrestito(mysql, CF, dataInizio, dataScadenza, IDL):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Utenti WHERE CF = %s"
    cursor.execute(query, (CF,))
    if not cursor.fetchall():
        return False
    query = "INSERT INTO Prestiti (DataInizio, DataRestituzione, DataScadenza, CF, IDL) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (dataInizio, None, dataScadenza, CF, IDL))
    query = "UPDATE Inventario SET isAvailable = 0 WHERE IDL = %s"
    cursor.execute(query, (IDL,))
    mysql.connection.commit()
    return True

def getIDL(mysql, x, y, z):
    cursor = mysql.connection.cursor()
    query = "SELECT IDL, isAvailable FROM Inventario WHERE x=%s AND y=%s AND z=%s"
    cursor.execute(query, (x, y, z))
    risultato = cursor.fetchone()
    cursor.close()
    if not risultato:
        return "non esistente"
    return risultato[0] if risultato[1] else "non disponibile"