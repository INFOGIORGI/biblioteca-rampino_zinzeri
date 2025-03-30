from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import bcrypt
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Configurazione MySQL
app.config['MYSQL_HOST'] = "138.41.20.102"
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = "5di"
app.config['MYSQL_PASSWORD'] = "colazzo"
app.config['MYSQL_DB'] = "rampino_zinzeri"
mysql = MySQL(app)

# Configurazione sessioni
app.config['SECRET_KEY'] = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=30)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Libri")
    libri = cur.fetchall()
    cur.close()
    return render_template('index.html', libri=libri)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')  # Convert to string
        cf = request.form['CF']
        nome = request.form['nome']
        cognome = request.form['cognome']
        email = request.form['email']
        telefono = request.form['telefono']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Utenti (CF, Nome, Cognome, Email, Telefono) VALUES (%s, %s, %s, %s, %s)", 
                    (cf, nome, cognome, email, telefono))
        cur.execute("INSERT INTO Tessera (CF, Nprestiti, DataScadenza, Username, Pwd, IsAdmin) VALUES (%s, %s, %s, %s, %s, %s)", 
                    (cf, 0, (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'), username, hashed_password, 0))
        mysql.connection.commit()
        cur.close()

        flash("Registrazione completata con successo!")
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT Pwd, CF, IsAdmin FROM Tessera WHERE Username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password, user[0].encode('utf-8')):
            session['user'] = username
            session['cf'] = user[1]
            session['isAdmin'] = user[2]  # Aggiungi sessione isAdmin
            flash("Login effettuato con successo!")
            return redirect(url_for('home'))
        else:
            flash("Credenziali errate.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logout effettuato.")
    return redirect(url_for('home'))

#route per aggiungere dei libri
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'user' in session:  # Verifica che l'utente sia loggato
        if request.method == 'POST':
            ISBN = request.form['ISBN']
            titolo = request.form['titolo']
            categoria = request.form['categoria']
            autore = request.form['autori']
            x = request.form['x']
            y = request.form['y']
            z = request.form['z']

            # Aggiungi il libro nel database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Libri (ISBN, titolo, categoria, autore) VALUES (%s, %s, %s, %s)",
                        (ISBN, titolo, categoria, autore))

            cur.execute("""
                INSERT INTO Inventario (ISBN, x, y, z)
                VALUES (%s, %s, %s, %s)
            """, (ISBN, x, y, z))

            mysql.connection.commit()
            cur.close()
            flash("Libro aggiunto con successo!")
            return redirect(url_for('home'))  # Reindirizza alla home page
        return render_template('add_book.html')  # Rende la pagina con il form
    else:
        flash("Devi essere loggato per aggiungere un libro.")
        return redirect(url_for('login'))  # Se l'utente non è loggato, lo rimanda alla pagina di login


# route per la ricerca dei libri
@app.route('/users', methods=['GET'])
def users():
    # Recupera i parametri dalla query string
    key = request.args.get('key', '')
    genere = request.args.get('genere', '')
    ordina = request.args.get('ordina', 'titolo')

    # Costruisci la query SQL dinamicamente in base ai parametri
    query = "SELECT * FROM Libri WHERE Titolo LIKE %s OR ISBN LIKE %s"
    params = ['%' + key + '%', '%' + key + '%']
    
    if genere:
        query += " AND Categoria LIKE %s"
        params.append('%' + genere + '%')
    
    if ordina == 'autore':
        query += " ORDER BY Autore"
    else:
        query += " ORDER BY Titolo"

    # Esegui la query e ottieni i risultati
    cur = mysql.connection.cursor()
    cur.execute(query, tuple(params))
    libri = cur.fetchall()
    
    # Conta il numero di libri nel genere selezionato
    numero_libri = None
    if genere:
        cur.execute("SELECT COUNT(*) FROM Libri WHERE Categoria LIKE %s", ('%' + genere + '%',))
        numero_libri = cur.fetchone()[0]
    
    cur.close()

    # Renderizza il template passando i risultati e i parametri di ricerca
    return render_template('users.html', libri=libri, key_selezionata=key, genere_selezionato=genere, ordina=ordina, numero_libri=numero_libri)

if __name__ == '__main__':
    app.run(debug=True)
