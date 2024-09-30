from flask import Flask, render_template, url_for, request, redirect, flash
from forms import FormLogin, FormCriarConta
from flask_sqlalchemy import SQLAlchemy

# Inicialização da Função
app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfvbusvbdbcsubcxbufgefdg87dftrg67df'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)

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

    if form_login.validate_on_submit() and 'btn_submit_login' in request.form:
        print("Login válido")
        flash(f'Login feito com sucesso no e-mail: {form_login.email.data}')
        return redirect(url_for('homepage'))

    if form_login.errors:
        print("Erros no login:", form_login.errors)  # Adicione esta linha

    if form_criarconta.validate_on_submit() and 'btn_submit_criarconta' in request.form:
        print("Conta criada")
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}')
        return redirect(url_for('homepage'))

    if form_criarconta.errors:
        print("Erros na criação da conta:", form_criarconta.errors)  # Adicione esta linha

    return render_template('login-conta.html', form_login=form_login, form_criarconta=form_criarconta)




if __name__ == '__main__':
    app.run(debug=True)