from models.models import db, Table
from models.enums import TableStatus, OrderStatus
 
class TableService:
    def criar_mesa(self, numero, capacidade):
        if self.get_table_by_number(numero):
            return False, "Número de mesa já existe."
        nova_mesa = Table(numero=numero, status=TableStatus.LIVRE, capacidade=capacidade)
        db.session.add(nova_mesa)
        db.session.commit()
        return True, "Mesa criada com sucesso."
    
    def editar_mesa(self, numero_mesa, numero=None, capacidade=None):
        mesa = self.get_table_by_number(numero_mesa)
        if not mesa:
            return False, "Mesa não encontrada."
        if numero:
            if self.get_table_by_number(numero):
                return False, "Número de mesa já existe."
            mesa.numero = numero
        if capacidade is not None:
            mesa.capacidade = capacidade
        db.session.commit()
        return True, "Mesa editada com sucesso."
    
    def deletar_mesa(self, numero_mesa):
        mesa = self.get_table_by_number(numero_mesa)
        if not mesa:
            return False, "Mesa não encontrada."
        if mesa.comandas:
            return False, "Não é possível deletar uma mesa com comandas associadas."
        db.session.delete(mesa)
        db.session.commit()
        return True, "Mesa deletada com sucesso."
    
    def listar_mesas(self):
        mesas = Table.query.all()
        return [
            {
                'numero': mesa.numero,
                'status': mesa.status.value if hasattr(mesa.status, 'value') else mesa.status,
                'capacidade': f"{len(mesa.comandas)}/{mesa.capacidade}",
            }
            for mesa in mesas
        ]
    
    def listar_comandas_mesa(self, mesa_numero):
        mesa = self.get_table_by_number(mesa_numero)
        if not mesa:
            return None, "Mesa não encontrada."
        comandas = []
        for comanda in mesa.comandas:
            comandas.append({
                'id': comanda.id,
                'status': comanda.status.value if hasattr(comanda.status, 'value') else comanda.status,
                'itens': [
                    {
                        'produto': item.product.nome,
                        'quantidade': item.quantidade,
                        'observacao': item.observacao
                    }
                    for item in comanda.itens
                ]
            })
        return comandas, "Comandas listadas com sucesso."
    
    def liberar_mesa(self, mesa_numero):
        mesa = self.get_table_by_number(mesa_numero)
        if not mesa:
            return False, "Mesa não encontrada."
        comandas_em_aberto = [
            p for p in mesa.comandas
            if p.status not in (OrderStatus.ENTREGUE, OrderStatus.CANCELADO)
        ]
        if comandas_em_aberto:
            return False, f"Mesa {mesa.numero} ainda tem comandas em aberto."
        mesa.status = TableStatus.LIVRE
        db.session.commit()
        return True, f"Mesa {mesa.numero} liberada."

    def get_table_by_number(self, numero):
        return db.session.get(Table, numero)
