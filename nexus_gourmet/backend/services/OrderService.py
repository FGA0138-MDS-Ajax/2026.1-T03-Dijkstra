from enums import PerfilUsuario, StatusPedido
import MesaService


FLUXO = {
    StatusPedido.PENDENTE:   [StatusPedido.EM_PREPARO, StatusPedido.CANCELADO],
    StatusPedido.EM_PREPARO: [StatusPedido.PRONTO,     StatusPedido.CANCELADO],
    StatusPedido.PRONTO:     [StatusPedido.ENTREGUE],
    StatusPedido.ENTREGUE:   [],
    StatusPedido.CANCELADO:  [],
}

PERMISSOES = {
    StatusPedido.EM_PREPARO: [PerfilUsuario.COZINHEIRO],
    StatusPedido.PRONTO:     [PerfilUsuario.COZINHEIRO],
    StatusPedido.ENTREGUE:   [PerfilUsuario.GARCOM],
    StatusPedido.CANCELADO:  [PerfilUsuario.ADMINISTRADOR, PerfilUsuario.GARCOM],
}


def criar_pedido(pedido, mesa, garcom):
    if garcom.perfil not in [PerfilUsuario.GARCOM, PerfilUsuario.ADMINISTRADOR]:
        return None, "Sem permissão."
    sucesso, msg = MesaService.ocupar(mesa)
    if not sucesso:
        return None, msg
    return pedido, "Pedido aberto."

def adicionar_item(pedido, item, garcom):
    if garcom.perfil not in [PerfilUsuario.GARCOM, PerfilUsuario.ADMINISTRADOR]:
        return None, "Sem permissão."
    if pedido.status_pedido != StatusPedido.PENDENTE:
        return None, "Pedido já enviado à cozinha."
    return item, "Item adicionado."

def atualizar_status(pedido, novo_status, usuario):
    if novo_status not in FLUXO[pedido.status_pedido]:
        return False, "Transição de status inválida."
    if usuario.perfil not in PERMISSOES[novo_status]:
        return False, "Sem permissão para este status."
    pedido.status_pedido = novo_status
    if novo_status in [StatusPedido.ENTREGUE, StatusPedido.CANCELADO]:
        MesaService.liberar(pedido.mesa)
    return True, f"Status: {novo_status.value}."

def get_fila_cozinha(todos_pedidos):
    return [p for p in todos_pedidos
            if p.status_pedido in (StatusPedido.PENDENTE, StatusPedido.EM_PREPARO)]

def calcular_total(pedido):
    return float(sum(i.produto.preco * i.quantidade for i in pedido.itens))