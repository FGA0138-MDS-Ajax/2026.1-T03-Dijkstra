from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

from models.enums import Role, TableStatus, ProductCategory, OrderStatus

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    cpf = db.Column(db.String(11), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.Enum(Role), nullable=False, default=Role.GARCOM)
    foto_usuario = db.Column(db.String(255), nullable=True)

    comandas = db.relationship('Order', backref='user', lazy=True)

    def to_dict(self):
        return {
            "cpf": self.cpf,
            "nome": self.nome,
            "cargo": self.cargo.name,
            "foto_usuario": self.foto_usuario
        }

class Table(db.Model):
    __tablename__ = 'tables'

    numero = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(TableStatus), nullable=False, default=TableStatus.LIVRE)

    comandas = db.relationship('Order', backref='table', lazy=True)

    def to_dict(self):
        return {
            "numero": self.numero,
            "capacidade": self.capacidade,
            "status": self.status.value
        }

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.Enum(ProductCategory), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    tempo_preparacao = db.Column(db.Integer, nullable=False, default=15)
    foto_prato = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria.value,
            "preco": float(self.preco),
            "tempo_preparacao": self.tempo_preparacao,
            "foto_produto": self.foto_prato
        }

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_diario = db.Column(db.Integer, nullable=False)
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    entrada_cozinha = db.Column(db.DateTime)
    saida_cozinha = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDENTE)
    itens = db.relationship('ProductOrdered', backref='order', lazy=True, cascade="all, delete-orphan")

    numero_mesa = db.Column(db.Integer, db.ForeignKey('tables.numero'), nullable=False)
    user_cpf = db.Column(db.String(11), db.ForeignKey('users.cpf'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "numero_diario": self.numero_diario,
            "entrada_cozinha": self.entrada_cozinha.isoformat() if self.entrada_cozinha else None,
            "saida_cozinha": self.saida_cozinha.isoformat() if self.saida_cozinha else None,
            "status": self.status.value,
            "itens": [item.to_dict() for item in self.itens],
            "numero_mesa": self.numero_mesa,
            "user_cpf": self.user_cpf            
        }

class ProductOrdered(db.Model):
    __tablename__ = 'itens_ordered'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    observacao = db.Column(db.String(255), nullable=True)
    cozinha_status = db.Column(db.String(20), default='PENDENTE')

    preco_vendido = db.Column(db.Float, nullable=False, default=0.0)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    product = db.relationship('Product')

    def to_dict(self):
        return {
            "id": self.id,
            "quantidade": self.quantidade,
            "observacao": self.observacao,
            "cozinha_status": self.cozinha_status,
            "product_id": self.product_id,
            "produto": self.product.to_dict() if self.product else None
        }