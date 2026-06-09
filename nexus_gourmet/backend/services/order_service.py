from models import db, Order, ItemOrdered, Table
from enums import Role, OrderStatus, TableStatus


FLUXO = {
    OrderStatus.PENDENTE:   [OrderStatus.EM_PREPARO, OrderStatus.CANCELADO],
    OrderStatus.EM_PREPARO: [OrderStatus.PRONTO,     OrderStatus.CANCELADO],
    OrderStatus.PRONTO:     [OrderStatus.ENTREGUE],
    OrderStatus.ENTREGUE:   [],
    OrderStatus.CANCELADO:  [],
}

PERMISSOES = {
    OrderStatus.EM_PREPARO: [Role.COZINHEIRO],
    OrderStatus.PRONTO:     [Role.COZINHEIRO],
    OrderStatus.ENTREGUE:   [Role.GARCOM],
    OrderStatus.CANCELADO:  [Role.ADMINISTRADOR, Role.GARCOM],
}


class PedidoService:

    def get_pedido_by_id(self, order_id):
        return Order.query.get(order_id)

    def listar_pedidos(self):
        return Order.query.all()

    def get_fila_cozinha(self):
        return (Order.query
                .filter(Order.status_pedido.in_([OrderStatus.PENDENTE, OrderStatus.EM_PREPARO]))
                .order_by(Order.data_hora_abertura)
                .all())

    def criar_comanda(self, mesa_id, user):
        if user.cargo not in [Role.GARCOM, Role.ADMINISTRADOR]:
            return False, "Sem permissão para abrir comanda."
        mesa = Table.query.get(mesa_id)
        if not mesa:
            return False, "Mesa não encontrada."
        if mesa.status != TableStatus.LIVRE:
            return False, f"Mesa {mesa.numero} não está livre."

        mesa.status = TableStatus.OCUPADA
        comanda = Order(mesa_id=mesa.id, user_id=user.id)
        db.session.add(comanda)
        db.session.commit()
        return True, "Comanda aberta."

    def adicionar_item(self, order_id, product_id, quantidade, observacao, user):
        if user.cargo not in [Role.GARCOM, Role.ADMINISTRADOR]:
            return False, "Sem permissão para adicionar itens."
        pedido = self.get_pedido_by_id(order_id)
        if not pedido:
            return False, "Pedido não encontrado."
        if pedido.status_pedido != OrderStatus.PENDENTE:
            return False, "Só é possível adicionar itens em pedidos com status Pendente."
        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            return False, "Quantidade inválida."
        if quantidade <= 0:
            return False, "Quantidade deve ser maior que zero."

        item = ItemOrdered(
            order_id=order_id,
            product_id=product_id,
            quantidade=quantidade,
            observacao=observacao
        )
        db.session.add(item)
        db.session.commit()
        return True, "Item adicionado."

    def remover_item(self, order_id, product_id, user):
        if user.cargo not in [Role.GARCOM, Role.ADMINISTRADOR]:
            return False, "Sem permissão para remover itens."
        pedido = self.get_pedido_by_id(order_id)
        if not pedido or pedido.status_pedido != OrderStatus.PENDENTE:
            return False, "Não é possível remover itens de um pedido já enviado."
        item = ItemOrdered.query.get(product_id)
        if not item or item.order_id != order_id:
            return False, "Item não encontrado neste pedido."

        db.session.delete(item)
        db.session.commit()
        return True, "Item removido."

    def atualizar_status(self, order_id, status, user):
        comanda = self.get_pedido_by_id(order_id)
        if not comanda:
            return False, "Pedido não encontrado."
        try:
            novo_status = OrderStatus(status)
        except ValueError:
            return False, f"Status inválido: {status}."
        if novo_status not in FLUXO[comanda.status_comanda]:
            return False, f"Transição inválida: {comanda.status.value} → {novo_status.value}."
        if user.cargo not in PERMISSOES[novo_status]:
            return False, f"Perfil '{user.cargo.value}' não pode definir status '{novo_status.value}'."
        if comanda.status == OrderStatus.PENDENTE and not comanda.itens:
            return False, "Não é possível enviar um pedido sem itens."

        comanda.status_comanda = novo_status
        db.session.commit()
        return True, f"Status atualizado para {novo_status.value}."

    def calcular_total(self, order_id):
        comanda = self.get_pedido_by_id(order_id)
        if not comanda:
            return None, "Pedido não encontrado."
        total = round(float(sum(i.produto.preco * i.quantidade for i in comanda.itens)), 2)
        return total, "Total calculado."