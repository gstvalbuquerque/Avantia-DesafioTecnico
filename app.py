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
conn = sqlite3.connect('investsimples.db', check_same_thread=False)
c = conn.cursor()

#criar o server
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

#registrar
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

# fazer o login
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")