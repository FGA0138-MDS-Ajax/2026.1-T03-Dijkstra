import os
from flask import Flask
from flask_cors import CORS
from backend.models.models import db
from backend.services.user_service import UserService
from backend.services.product_service import ProductService
from backend.services.order_service import OrderService
from backend.services.table_service import TableService
from backend.controllers import init_controllers

def create_app():
    """Cria e configura a instância da aplicação Flask como API REST."""
    app = Flask(__name__)
    
    # Habilita o CORS permitindo envio de cookies/sessões do React para o Flask
    CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

    # Configurações do Banco de Dados
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'backend', 'instance', 'nexus.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'nexus_super_secret_key_flask'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    user_service = UserService()
    product_service = ProductService()
    table_service = TableService()
    order_service = OrderService(table_service) 

    init_controllers(app, user_service, order_service, table_service, product_service)

    return app
