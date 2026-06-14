from enum import Enum

class Role(Enum):
    ADMINISTRADOR = 'Administrador'
    GARCOM = 'Garçom'
    COZINHEIRO = 'Cozinheiro'

class TableStatus(Enum):
    LIVRE = 'Livre'
    OCUPADA = 'Ocupada'
    RESERVADA = 'Reservada'

class ProductCategory(Enum):
    BEBIDA = 'Bebida'
    PRATO = 'Prato'
    SOBREMESA = 'Sobremesa'

class OrderStatus(Enum):
    PENDENTE = 'Pendente'
    EM_PREPARO = 'Em Preparo'
    PRONTO = 'Pronto'
    ENTREGUE = 'Entregue'
    CANCELADO = 'Cancelado'