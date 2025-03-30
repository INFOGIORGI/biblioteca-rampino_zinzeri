from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import bcrypt
import db
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = "138.41.20.102"
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = "5di"
app.config['MYSQL_PASSWORD'] = "colazzo"
app.config['MYSQL_DB'] = "rampino_zinzeri"
mysql = MySQL(app)

# Genera una secret key casuale (consigliato):
app.config['SECRET_KEY'] = os.urandom(24)

app.permanent_session_lifetime = timedelta(days=30) # Session Life Time
app.config['SESSION_TYPE'] = "filesystem"  # Session Storage Type

@app.route('/')
def home():
    libri = db.getLibriPerKey(mysql, "", "")
    return render_template('index.html', libri=libri)

@app.route('/librarian', methods=['GET', 'POST'])
def librarian():
    if request.method == 'POST':
        form_type = request.form['form_type']
        if form_type == 'aggiunta_libro':
            ISBN = request.form['ISBN']
            titolo = request.form['titolo']
            categoria = request.form['categoria']
            autori = request.form['autori']
            x = request.form['x']
            y = request.form['y']
            z = request.form['z']
            ritorno = db.addLibro(mysql, ISBN, titolo, categoria, autori, x, y, z)
            if ritorno == 0:
                flash("Esiste già un libro in questa posizione")
            elif ritorno == 2:
                flash("Il libro è stato memorizzato per la prima volta")
            return redirect(url_for('librarian'))
        elif form_type == 'rinnovo_tessera':
            username = request.form['username']
            if not db.rinnovaTessera(mysql, username):
                flash("Username inesistente")
            else:
                flash("Tessera aggiornata con successo")
            return redirect(url_for('librarian'))
        elif form_type == 'aggiunta_prestito':
            x = request.form['x']
            y = request.form['y']
            z = request.form['z']
            idl = db.getIDL(mysql, x, y, z)

            if idl == "non disponibile":
                flash("Libro già in prestito")
            elif idl == "non esistente":
                flash(f"Non esiste nessun libro in posizione {x}, {y}, {z}")
            else:
                cf = request.form['CF']
                dataInizio = request.form['dataInizio']
                dataScadenza = datetime.now() + relativedelta(months=1)
                if db.aggiungiPrestito(mysql, cf, dataInizio, dataScadenza, idl):
                    flash("Prestito aggiunto con successo")
                else:
                    flash("Codice fiscale inesistente")
            return redirect(url_for('librarian'))
    
    return render_template('librarian.html')

@app.route('/users')
def users():
    key = request.args.get('key', '')
    genere = request.args.get('genere', '')
    ordina = request.args.get('ordina', '')  # "titolo" o "autore"

    libri = db.getLibriPerKey(mysql, key, genere)
    numero_libri = db.getStatisticheGenere(mysql, genere)

    if ordina == "titolo":
        libri = db.ordinaLibri(libri, tipo=True)
    elif ordina == "autore":
        libri = db.ordinaLibri(libri, tipo=False)

    return render_template('users.html', libri=libri, numero_libri=numero_libri, genere_selezionato=genere, key_selezionata=key, ordina=ordina)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        cf = request.form['CF']
        password_hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        if db.registraUtente(mysql, request.form['nome'], request.form['cognome'], cf, request.form['email'], request.form['telefono'], username, password_hashed):
            session['user'] = username
            flash(f"Successfully registered username - {session['user']}.")
            session['isAdmin'] = False
        else:
            flash(f"L'utente con codice fiscale: {cf} è già registrato.")
            return redirect(url_for("register"))
        return redirect(url_for("home"))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def logIn():
    if request.method == "POST":
        username = request.form['username']
        risultato = db.getHashedPw(mysql, username)
        if risultato == 0:
            flash(f"L'username {username} non esiste")
        elif risultato == 2:
            flash(f"La tessera è scaduta, rivolgersi al bibliotecario per rinnovarla")
        else:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), risultato.encode('utf-8')):
                session['user'] = username
                flash(f"Log in avvenuto con successo, bentornato {username}")
                session['isAdmin'] = db.isAdmin(mysql, username)
                return redirect(url_for("home"))
            else:
                flash(f"Password errata")
                return redirect(url_for("logIn"))
    return render_template('login.html')

@app.route('/logout')
def logOut():
    session.clear()
    flash("Log out effettuato con successo")
    response = redirect(url_for('home'))
    response.set_cookie('session', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)