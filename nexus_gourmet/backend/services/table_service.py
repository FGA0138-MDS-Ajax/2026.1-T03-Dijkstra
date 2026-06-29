from models.models import db, Table
from models.enums import Role, TableStatus, OrderStatus
from models.sucess_message import TableSuccessMessages
from models.error_message import UserErrorMessages, TableErrorMessages
from services.user_service import UserService 

class TableService:
    def criar_mesa(self, cpf_usuario_logado, capacidade):
        usuario_logado = UserService().get_user_by_cpf(cpf_usuario_logado)
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return False, UserErrorMessages.ACESSO_NEGADO

        novo_numero = 1
        while self.get_table_by_number(novo_numero) is not None:
            novo_numero += 1
        
        try:
            capacidade = int(capacidade)
        except (TypeError, ValueError):
            return False, TableErrorMessages.CAPACIDADE_INVALIDA
        
        if capacidade < 1:
            return False, TableErrorMessages.CAPACIDADE_INVALIDA
        
        if capacidade > 20:
            return False, TableErrorMessages.CAPACIDADE_EXCEDIDA

        nova_mesa = Table(numero=novo_numero, status=TableStatus.LIVRE, capacidade=capacidade)
        db.session.add(nova_mesa)
        db.session.commit()
        return True, TableSuccessMessages.MESA_CRIADA

    def editar_mesa(self, cpf_usuario_logado, numero_mesa, capacidade=None):
        usuario_logado = UserService().get_user_by_cpf(cpf_usuario_logado)
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return False, UserErrorMessages.ACESSO_NEGADO

        mesa = self.get_table_by_number(numero_mesa)
        if not mesa:
            return False, TableErrorMessages.MESA_NAO_ENCONTRADA
        
        if capacidade is not None:
            try:
                capacidade = int(capacidade)
            except (TypeError, ValueError):
                return False, TableErrorMessages.CAPACIDADE_INVALIDA
            
            if capacidade < 1:
                return False, TableErrorMessages.CAPACIDADE_INVALIDA
            
            if capacidade > 20:
                return False, TableErrorMessages.CAPACIDADE_EXCEDIDA
            mesa.capacidade = capacidade

        try:
            db.session.commit()
            return True, TableSuccessMessages.MESA_EDITADA
        except Exception as e:
            db.session.rollback()        
            return False, TableErrorMessages.ERRO_ATUALIZAR_MESA

    def deletar_mesa(self, cpf_usuario_logado, numero_mesa):
        usuario_logado = UserService().get_user_by_cpf(cpf_usuario_logado)
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return False, UserErrorMessages.ACESSO_NEGADO

        mesa = self.get_table_by_number(numero_mesa)
        if not mesa:
            return False, TableErrorMessages.MESA_NAO_ENCONTRADA
        
        if mesa.comandas:
            return False, TableErrorMessages.MESA_COM_COMANDAS
        
        db.session.delete(mesa)
        db.session.commit()
        return True, TableSuccessMessages.MESA_DELETADA

    def listar_mesas(self):
        mesas = Table.query.all()
        return [
            {
                'numero': mesa.numero,
                'status': mesa.status.value if hasattr(mesa.status, 'value') else mesa.status,
                'capacidade': mesa.capacidade
            }
            for mesa in mesas
        ]
    
    def listar_comandas_mesa(self, mesa_numero):
        mesa = self.get_table_by_number(mesa_numero)
        if not mesa:
            return False, TableErrorMessages.MESA_NAO_ENCONTRADA
        
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
        return comandas, None

    def liberar_mesa(self, mesa_numero):
        mesa = self.get_table_by_number(mesa_numero)
        if not mesa:
            return False, TableErrorMessages.MESA_NAO_ENCONTRADA
        
        comandas_em_aberto = [
            p for p in mesa.comandas
            if p.status not in (OrderStatus.FINALIZADO, OrderStatus.CANCELADO)
        ]

        if comandas_em_aberto:
            return False, f"Mesa {mesa.numero} ainda tem comandas em aberto."
                
        mesa.status = TableStatus.LIVRE
        db.session.commit()
        return True, TableSuccessMessages.MESA_LIBERADA

    def get_table_by_number(self, numero):
        return Table.query.filter_by(numero=numero).first()