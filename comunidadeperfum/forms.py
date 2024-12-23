from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeperfum.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    btn_submit_criarconta = SubmitField('Criar Conta', validators=[])

    
    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Nome já cadastrado. Cadastre-se com outro nome ou faça login para continuar.')
        

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')
        


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_login = BooleanField('Lembrar Login.')
    btn_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    bio = StringField('Bio', validators=[Length(2, 20)])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    btn_submit_editarperfil = SubmitField('Confirmar Edição', validators=[])

    perfume_doce = BooleanField('Perfume Doce')
    perfume_citrico = BooleanField('Perfume Cítrico')
    perfume_amadeirado = BooleanField('Perfume Amadeirado')
    perfume_caramelado = BooleanField('Perfume Caramelado')
    perfume_quente = BooleanField('Perfume Quente')
    perfume_suave = BooleanField('Perfume Suave')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('E-mail em uso por outro usuário. Cadastre outro e-mail.')
            

class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu post aqui...', validators=[DataRequired()])
    btn_submit = SubmitField('Criar Post')
        