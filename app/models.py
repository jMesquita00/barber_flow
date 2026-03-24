from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    agendamentos = db.relationship('Booking', backref='cliente', lazy=True)



class Barbearia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    # NOVA LINHA: Liga a barbearia ao usuário que a criou
    dono_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    agendamentos = db.relationship('Booking', backref='salao', lazy=True)




class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    servico = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pendente') # pendente, concluido, cancelado
    valor = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # A CHAVE ESTRANGEIRA FICA AQUI:
    barbearia_id = db.Column(db.Integer, db.ForeignKey('barbearia.id'), nullable=False)
