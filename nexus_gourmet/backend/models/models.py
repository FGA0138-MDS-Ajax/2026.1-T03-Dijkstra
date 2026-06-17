# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from models.enums import Role, TableStatus, ProductCategory, OrderStatus

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.Enum(Role), nullable=False, default=Role.GARCOM)

    comanda = db.relationship('Order', backref='user', lazy=True)


class Table(db.Model):
    __tablename__ = 'tables'

    numero = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(TableStatus), nullable=False, default=TableStatus.LIVRE)

    comandas = db.relationship('Order', backref='table', lazy=True)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.Enum(ProductCategory), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_hora_abertura = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDENTE)

    numero_mesa = db.Column(db.Integer, db.ForeignKey('tables.numero'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    itens = db.relationship('ProductOrdered', backref='order', lazy=True, cascade="all, delete-orphan")


class ProductOrdered(db.Model):
    __tablename__ = 'itens_ordered'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    observacao = db.Column(db.String(255), nullable=True)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    product = db.relationship('Product')