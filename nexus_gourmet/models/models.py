# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from enums import PerfilUsuario, StatusMesa, CategoriaProduto, StatusPedido

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.Enum(PerfilUsuario), nullable=False, default=PerfilUsuario.GARCOM)

    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)


class Mesa(db.Model):
    __tablename__ = 'mesas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(StatusMesa), nullable=False, default=StatusMesa.LIVRE)

    pedidos = db.relationship('Pedido', backref='mesa', lazy=True)


class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.Enum(CategoriaProduto), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)


class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_hora_abertura = db.Column(db.DateTime, default=datetime.utcnow)
    status_pedido = db.Column(db.Enum(StatusPedido), nullable=False, default=StatusPedido.PENDENTE)
    
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesas.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade="all, delete-orphan")


class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    observacao = db.Column(db.String(255), nullable=True)

    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    
    produto = db.relationship('Produto')