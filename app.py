from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Configurazione MySQL
app.config['MYSQL_HOST']="138.41.20.102"
app.config['MYSQL_PORT']=53306
app.config['MYSQL_USER']="5di"
app.config['MYSQL_PASSWORD']="colazzo"
app.config['MYSQL_DB']="rampino_zinzeri"
mysql= MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        titolo = request.form['titolo']
        nome_autore = request.form['autore']
        anno = request.form['anno']
        isbn = request.form['isbn']
        genere = request.form['genere']

        cur = mysql.connection.cursor()
        
        # Controlla se l'autore esiste già
        cur.execute("SELECT id_autore FROM Autori WHERE nome = %s", (nome_autore,))
        autore = cur.fetchone()
        if not autore:
            cur.execute("INSERT INTO Autori (nome, cognome) VALUES (%s, '')", (nome_autore,))
            mysql.connection.commit()
            cur.execute("SELECT id_autore FROM Autori WHERE nome = %s", (nome_autore,))
            autore = cur.fetchone()

        id_autore = autore[0]

        # Controlla se il genere esiste già
        cur.execute("SELECT id_genere FROM Generi WHERE nome = %s", (genere,))
        genere_res = cur.fetchone()
        if not genere_res:
            cur.execute("INSERT INTO Generi (nome) VALUES (%s)", (genere,))
            mysql.connection.commit()
            cur.execute("SELECT id_genere FROM Generi WHERE nome = %s", (genere,))
            genere_res = cur.fetchone()

        id_genere = genere_res[0]

        # Inserisci il libro
        cur.execute("INSERT INTO Libri (titolo, id_autore, data_pubblicazione, isbn, id_genere) VALUES (%s, %s, %s, %s, %s)",
                    (titolo, id_autore, anno, isbn, id_genere))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('view_books'))

    return render_template('addbook.html')

@app.route('/view_books')
def view_books():
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT L.titolo, A.nome, L.data_pubblicazione, L.isbn, G.nome 
    FROM Libri L
    JOIN Autori A ON L.id_autore = A.id_autore
    JOIN Generi G ON L.id_genere = G.id_genere
    """)
    books = cur.fetchall()
    cur.close()
    return render_template('viewbook.html', books=books)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT L.titolo, A.nome, L.data_pubblicazione, L.isbn, G.nome 
    FROM Libri L
    JOIN Autori A ON L.id_autore = A.id_autore
    JOIN Generi G ON L.id_genere = G.id_genere
    WHERE L.titolo LIKE %s OR A.nome LIKE %s
    """, ('%' + query + '%', '%' + query + '%'))
    results = cur.fetchall()
    cur.close()
    return render_template('searchresults.html', results=results, query=query)

@app.route('/sort/<criteria>')
def sort_books(criteria):
    cur = mysql.connection.cursor()
    if criteria == 'titolo':
        cur.execute("""
        SELECT L.titolo, A.nome, L.data_pubblicazione, L.isbn, G.nome 
        FROM Libri L
        JOIN Autori A ON L.id_autore = A.id_autore
        JOIN Generi G ON L.id_genere = G.id_genere
        ORDER BY L.titolo ASC
        """)
    elif criteria == 'autore':
        cur.execute("""
        SELECT L.titolo, A.nome, L.data_pubblicazione, L.isbn, G.nome 
        FROM Libri L
        JOIN Autori A ON L.id_autore = A.id_autore
        JOIN Generi G ON L.id_genere = G.id_genere
        ORDER BY A.nome ASC
        """)
    books = cur.fetchall()
    cur.close()
    return render_template('view_books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
