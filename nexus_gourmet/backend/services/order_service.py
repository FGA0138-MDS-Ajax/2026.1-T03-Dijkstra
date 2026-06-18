from models.models import db, Order, ProductOrdered, User, Table
from models.enums import Role, OrderStatus, TableStatus

FLUXO = {
    OrderStatus.PENDENTE:   [OrderStatus.EM_PREPARO, OrderStatus.CANCELADO],
    OrderStatus.EM_PREPARO: [OrderStatus.PRONTO,     OrderStatus.CANCELADO],
    OrderStatus.PRONTO:     [OrderStatus.ENTREGUE],
    OrderStatus.ENTREGUE:   [],
    OrderStatus.CANCELADO:  [],
}

PERMISSOES = {
    OrderStatus.EM_PREPARO: [Role.COZINHEIRO, Role.GARCOM],
    OrderStatus.PRONTO:     [Role.COZINHEIRO],
    OrderStatus.ENTREGUE:   [Role.GARCOM],
    OrderStatus.CANCELADO:  [Role.ADMINISTRADOR, Role.GARCOM],
}

class OrderService:
    def __init__(self, table_service):
        self.table_service = table_service

    def listar_todas_comandas(self):
        comandas = Order.query.all()
        return [
            {
                'id': comanda.id,
                'status': comanda.status.value if comanda.status else None,
                'mesa': {
                    'numero': comanda.table.numero if comanda.table else None,
                    'status': comanda.table.status.value if comanda.table and comanda.table.status else None,
                },
                'itens': [
                    {
                        'id': item.id,
                        'produto': item.product.nome if item.product else None,
                        'quantidade': item.quantidade,
                        'observacao': item.observacao,
                    }
                    for item in comanda.itens
                ],
            }
            for comanda in comandas
        ]
    
    def abrir_comanda(self, numero_mesa, user_id):
        user = db.session.get(User, user_id)
        if not user or user.cargo != Role.GARCOM:
            return None, "Sem permissão para abrir comanda."
            
        mesa = self.table_service.get_table_by_number(numero_mesa)
        if not mesa:
            return None, "Mesa não encontrada."

        if mesa.status == TableStatus.LIVRE:
            mesa.status = TableStatus.OCUPADA
            db.session.commit()        


        nova_comanda = Order(numero_mesa=numero_mesa, user_id=user_id, status=OrderStatus.PENDENTE)
        db.session.add(nova_comanda)
        mesa.status = TableStatus.OCUPADA
        db.session.commit()

        return nova_comanda.id, "Comanda aberta com sucesso."
    
    def visualizar_comanda(self, order_id):
        comanda = self.get_order_by_id(order_id)
        if not comanda:
            return None, "Pedido não encontrado."
        return comanda

    def adicionar_item(self, order_id, product_id, quantidade, observacao, user):
        if user.cargo not in [Role.GARCOM, Role.ADMINISTRADOR]:
            return False, "Sem permissão para adicionar itens."
        pedido = self.get_order_by_id(order_id)
        if not pedido:
            return False, "Pedido não encontrado."
        if pedido.status != OrderStatus.PENDENTE:
            return False, "Só é possível adicionar itens em pedidos com status Pendente."
        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            return False, "Quantidade inválida."
        if quantidade <= 0:
            return False, "Quantidade deve ser maior que zero."

        item = ProductOrdered(
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
        
        pedido = self.get_order_by_id(order_id)
        if not pedido:
            return False, "Pedido não encontrado."
        if pedido.status != OrderStatus.PENDENTE:
            return False, "Só é possível editar itens em pedidos com status Pendente."
        
        for item_data in itens:
            product_id = item_data.get('product_id')

            try: 
                quantidade = int(item_data.get('quantidade', 0))
            except (TypeError, ValueError):
                continue

            if product_id:
                product = ProductOrdered.query.get(product_id)
                
                if not product or product.order_id != order_id:
                    continue
                if quantidade <= 0:
                    db.session.delete(product)
                else:
                    product.quantidade = quantidade
                    if 'observacao' in item_data:
                        product.observacao = item_data['observacao']
                    
            elif product_id and quantidade > 0:
                new_item = ProductOrdered(
                    order_id=order_id,
                    product_id=product_id,
                    quantidade=quantidade,
                    observacao=item_data.get('observacao', '')
                )
                db.session.add(new_item)
        db.session.commit() 
        return True, "Comanda atualizada com sucesso."

    def enviar_comanda(self, order_id, user): 
        pedido = self.get_order_by_id(order_id)
        if not pedido:
            return False, "Pedido não encontrado."
        if not pedido.itens:
            return False, "Não é possível enviar um pedido sem itens."

        sucesso, mensagem = self.alterar_status(order_id, OrderStatus.EM_PREPARO, user)
        if sucesso:
            return True, "Comanda enviada para a cozinha."
        return False, mensagem
    
    def alterar_status(self, order_id, status, user):
        comanda = self.get_order_by_id(order_id)
        if not comanda:
            return False, "Pedido não encontrado."
        try:
            novo_status = OrderStatus(status)
        except ValueError:
            return False, f"Status inválido: {status}."
        status_atual = comanda.status
        if novo_status not in FLUXO.get(status_atual, []):
            return False, f"Transição inválida: {status_atual.value} → {novo_status.value}."
        
        if user.cargo not in PERMISSOES[novo_status]:
            return False, f"Perfil '{user.cargo.value}' não pode definir status '{novo_status.value}'."
        
        if status_atual == OrderStatus.PENDENTE and not comanda.itens:
            return False, "Não é possível enviar um pedido sem itens."

        comanda.status = novo_status
        db.session.commit()
        return True, f"Status atualizado para {novo_status.value}."

    def calcular_total(self, order_id):
        comanda = self.get_order_by_id(order_id)
        if not comanda:
            return None, "Pedido não encontrado."
        total = round(float(sum(i.product.preco * i.quantidade for i in comanda.itens)), 2)
        return total
    
    def gerar_conta(self, mesa_numero):
        mesa = self.table_service.get_table_by_number(mesa_numero)
        if not mesa:
            return None, "Mesa não encontrada."

        comandas_entregues = [
            p for p in mesa.comandas
            if p.status == OrderStatus.ENTREGUE
        ]
        if not comandas_entregues:
            return None, "Nenhuma comanda entregue nesta mesa."

        itens_detalhados = []
        subtotal = 0.0
        for comanda in comandas_entregues:
            for item in comanda.itens:
                valor_item = float(item.product.preco) * item.quantidade
                subtotal += valor_item
                itens_detalhados.append({
                    'produto': item.product.nome,
                    'quantidade': item.quantidade,
                    'preco_unitario': float(item.product.preco),
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
        comanda = self.get_order_by_id(order_id)
        if not comanda:
            return False, "Pedido não encontrado."
        
        if comanda.status not in [OrderStatus.ENTREGUE, OrderStatus.CANCELADO]:
            return False, "Só é possível fechar uma comanda com status Entregue ou Cancelado."

        total = self.calcular_total(order_id)
        if isinstance(total, tuple):
            return False, total[1]

        conta, mensagem_conta = self.gerar_conta(comanda.numero_mesa)
        if conta is None:
            return False, mensagem_conta

        conta['total'] = total

        mesa = self.table_service.get_table_by_number(comanda.numero_mesa)
        
        if mesa:
            comandas_ativas = Order.query.filter(
                Order.numero_mesa == mesa.numero,
                Order.id != order_id, #Ignorar a comanda que está sendo fechanda agora
                Order.status.in_([
                    OrderStatus.PENDENTE, 
                    OrderStatus.EM_PREPARO, 
                    OrderStatus.PRONTO, 
                    OrderStatus.ENTREGUE
                ])
            ).count()
            if comandas_ativas == 0:
                mesa.status = TableStatus.LIVRE
        
        db.session.commit()
        return True, {"mensagem": "Comanda fechada com sucesso.", "conta": conta}
    
    def get_order_by_id(self, order_id):
        return db.session.get(Order, order_id)

    def open_order_counter(self, numero_mesa=None):
        query = Order.query
        if numero_mesa is not None:
            query = query.filter(Order.numero_mesa == numero_mesa)
        return query.count()

    def order_per_table(self):
        mesas = Table.query.all()
        return {mesa.numero: self.open_order_counter(mesa.numero) for mesa in mesas}