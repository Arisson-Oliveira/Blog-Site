from flask import Flask, render_template, url_for, request, redirect, flash
from comunidadeperfum.forms import FormLogin, FormCriarConta, FormEditarPerfil, Email
from comunidadeperfum.models import Usuario
from flask_sqlalchemy import SQLAlchemy
from comunidadeperfum import app, database, bcrypt
from flask_login import login_user, logout_user, current_user, login_required

lista_usuarios = []

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login-conta', methods=['GET', 'POST'])
def loginconta():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'btn_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_login.data)
            print("Login válido")
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'success')
            par_next  = request.args.get('next')
            if par_next:
                return render_template(par_next)
            else:
                return redirect(url_for('homepage'))
        else:
            flash('Falha no Login. E-mail ou Senha Incorretos.', 'danger')

    if form_login.errors:
        print("Erros no login:", form_login.errors)  # Adicione esta linha

    if form_criarconta.validate_on_submit() and 'btn_submit_criarconta' in request.form:
        print("Conta criada")
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data,senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'success')
        return redirect(url_for('homepage'))

    if form_criarconta.errors:
        print("Erros na criação da conta:", form_criarconta.errors)  # Adicione esta linha

    return render_template('login-conta.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'success')
    return redirect(url_for('homepage'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'images/{current_user.foto_perfil}')
    
    return render_template('perfil.html', usuario=current_user, foto_perfil=foto_perfil)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    foto_perfil = url_for('static', filename=f'images/{current_user.foto_perfil}')

    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')
