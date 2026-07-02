import sys
import os
import pytest
from flask import Flask

# Ajuste do path para encontrar a pasta raiz do backend
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from models.models import User, Table, Product, db
from models.enums import Role, TableStatus, ProductCategory
from services.user_service import UserService
from services.table_service import TableService
from services.order_service import OrderService
from services.product_service import ProductService

from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:#Pr0j3to5MD5@127.0.0.1:3306/nexus_db' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'chave_secreta_testes' 
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        #apaga todas as tabelas do nexus_db após os testes
        db.drop_all()

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

@pytest.fixture
def client(app, user_service, table_service, order_service, product_service):
    # Importar controllers localmente
    from controllers.user_controller import UserController
    from controllers.order_controller import OrderController
    from controllers.table_controller import TableController
    from controllers.product_controller import ProductController
    
    # Registar as rotas na aplicação Flask
    UserController(app, user_service, order_service)
    OrderController(app, user_service, order_service, table_service)
    TableController(app, user_service, table_service)
    ProductController(app, user_service, product_service)
    
    with app.test_client() as client:
        yield client

@pytest.fixture
def dados_iniciais(app):
    garcom = User(cpf="12345678901", nome="João Garçom", senha=generate_password_hash("Senha123!"), cargo=Role.GARCOM)
    admin = User(cpf="27791093197", nome="Chefia Admin", senha=generate_password_hash("SenhaAdmin!"), cargo=Role.ADMINISTRADOR)
    cozinheiro = User(cpf="09427827122", nome="Carlos Cozinha", senha=generate_password_hash("SenhaCozinha!"), cargo=Role.COZINHEIRO)

    mesa = Table(numero=5, capacidade=4, status=TableStatus.LIVRE)
    produto = Product(nome="Hambúrguer", preco=20.50, categoria=ProductCategory.PRATO)
    
    db.session.add_all([garcom, admin, cozinheiro, mesa, produto])
    db.session.commit()
    
    return {
        "garcom": garcom,
        "admin": admin,
        "cozinheiro": cozinheiro,
        "mesa": mesa,
        "produto": produto
    }