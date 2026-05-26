# É responsável por criar e configurar a aplicação. 
# Ele inicia os middlewares de sessão 
# (para manter o usuário logado usando a biblioteca Beaker), 
# configura as rotas iniciais e inicia os controladores.


# from bottle import Bottle, template, request, redirect
# from beaker.middleware import SessionMiddleware
# from config import Config
# from controllers import init_controllers
# from controllers.base_controller import BaseController
# from services.livro_service import LivroService

# session_opts = {
#     'session.type': 'file',
#     'session.cookie_expires': 3600,
#     'session.data_dir': './.sessions',
#     'session.auto': True,
#     'session.secret': Config.SECRET_KEY
# }

# def create_app():
#     """Cria e configura a instância da aplicação Bottle."""
#     base_app = Bottle()

#     @base_app.route('/')
#     def home_page():
#         livro_service = LivroService()
#         livros_em_destaque = livro_service.get_all()[:3]        
#         session = request.environ.get('beaker.session')
#         return template('index', livros=livros_em_destaque, session=session)

#     init_controllers(base_app)
#     base_controller = BaseController(base_app)
#     base_controller.setup_routes()
    
#     app_with_session = SessionMiddleware(base_app, session_opts)    
#     return app_with_session