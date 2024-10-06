from main import app, database  # Importa o app e o database
from models import Usuario, Post

with app.app_context():
    database.drop_all()  # Remove as tabelas
    database.create_all()  # Cria as tabelas
