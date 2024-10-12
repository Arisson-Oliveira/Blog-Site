from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Inicialização da Função
app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfvbusvbdbcsubcxbufgefdg87dftrg67df'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view  = 'loginconta'
login_manager.login_message_category = 'alert-info'

from comunidadeperfum import routes