from models import db, Table
from enums import TableStatus, OrderStatus
 
 
class MesaService:

    def listar_mesas(self):
        mesas = Table.query.all()
        return [
            {
                'id': mesa.id,
                'numero': mesa.numero,
                'status': mesa.status.value if hasattr(mesa.status, 'value') else mesa.status,
            }
            for mesa in mesas
        ]
 
    def listar_comandas_mesa(self, mesa_id):
        mesa = self.get_by_table_number(mesa_id)
        if not mesa:
            return None, "Mesa não encontrada."
        comandas = []
        for pedido in mesa.pedidos:
            comandas.append({
                'id': pedido.id,
                'status_pedido': pedido.status_pedido.value if hasattr(pedido.status_pedido, 'value') else pedido.status_pedido,
                'itens': [
                    {
                        'produto': item.produto.nome,
                        'quantidade': item.quantidade,
                        'observacao': item.observacao
                    }
                    for item in pedido.itens
                ]
            })
        return comandas, "Comandas listadas com sucesso."
    
    def liberar_mesa(self, mesa_id):
        mesa = self.get_by_table_number(mesa_id)
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

    def get_by_table_number(self, numero):
        return Table.query.filter_by(numero=numero).first()
 