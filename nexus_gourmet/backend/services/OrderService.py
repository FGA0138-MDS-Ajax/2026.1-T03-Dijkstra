from models import db, Pedido, ItemPedido, Mesa
from enums import PerfilUsuario, StatusPedido, StatusMesa
 
 
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
 
 
class PedidoService:
 
    def get_pedido_by_id(self, pedido_id):
        return Pedido.query.get(pedido_id)
 
    def listar_pedidos(self):
        return Pedido.query.all()
 
    def get_fila_cozinha(self):
        return (Pedido.query
                .filter(Pedido.status_pedido.in_([StatusPedido.PENDENTE, StatusPedido.EM_PREPARO]))
                .order_by(Pedido.data_hora_abertura)
                .all())
 
    def criar_comanda(self, mesa_id, garcom):
        if garcom.perfil not in [PerfilUsuario.GARCOM, PerfilUsuario.ADMINISTRADOR]:
            return False, "Sem permissão para abrir comanda."
        mesa = Mesa.query.get(mesa_id)
        if not mesa:
            return False, "Mesa não encontrada."
        if mesa.status != StatusMesa.LIVRE:
            return False, f"Mesa {mesa.numero} não está livre."
 
        mesa.status = StatusMesa.OCUPADA
        pedido = Pedido(mesa_id=mesa.id, usuario_id=garcom.id)
        db.session.add(pedido)
        db.session.commit()
        return True, "Comanda aberta."
 
    def adicionar_item(self, pedido_id, produto_id, quantidade, observacao, garcom):
        if garcom.perfil not in [PerfilUsuario.GARCOM, PerfilUsuario.ADMINISTRADOR]:
            return False, "Sem permissão para adicionar itens."
        pedido = self.get_pedido_by_id(pedido_id)
        if not pedido:
            return False, "Pedido não encontrado."
        if pedido.status_pedido != StatusPedido.PENDENTE:
            return False, "Só é possível adicionar itens em pedidos com status Pendente."
        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            return False, "Quantidade inválida."
        if quantidade <= 0:
            return False, "Quantidade deve ser maior que zero."
 
        item = ItemPedido(
            pedido_id=pedido_id,
            produto_id=produto_id,
            quantidade=quantidade,
            observacao=observacao
        )
        db.session.add(item)
        db.session.commit()
        return True, "Item adicionado."
 
    def remover_item(self, pedido_id, item_id, garcom):
        if garcom.perfil not in [PerfilUsuario.GARCOM, PerfilUsuario.ADMINISTRADOR]:
            return False, "Sem permissão para remover itens."
        pedido = self.get_pedido_by_id(pedido_id)
        if not pedido or pedido.status_pedido != StatusPedido.PENDENTE:
            return False, "Não é possível remover itens de um pedido já enviado."
        item = ItemPedido.query.get(item_id)
        if not item or item.pedido_id != pedido_id:
            return False, "Item não encontrado neste pedido."
 
        db.session.delete(item)
        db.session.commit()
        return True, "Item removido."
 
    def atualizar_status(self, pedido_id, novo_status_str, usuario):
        pedido = self.get_pedido_by_id(pedido_id)
        if not pedido:
            return False, "Pedido não encontrado."
        try:
            novo_status = StatusPedido(novo_status_str)
        except ValueError:
            return False, f"Status inválido: {novo_status_str}."
        if novo_status not in FLUXO[pedido.status_pedido]:
            return False, f"Transição inválida: {pedido.status_pedido.value} → {novo_status.value}."
        if usuario.perfil not in PERMISSOES[novo_status]:
            return False, f"Perfil '{usuario.perfil.value}' não pode definir status '{novo_status.value}'."
        if pedido.status_pedido == StatusPedido.PENDENTE and not pedido.itens:
            return False, "Não é possível enviar um pedido sem itens."
 
        pedido.status_pedido = novo_status
        db.session.commit()
        return True, f"Status atualizado para {novo_status.value}."
 
    def calcular_total(self, pedido_id):
        pedido = self.get_pedido_by_id(pedido_id)
        if not pedido:
            return None, "Pedido não encontrado."
        total = round(float(sum(i.produto.preco * i.quantidade for i in pedido.itens)), 2)
        return total, "Total calculado."
