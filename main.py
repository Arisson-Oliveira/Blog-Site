from flask import Flask, render_template, url_for


# Inicialização da Função
app = Flask(__name__)

lista_usuarios = ['Arisson', 'Welisson']

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login-conta')
def loginconta():
    return render_template('login-conta.html')



if __name__ == '__main__':
    app.run(debug=True)