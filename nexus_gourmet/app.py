import os
from flask import Flask, redirect, render_template
from backend.models.models import db
from backend.services.user_service import UserService
from backend.services.product_service import ProductService
from backend.services.order_service import OrderService
from backend.services.table_service import TableService
from backend.controllers import init_controllers

def create_app():
    """Cria e configura a instância da aplicação Flask."""
    
    # Define os caminhos absolutos para o front-end
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, 'frontend', 'views')
    static_dir = os.path.join(base_dir, 'frontend', 'static')

    # Inicializa o Flask apontando para as pastas do Front-end
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Configurações do Banco de Dados e Sessão
    db_path = os.path.join(base_dir, 'backend', 'instance', 'nexus.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'nexus_super_secret_key_flask'

    # Vincula o SQLAlchemy ao app
    db.init_app(app)

    # Cria as tabelas do banco de dados (caso não existam)
    with app.app_context():
        db.create_all()

    # Instanciando os Serviços (Regras de negócio)
    user_service = UserService()
    product_service = ProductService()
    table_service = TableService()
    # OrderService depende do TableService, conforme definido no seu __init__
    order_service = OrderService(table_service) 

    # Inicializando os Controladores (Rotas)
    init_controllers(app, user_service, order_service, table_service, product_service)

    # Rota raiz: Redireciona o usuário direto para a página de Login do front-end
    @app.route('/')
    def index():
        return redirect('/login')

    return app