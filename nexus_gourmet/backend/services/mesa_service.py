from models import db, Table
from enums import TableStatus, OrderStatus
 
 
class MesaService:
 
    def get_mesa_by_id(self, mesa_id):
        return Table.query.get(mesa_id)
 
    def get_mesa_by_numero(self, numero):
        return Table.query.filter_by(numero=numero).first()
 
    def listar_mesas(self):
        return Table.query.all()
 
    def listar_mesas_livres(self):
        return Table.query.filter_by(status=TableStatus.LIVRE).all()
 
    def liberar_mesa(self, mesa_id):
        mesa = self.get_mesa_by_id(mesa_id)
        if not mesa:
            return False, "Mesa não encontrada."
        pedidos_em_aberto = [
            p for p in mesa.pedidos
            if p.status_pedido not in (OrderStatus.ENTREGUE, OrderStatus.CANCELADO)
        ]
        if pedidos_em_aberto:
            return False, f"Mesa {mesa.numero} ainda tem pedidos em aberto."
        mesa.status = TableStatus.LIVRE
        db.session.commit()
        return True, f"Mesa {mesa.numero} liberada."
 
    def gerar_conta(self, mesa_id):
        mesa = self.get_mesa_by_id(mesa_id)
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
