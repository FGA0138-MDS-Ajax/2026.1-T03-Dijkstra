# enums.py
from enum import Enum

class PerfilUsuario(Enum):
    ADMINISTRADOR = 'Administrador'
    GARCOM = 'Garçom'
    COZINHEIRO = 'Cozinheiro'

class StatusMesa(Enum):
    LIVRE = 'Livre'
    OCUPADA = 'Ocupada'
    RESERVADA = 'Reservada'

class CategoriaProduto(Enum):
    BEBIDA = 'Bebida'
    PRATO = 'Prato'
    SOBREMESA = 'Sobremesa'

class StatusPedido(Enum):
    PENDENTE = 'Pendente'
    EM_PREPARO = 'Em Preparo'
    PRONTO = 'Pronto'
    ENTREGUE = 'Entregue'
    CANCELADO = 'Cancelado'