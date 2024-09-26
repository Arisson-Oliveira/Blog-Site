from flask import Flask

# Inicialização da Função
app = Flask(__name__)

@app.route('/')
def homepage():
    return 'Hello comunity'

if __name__ == '__main__':
    app.run(debug=True)