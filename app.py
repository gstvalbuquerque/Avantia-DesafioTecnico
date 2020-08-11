import sqlite3
import requests
from flask import Flask, flash, jsonify, redirect, render_template, request, session,g, url_for
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import tempfile

#aplicação 
app = Flask(__name__)

# templates carregados automaticamente
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Não guardar informações no cache 
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# usar filesystem, não cookies
app.config["SESSION_FILE_DIR"] = tempfile.mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#configuração do banco de dados
conn = sqlite3.connect('avantia-sma.db', check_same_thread=False)
c = conn.cursor()

#criar o server
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

#registrar
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    else:
        # criar tabela caso não exista
        c.execute("CREATE TABLE IF NOT EXISTS accounts ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' VARCHAR(50) NOT NULL,'name' VARCHAR(100), 'lastName' VAR(250), 'email' VARCHAR(250) NOT NULL, 'hash' VARCHAR(250) NOT NULL)")

        #pegar os dados do formulário
        username = request.form.get("username")
        name = request.form.get("name").capitalize()
        lastName = request.form.get("lastName").capitalize()
        password = request.form.get("password")
        conf_password = request.form.get("conf_password")
        email = request.form.get("email")

        #conferir se as senhas conferem
        if (password != conf_password):
            flash("As senhas não são iguais!")
            return render_template("register.html")
        
        #checar na base de dados se já existe alguém com o mesmo login
        rows = c.execute("SELECT * FROM accounts WHERE username = (?)",
                          [username])
        conf_user = rows.fetchone()
        if conf_user is not None:
            flash("Nome de usuário já cadastrado!")
            return render_template("register.html")

        #chegar na base de dados se já existe alguém com o mesmo email
        email_row = c.execute("SELECT * FROM accounts WHERE email = (?)",
                          [email])
        conf_email = email_row.fetchone()
        if conf_email != None:
            flash("Email já cadastrado")
            return render_template("register.html")
        
        #inserir no banco de dados
        password=generate_password_hash(password) 
        c.execute("INSERT INTO accounts (username, name, lastName, email, hash) VALUES (?, ?, ?, ?, ?)", (username,name, lastName, email, password))
        conn.commit() 
        flash("Registrado com sucesso!")
        return render_template("login.html")

        redirect ("/login")



# fazer o login
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")