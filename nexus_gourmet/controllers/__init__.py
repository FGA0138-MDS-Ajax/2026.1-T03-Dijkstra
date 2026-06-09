from .user_controller import UserController
from .order_controller import PedidoController
from .product_controller import ProdutoController

def init_controllers(app, user_service):
    # Instancia todos os controladores exigidos pela especificação arquitetural,
    # vinculando-os ao aplicativo Flask e injetando a camada de serviço.

    UserController(app, user_service)
    ProdutoController(app, user_service)
    PedidoController(app, user_service)