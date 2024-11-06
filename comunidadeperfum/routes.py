from flask import Flask, render_template, url_for, request, redirect, flash, abort
from comunidadeperfum.forms import FormLogin, FormCriarConta, FormEditarPerfil,FormCriarPost, Email
from comunidadeperfum.models import Usuario, Post
from flask_sqlalchemy import SQLAlchemy
from comunidadeperfum import app, database, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

lista_usuarios = []

@app.route('/')
def homepage():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login-conta', methods=['GET', 'POST'])
def loginconta():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'btn_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_login.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('homepage'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'btn_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('homepage'))
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


def atualizar_perfumes(form):
    lista_perfumes = []
    for campo in form:
        if 'perfume_' in campo.name:
            if campo.data:
                lista_perfumes.append(campo.label.text)
    return ';'.join(lista_perfumes)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.perfumes = atualizar_perfumes(form)
        database.session.commit()
        flash(f'Perfil atualizado com sucesso.', 'success')
        return redirect(url_for('perfil'))
    
    elif request.method == 'GET':
        # Preencher os campos com os dados atuais do usuário
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.perfil_bio

        if form.bio.data:
            current_user.perfil_bio = form.bio.data
        
        # Obter perfumes do usuário e preencher os campos booleanos
        perfumes_usuario = current_user.perfumes.split(';') if current_user.perfumes else []
        for campo in form:
            if 'perfume_' in campo.name:  # Verifica se o campo é de perfume
                if campo.label.text in perfumes_usuario:  # Marca o campo se o perfume estiver nos perfumes do usuário
                    campo.data = True
    foto_perfil = url_for('static', filename=f'images/{current_user.foto_perfil}')

    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso!', 'success')
        return redirect(url_for('homepage'))
    return render_template('criarpost.html', form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    
    if post is None:
        flash('Postagem não encontrada.', 'danger')
        return redirect(url_for('homepage'))
    
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data

            database.session.commit()
            flash('Postagem editada com sucesso.', 'success')
            return redirect(url_for('homepage'))
    else:
        form = None

    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Postagem deletada com sucesso.', 'danger')
    else:
        abort(403)
        
    return redirect(url_for('homepage'))