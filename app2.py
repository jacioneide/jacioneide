from flask import Flask, redirect, render_template, url_for, request, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "segredo"

def obter_conexao():
    conexao = sqlite3.connect('banco.db')
    conexao.row_factory = sqlite3.Row
    return conexao

@app.route('/')
def index():
    if 'usuario_id' in session:
        return render_template('index.html', nome=session['usuario_nome'])
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        email = request.form.get('email')

        if not nome or not senha or not email:
            flash("Preencha todos os campos", "erro")
            return redirect(url_for('cadastro'))

        senha_hash = generate_password_hash(senha)

        conn = obter_conexao()
        SQL = "INSERT INTO users(nome, senha, email) VALUES (?, ?, ?)"
        conn.execute(SQL, (nome, senha_hash, email))
        conn.commit()
        conn.close()

        flash("Usuário cadastrado com sucesso!", "sucesso")
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('senha')

        conn = obter_conexao()
        usuario = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if usuario and check_password_hash(usuario["senha"], senha):
            session['usuario_id'] = usuario["id"]
            session['usuario_nome'] = usuario["nome"]
            flash("Login bem-sucedido!", "sucesso")
            return redirect(url_for('index'))
        else:
            flash("Email ou senha incorretos", "erro")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logout realizado com sucesso", "sucesso")
    return redirect(url_for('login'))
