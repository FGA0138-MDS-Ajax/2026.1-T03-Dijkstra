from models import db, Order, ItemOrdered, Table
from enums import Role, OrderStatus, TableStatus
from services.mesa_service import MesaService


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


class OrderService:

    def listar_todas_comandas(self):
        comandas = Order.query.all()
        return [
            {
                'id': comanda.id,
                'status': comanda.status_pedido.value if comanda.status_pedido else None,
                'mesa': {
                    'id': comanda.mesa.id if comanda.mesa else None,
                    'numero': comanda.mesa.numero if comanda.mesa else None,
                    'status': comanda.mesa.status.value if comanda.mesa and comanda.mesa.status else None,
                },
                'itens': [
                    {
                        'id': item.id,
                        'produto': item.produto.nome if item.produto else None,
                        'quantidade': item.quantidade,
                        'observacao': item.observacao,
                    }
                    for item in comanda.itens
                ],
            }
            for comanda in comandas
        ]

    def abrir_comanda(self, mesa_id):
        mesa = Table.query.get(mesa_id)
        if not mesa:
            return None, "Mesa não encontrada."
        if mesa.status != TableStatus.LIVRE:
            return None, f"Mesa {mesa.numero} não está livre."
        nova_comanda = Order(mesa_id=mesa_id, status_pedido=OrderStatus.PENDENTE)
        db.session.add(nova_comanda)
        mesa.status = TableStatus.OCUPADA
        db.session.commit()
        return nova_comanda.id, "Comanda aberta com sucesso."
    
    def visualizar_comanda(self, order_id):
        comanda = self.get_by_order_id(order_id)
        if not comanda:
            return None, "Pedido não encontrado."
        return comanda

    def adicionar_item(self, order_id, product_id, quantidade, observacao, user):
        if user.cargo not in [Role.GARCOM, Role.ADMINISTRADOR]:
            return False, "Sem permissão para adicionar itens."
        pedido = self.get_by_order_id(order_id)
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
    
    def editar_comanda(self, order_id, itens, user):
        if user.cargo not in [Role.GARCOM, Role.ADMINISTRADOR]:
            return False, "Sem permissão para editar a comanda."
        pedido = self.get_by_order_id(order_id)
        if not pedido:
            return False, "Pedido não encontrado."
        if pedido.status_pedido != OrderStatus.PENDENTE:
            return False, "Só é possível editar itens em pedidos com status Pendente."

        for item_data in itens:
            item_id = item_data.get('id')
            item = ItemOrdered.query.get(item_id)
            if not item or item.order_id != order_id:
                continue  
            try:
                quantidade = int(item_data.get('quantidade', item.quantidade))
            except (TypeError, ValueError):
                continue  
            if quantidade <= 0:
                continue  
            item.quantidade = quantidade
            item.observacao = item_data.get('observacao', item.observacao)

        db.session.commit()
        return True, "Comanda editada com sucesso."
    
    def enviar_comanda(self, order_id):
        pedido = self.get_by_order_id(order_id)
        if not pedido:
            return False, "Pedido não encontrado."
        if pedido.status_pedido != OrderStatus.PENDENTE:
            return False
        if not pedido.itens:
            return False, "Não é possível enviar um pedido sem itens."

        pedido.status_pedido = OrderStatus.EM_PREPARO
        db.session.commit()
        return True, "Comanda enviada para a cozinha."
    
    def alterar_status(self, order_id, status, user):
        comanda = self.get_by_order_id(order_id)
        if not comanda:
            return False, "Pedido não encontrado."
        try:
            novo_status = OrderStatus(status)
        except ValueError:
            return False, f"Status inválido: {status}."
        status_atual = comanda.status_pedido
        if novo_status not in FLUXO.get(status_atual, []):
            return False, f"Transição inválida: {status_atual.value} → {novo_status.value}."
        if user.cargo not in PERMISSOES[novo_status]:
            return False, f"Perfil '{user.cargo.value}' não pode definir status '{novo_status.value}'."
        if status_atual == OrderStatus.PENDENTE and not comanda.itens:
            return False, "Não é possível enviar um pedido sem itens."

        comanda.status_pedido = novo_status
        db.session.commit()
        return True, f"Status atualizado para {novo_status.value}."

    def calcular_total(self, order_id):
        comanda = self.get_by_order_id(order_id)
        if not comanda:
            return None, "Pedido não encontrado."
        total = round(float(sum(i.produto.preco * i.quantidade for i in comanda.itens)), 2)
        return total
    
    def gerar_conta(self, mesa_id):
        mesa = self.get_by_table_number(mesa_id)
        if not mesa:
            return None, "Mesa não encontrada."

        pedidos_entregues = [
            p for p in mesa.pedidos
            if p.status_pedido == OrderStatus.ENTREGUE
        ]
        if not pedidos_entregues:
            return None, "Nenhum pedido entregue nesta mesa."

        itens_detalhados = []
        subtotal = 0.0
        for pedido in pedidos_entregues:
            for item in pedido.itens:
                valor_item = float(item.produto.preco) * item.quantidade
                subtotal += valor_item
                itens_detalhados.append({
                    'produto': item.produto.nome,
                    'quantidade': item.quantidade,
                    'preco_unitario': float(item.produto.preco),
                    'subtotal_item': round(valor_item, 2),
                    'observacao': item.observacao or ''
                })

        conta = {
            'mesa': mesa.numero,
            'itens': itens_detalhados,
            'total': round(subtotal, 2)
        }
        return conta, "Conta gerada."
    
    def fechar_comanda(self, order_id):
        comanda = self.get_by_order_id(order_id)
        if not comanda:
            return False, "Pedido não encontrado."
        if comanda.status_pedido != OrderStatus.ENTREGUE:
            return False, "Só é possível fechar uma comanda com status Entregue."

        total = self.calcular_total(order_id)
        if isinstance(total, tuple):
            return False, total[1]

        conta, mensagem_conta = self.gerar_conta(comanda.mesa_id)
        if conta is None:
            return False, mensagem_conta

        conta['total'] = total

        mesa = Table.query.get(comanda.mesa_id)
        if mesa:
            mesa.status = TableStatus.LIVRE
        db.session.commit()
        return True, {"mensagem": "Comanda fechada e mesa liberada.", "conta": conta}
    
    def get_by_order_id(self, order_id):
        return Order.query.get(order_id)
    
    def open_order_counter(self):
        return Order.query.count()

    def order_per_table(self):
        mesas = MesaService().listar_mesas()
        return {mesa['numero']: len(mesa['pedidos']) for mesa in mesas}