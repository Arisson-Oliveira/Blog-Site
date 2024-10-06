from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Inicialização da Função
app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfvbusvbdbcsubcxbufgefdg87dftrg67df'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from comunidadeperfum import routes