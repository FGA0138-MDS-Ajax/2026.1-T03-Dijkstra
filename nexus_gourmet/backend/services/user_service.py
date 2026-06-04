from models import db, Usuario, Mesa, Produto, Pedido, ItemPedido
from enums import PerfilUsuario, StatusMesa, StatusPedido
from werkzeug.security import generate_password_hash, check_password_hash

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

def autenticar(login, senha):
    u = Usuario.query.filter_by(login=login).first()
    if u and check_password_hash(u.senha, senha):
        return u
    return None

def criar_usuario(nome, login, senha, perfil=PerfilUsuario.GARCOM):
    if Usuario.query.filter_by(login=login).first():
        return None, "Login já em uso."
    u = Usuario(nome=nome, login=login, senha=generate_password_hash(senha), perfil=perfil)
    db.session.add(u)
    db.session.commit()
    return u, "Usuário criado."

def criar_pedido(mesa_id, garcom):
    if garcom.perfil not in [PerfilUsuario.GARCOM, PerfilUsuario.ADMINISTRADOR]:
        return None, "Sem permissão."
    mesa = Mesa.query.get(mesa_id)
    if not mesa or mesa.status != StatusMesa.LIVRE:
        return None, "Mesa indisponível."

    mesa.status = StatusMesa.OCUPADA
    pedido = Pedido(mesa_id=mesa_id, usuario_id=garcom.id)
    db.session.add(pedido)
    db.session.commit()
    return pedido, "Pedido aberto."

def adicionar_item(pedido_id, produto_id, quantidade, observacao, garcom):
    pedido = Pedido.query.get(pedido_id)
    if not pedido or pedido.status_pedido != StatusPedido.PENDENTE:
        return None, "Pedido inválido ou já enviado."
    if garcom.perfil not in [PerfilUsuario.GARCOM, PerfilUsuario.ADMINISTRADOR]:
        return None, "Sem permissão."

    item = ItemPedido(pedido_id=pedido_id, produto_id=produto_id,
                      quantidade=quantidade, observacao=observacao)
    db.session.add(item)
    db.session.commit()
    return item, "Item adicionado."

def atualizar_status(pedido_id, novo_status, usuario):
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        return False, "Pedido não encontrado."
    if novo_status not in FLUXO[pedido.status_pedido]:
        return False, "Transição de status inválida."
    if usuario.perfil not in PERMISSOES[novo_status]:
        return False, "Sem permissão para este status."

    pedido.status_pedido = novo_status
    if novo_status in [StatusPedido.ENTREGUE, StatusPedido.CANCELADO]:
        pedido.mesa.status = StatusMesa.LIVRE

    db.session.commit()
    return True, f"Status: {novo_status.value}."

def get_fila_cozinha():
    return (Pedido.query
            .filter(Pedido.status_pedido.in_([StatusPedido.PENDENTE, StatusPedido.EM_PREPARO]))
            .order_by(Pedido.data_hora_abertura)
            .all())

def calcular_total(pedido_id):
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        return None
    return float(sum(i.produto.preco * i.quantidade for i in pedido.itens))