from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Aluno(db.Model):
    __tablename__ = 'aluno'

    id_aluno = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(300), nullable=False)
    data_nascimento = db.Column(db.String(30), nullable=False)
    celular = db.Column(db.String(30), nullable=False)
    endereco = db.Column(db.String(300), nullable=False)
    cpf = db.Column(db.String(30), nullable=False, unique=True)
    foto_perfil = db.Column(db.String(300), nullable=True)
    email = db.Column(db.String(300), nullable=False, unique=True)
    senha = db.Column(db.String(300), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)