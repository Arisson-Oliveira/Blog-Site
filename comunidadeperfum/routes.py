from flask import Flask, render_template, url_for, request, redirect, flash
from comunidadeperfum.forms import FormLogin, FormCriarConta, FormEditarPerfil, Email
from comunidadeperfum.models import Usuario
from flask_sqlalchemy import SQLAlchemy
from comunidadeperfum import app, database, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

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

            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)  
            else:
                return redirect(url_for('homepage'))
        else:
            flash('Falha no Login. E-mail ou Senha Incorretos.', 'danger')

    return render_template('login-conta.html', form_login=form_login, form_criarconta=form_criarconta)

    if form_login.errors:
        print("Erros no login:", form_login.errors) 

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

# Reduzir essa função um dia

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_completo = os.path.join(nome, codigo, extensao)
    nome_arquivo = nome + codigo + extensao

    caminho_completo = os.path.join(app.root_path, 'static/images', nome_arquivo)

    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    imagem_reduzida.save(caminho_completo)

    return nome_arquivo


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        flash(f'Perfil atualizado com sucesso.', 'success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    foto_perfil = url_for('static', filename=f'images/{current_user.foto_perfil}')

    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')
