import sqlite3
import requests
from flask import Flask, flash, jsonify, redirect, render_template, request, session,g, url_for
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

#aplicação 
app = Flask(__name__)

# templates carregados automaticamente
app.config["TEMPLATES_AUTO_RELOAD"] = True
