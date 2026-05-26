# Arquivo responsável por importar e 
# ativar todos os controladores de uma vez no sistema.


# from bottle import Bottle
# from controllers.user_controller import UserController
# from controllers.livro_controller import LivroController
# from controllers.auth_controller import AuthController
# from services.user_service import UserService
# from services.livro_service import LivroService
# from services.categoria_service import CategoriaService

# def init_controllers(app: Bottle):
#     """Inicializa os controladores e os registra no aplicativo Bottle."""
#     user_service = UserService()
#     livro_service = LivroService()
#     categoria_service = CategoriaService()

#     AuthController(app, user_service)
#     UserController(app, user_service, livro_service)
#     LivroController(app, livro_service, user_service, categoria_service)