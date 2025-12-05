
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os, datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key'

DB_PATH = 'biblioteca.db'

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_conn()
        conn.execute("""CREATE TABLE libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT,
            estado TEXT
        )""")
        conn.commit()
        conn.close()

init_db()

@app.context_processor
def inject_year():
    return {'current_year': datetime.datetime.now().year}

@app.route('/')
def index():
    q = request.args.get('q','').strip()
    conn = get_conn()
    if q:
        rows = conn.execute("SELECT * FROM libros WHERE titulo LIKE ? OR autor LIKE ? OR genero LIKE ?",
                            (f'%{q}%', f'%{q}%', f'%{q}%')).fetchall()
    else:
        rows = conn.execute("SELECT * FROM libros").fetchall()
    conn.close()
    return render_template('index.html', books=rows, q=q)

@app.route('/agregar', methods=['GET','POST'])
def agregar():
    if request.method=='POST':
        titulo = request.form['titulo'].strip()
        autor = request.form['autor'].strip()
        genero = request.form['genero'].strip()
        estado = request.form['estado'].strip()
        if not titulo or not autor:
            flash('Título y autor son obligatorios.', 'danger')
            return render_template('add_edit.html', action='Agregar')
        conn = get_conn()
        conn.execute("INSERT INTO libros (titulo, autor, genero, estado) VALUES (?,?,?,?)",
                     (titulo, autor, genero, estado))
        conn.commit()
        conn.close()
        flash('Libro agregado correctamente.', 'success')
        return redirect(url_for('index'))
    return render_template('add_edit.html', action='Agregar')

@app.route('/editar/<int:book_id>', methods=['GET','POST'])
def editar(book_id):
    conn = get_conn()
    libro = conn.execute("SELECT * FROM libros WHERE id=?", (book_id,)).fetchone()
    if not libro:
        flash('Libro no encontrado.','danger')
        return redirect(url_for('index'))
    if request.method=='POST':
        titulo = request.form['titulo'].strip()
        autor = request.form['autor'].strip()
        genero = request.form['genero'].strip()
        estado = request.form['estado'].strip()
        conn.execute("UPDATE libros SET titulo=?, autor=?, genero=?, estado=? WHERE id=?",
                     (titulo, autor, genero, estado, book_id))
        conn.commit()
        conn.close()
        flash('Libro actualizado.', 'success')
        return redirect(url_for('index'))
    conn.close()
    return render_template('add_edit.html', action='Editar', book=libro)

@app.route('/eliminar/<int:book_id>', methods=['POST'])
def eliminar(book_id):
    conn = get_conn()
    conn.execute("DELETE FROM libros WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    flash('Libro eliminado.','success')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__=='__main__':
    app.run(debug=True)
