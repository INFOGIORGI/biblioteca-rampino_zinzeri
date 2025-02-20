from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import db
import json

app = Flask(__name__)
app.secret_key = "super secret key"


app.config['MYSQL_HOST'] = ''
app.config['MYSQL_PORT'] = 1
app.config['MYSQL_USER'] = 'ospite'
app.config['MYSQL_PASSWORD'] = 'ospite'
app.config['MYSQL_DB'] = 'w3schools'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        titolo = request.form['titolo']
        autore = request.form['autore']
        anno = request.form['anno']
        isbn = request.form['isbn']
        genere = request.form['genere']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Libri (titolo, id_autore, data_pubblicazione, isbn, quantita) VALUES (%s, %s, %s, %s, 1)",
                    (titolo, autore, anno, isbn))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('view_books'))
    return render_template('add_book.html')

@app.route('/view_books')
def view_books():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Libri")
    books = cur.fetchall()
    cur.close()
    return render_template('view_books.html', books=books)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Libri WHERE titolo LIKE %s OR id_autore IN (SELECT id_autore FROM Autori WHERE nome LIKE %s OR cognome LIKE %s)", 
                ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    results = cur.fetchall()
    cur.close()
    return render_template('search_results.html', results=results, query=query)

@app.route('/sort/<criteria>')
def sort_books(criteria):
    cur = mysql.connection.cursor()
    if criteria == 'titolo':
        cur.execute("SELECT * FROM Libri ORDER BY titolo ASC")
    elif criteria == 'autore':
        cur.execute("SELECT L.*, A.nome, A.cognome FROM Libri L JOIN Autori A ON L.id_autore = A.id_autore ORDER BY A.cognome ASC")
    books = cur.fetchall()
    cur.close()
    return render_template('view_books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
