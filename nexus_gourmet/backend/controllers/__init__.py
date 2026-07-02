from .user_controller import UserController
from .order_controller import OrderController
from .product_controller import ProductController
from .table_controller import TableController

def init_controllers(app, user_service, order_service, table_service, product_service):
    # Instancia todos os controladores exigidos pela especificação arquitetural,
    # vinculando-os ao aplicativo Flask e injetando a camada de serviço.

    UserController(app, user_service, order_service)
    ProductController(app, user_service, product_service)
    OrderController(app, user_service, order_service, table_service)
    TableController(app, user_service, table_service)
