import pytest
from flask import Flask
from models.models import db
from services.user_service import UserService
from services.table_service import TableService
from services.order_service import OrderService
from services.product_service import ProductService

# Cria uma aplicação Flask falsa apenas para os testes
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Banco em memória (muito rápido)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all() # Cria as tabelas vazias
        yield app       # Entrega o app para o teste rodar
        db.session.remove()
        db.drop_all()   # Apaga as tabelas depois do teste

# Injeção das classes de serviço para os testes
@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def table_service():
    return TableService()

@pytest.fixture
def order_service(table_service):
    return OrderService(table_service)

@pytest.fixture
def product_service():
    return ProductService()

# No test/conftest.py
@pytest.fixture
def dados_iniciais():
    from models.models import User, Table, Product, db
    from models.enums import Role, TableStatus, ProductCategory
    
    garcom = User(nome="João Garçom", senha="123", cargo=Role.GARCOM)
    mesa = Table(numero=5, capacidade=4, status=TableStatus.LIVRE)
    produto = Product(nome="Hambúrguer", preco=20.50, categoria=ProductCategory.PRATO)
    db.session.add_all([garcom, mesa, produto])
    db.session.commit()
    return garcom, mesa, produto