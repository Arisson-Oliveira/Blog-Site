from flask import Flask, render_template, url_for
from forms import FormLogin, FormCriarConta

# Inicialização da Função
app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfvbusvbdbcsubcxbufgefdg87dftrg67df'

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

@app.route('/login-conta', methods=['GET', 'POST'])
def loginconta():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    return render_template('login-conta.html', form_login=form_login, form_criarconta=form_criarconta)



if __name__ == '__main__':
    app.run(debug=True)