from datetime import datetime, time, timezone
from backend.models.models import db, Order, ProductOrdered, User, Table, Product
from backend.models.enums import Role, OrderStatus, TableStatus
from backend.models.error_message import UserErrorMessages, OrderErrorMessages, TableErrorMessages
from backend.models.sucess_message import OrderSuccessMessages

# backend/services/order_service.py

#FLUXO = {
#    OrderStatus.PENDENTE:   [OrderStatus.EM_PREPARO, OrderStatus.CANCELADO],
#    # Permite voltar de PREPARO para PENDENTE, e adicionar novos itens (EM_PREPARO):
#    OrderStatus.EM_PREPARO: [OrderStatus.PRONTO, OrderStatus.PENDENTE, OrderStatus.CANCELADO, OrderStatus.EM_PREPARO], 
#    # Permite voltar de PRONTO para PREPARO:
#    OrderStatus.PRONTO:     [OrderStatus.ENTREGUE, OrderStatus.EM_PREPARO],
#    # Permite voltar de ENTREGUE para PRONTO:
#    OrderStatus.ENTREGUE:   [OrderStatus.PRONTO],
#    # Status finais onde o fluxo morre (não tem volta):
#    OrderStatus.FINALIZADO: [], 
#    OrderStatus.CANCELADO:  [],
#}
FLUXO = {
    OrderStatus.PENDENTE:   [OrderStatus.EM_PREPARO, OrderStatus.CANCELADO],
    # Adicionado OrderStatus.EM_PREPARO para permitir reenvios:
    OrderStatus.EM_PREPARO: [OrderStatus.PRONTO, OrderStatus.PENDENTE, OrderStatus.CANCELADO, OrderStatus.EM_PREPARO], 
    OrderStatus.PRONTO:     [OrderStatus.ENTREGUE, OrderStatus.EM_PREPARO],
    # Adicionado OrderStatus.EM_PREPARO para novos pedidos após entregas:
    OrderStatus.ENTREGUE:   [OrderStatus.PRONTO, OrderStatus.EM_PREPARO],
    OrderStatus.FINALIZADO: [], 
    OrderStatus.CANCELADO:  [],
}



PERMISSOES = {
    OrderStatus.PENDENTE:   [Role.GARCOM, Role.ADMINISTRADOR, Role.COZINHEIRO],
    # Adicionado COZINHEIRO (para reverter de PRONTO para PREPARO):
    OrderStatus.EM_PREPARO: [Role.GARCOM, Role.ADMINISTRADOR, Role.COZINHEIRO], 
    # Adicionado GARCOM (para reverter de ENTREGUE para PRONTO):
    OrderStatus.PRONTO:     [Role.COZINHEIRO, Role.ADMINISTRADOR, Role.GARCOM],
    OrderStatus.ENTREGUE:   [Role.GARCOM, Role.ADMINISTRADOR], 
    OrderStatus.FINALIZADO: [Role.GARCOM, Role.ADMINISTRADOR],
    OrderStatus.CANCELADO:  [Role.ADMINISTRADOR, Role.GARCOM],
}

class OrderService:
    def __init__(self, table_service):
        self.table_service = table_service

    def listar_todas_comandas(self):
        comandas = Order.query.all()
        return [self._formatar_comanda(comanda) for comanda in comandas]

    def listar_comandas_por_status(self, status_alvo):
        if isinstance(status_alvo, OrderStatus):
            status_alvo = [status_alvo]
            
        comandas = Order.query.filter(Order.status.in_(status_alvo)).all()
        return [self._formatar_comanda(comanda) for comanda in comandas]

    def _formatar_comanda(self, comanda):
        return {
            'id': comanda.id,
            'status': comanda.status.value if comanda.status else None,
            'tempo_decorrido': self.tempo_decorrido(comanda),
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
                    'cozinha_status': item.cozinha_status,
                    'preparation_time_minutes': item.product.tempo_preparacao if item.product else 15,
                }
                for item in comanda.itens
            ],
        }
    
    def abrir_comanda(self, numero_mesa, user_cpf):
        # CORREÇÃO: Busca apenas as comandas abertas HOJE para que o número reinicie amanhã
        hoje = datetime.now(timezone.utc).replace(tzinfo=None).date()
        inicio_do_dia = datetime.combine(hoje, time.min)
        
        ultima_comanda_hoje = Order.query.filter(
            Order.data_criacao >= inicio_do_dia
        ).order_by(Order.id.desc()).first()

        proximo_numero = (ultima_comanda_hoje.numero_diario + 1) if ultima_comanda_hoje else 1

        user = db.session.get(User, user_cpf)
        if not user or user.cargo not in [Role.GARCOM, Role.ADMINISTRADOR]:
            return None, OrderErrorMessages.SEM_PERMISSAO
            
        mesa = self.table_service.get_table_by_number(numero_mesa)
        if not mesa:
            return None, TableErrorMessages.MESA_NAO_ENCONTRADA
        
        nova_comanda = Order(
            numero_diario=proximo_numero, 
            numero_mesa=numero_mesa, 
            user_cpf=user_cpf, 
            status=OrderStatus.PENDENTE,
            entrada_cozinha=None 
        )
        db.session.add(nova_comanda)
        mesa.status = TableStatus.OCUPADA
        db.session.commit()
        
        return nova_comanda.id, OrderSuccessMessages.COMANDA_ABERTA

    def visualizar_comanda(self, order_id):
        comanda = self.get_order_by_id(order_id)
        if not comanda:
            return None, OrderErrorMessages.COMANDA_NAO_ENCONTRADA
        return comanda

    def adicionar_item(self, order_id, product_id, quantidade, observacao, user):
        if user.cargo != Role.GARCOM:
            return False, OrderErrorMessages.SEM_PERMISSAO
        pedido = self.get_order_by_id(order_id)
        if not pedido:
            return False, OrderErrorMessages.COMANDA_NAO_ENCONTRADA
        if pedido.status == OrderStatus.CANCELADO:
            return False, OrderErrorMessages.COMANDA_JA_CANCELADA
        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            return False, OrderErrorMessages.QUANTIDADE_INVALIDA
        if quantidade <= 0:
            return False, OrderErrorMessages.QUANTIDADE_MINIMA
        
        produto = db.session.get(Product, product_id)
        if not produto:
            return False, "Produto não encontrado."
        
        item = ProductOrdered(
            order_id=order_id,
            product_id=product_id,
            quantidade=quantidade,
            observacao=observacao,
            preco_vendido=float(produto.preco) 
        )
        db.session.add(item)
        db.session.commit()
        return True, OrderSuccessMessages.ITEM_ADICIONADO
    
    def editar_comanda(self, order_id, itens, user, cancelar=False):
        if user.cargo != Role.GARCOM:
            return False, OrderErrorMessages.SEM_PERMISSAO
        
        pedido = self.get_order_by_id(order_id)
        if not pedido:
            return False, OrderErrorMessages.COMANDA_NAO_ENCONTRADA
        
        if cancelar:
            if pedido.status not in [OrderStatus.PENDENTE, OrderStatus.EM_PREPARO]:
                return False, OrderErrorMessages.COMANDA_NAO_PODE_SER_CANCELADA
            pedido.status = OrderStatus.CANCELADO
            db.session.commit()
            return True, OrderSuccessMessages.COMANDA_CANCELADA

        if pedido.status == OrderStatus.CANCELADO:
            return False, OrderErrorMessages.COMANDA_JA_CANCELADA
        
        for item_data in itens:
            item_id = item_data.get('id')
            product_id = item_data.get('product_id')
            
            try: 
                quantidade = int(item_data.get('quantidade', 0))
            except (TypeError, ValueError):
                continue

            if item_id:
                if pedido.status != OrderStatus.PENDENTE:
                    continue 
                    
                item_existente = db.session.get(ProductOrdered, item_id)
                if not item_existente or item_existente.order_id != order_id:
                    continue
                    
                if quantidade <= 0:
                    db.session.delete(item_existente)
                else:
                    item_existente.quantidade = quantidade
                    if 'observacao' in item_data:
                        item_existente.observacao = item_data['observacao']
                        
            elif product_id and quantidade > 0:
                new_item = ProductOrdered(
                    order_id=order_id,
                    product_id=product_id,
                    quantidade=quantidade,
                    observacao=item_data.get('observacao', ''),
                )
                db.session.add(new_item)
                
        db.session.commit() 
        return True, OrderSuccessMessages.COMANDA_EDITADA

    def enviar_comanda(self, order_id, user): 
        if user.cargo != Role.GARCOM:
            return False, OrderErrorMessages.SEM_PERMISSAO
        pedido = self.get_order_by_id(order_id)
        if not pedido:
            return False, OrderErrorMessages.COMANDA_NAO_ENCONTRADA
        if not pedido.itens:
            return False, OrderErrorMessages.COMANDA_SEM_ITENS
        
        # CORREÇÃO AQUI: Enviamos .value para evitar conflito de tipo ValueError no Python
        sucesso, mensagem = self.alterar_status(order_id, OrderStatus.EM_PREPARO.value, user)
        if sucesso:
            return True, OrderSuccessMessages.COMANDA_ENVIADA
        
        return False, mensagem
    
    def alterar_status(self, order_id, status, user):
        comanda = self.get_order_by_id(order_id)
        if not comanda:
            return False, OrderErrorMessages.COMANDA_NAO_ENCONTRADA
            
        try:
            if isinstance(status, OrderStatus):
                novo_status = status
            else:
                novo_status = OrderStatus(status)
        except ValueError:
            return False, f"Status inválido: {status}."
            
        status_atual = comanda.status
        # CORREÇÃO VITAL: O SQLite às vezes retorna uma string, vamos forçar de volta para Enum
        if isinstance(status_atual, str):
            try:
                status_atual = OrderStatus(status_atual)
            except ValueError:
                pass
                
        if novo_status not in FLUXO.get(status_atual, []):
            valor_atual = status_atual.value if hasattr(status_atual, 'value') else status_atual
            return False, f"Transição inválida: {valor_atual} → {novo_status.value}."
            
        if user.cargo not in PERMISSOES[novo_status]:
            return False, f"Perfil '{user.cargo.value}' não pode definir status '{novo_status.value}'."
            
        if status_atual == OrderStatus.PENDENTE and not comanda.itens:
            return False, OrderErrorMessages.COMANDA_SEM_ITENS

        agora = datetime.now(timezone.utc).replace(tzinfo=None)
        
        if novo_status == OrderStatus.EM_PREPARO:
            if not comanda.entrada_cozinha:
                comanda.entrada_cozinha = agora
            for item in comanda.itens:
                if item.cozinha_status == 'PENDENTE':
                    item.cozinha_status = 'PREPARANDO'

        if novo_status == OrderStatus.PRONTO:
            comanda.saida_cozinha = agora
            for item in comanda.itens:
                if item.cozinha_status == 'PREPARANDO':
                    item.cozinha_status = 'PRONTO'

        comanda.status = novo_status
        db.session.commit()
        return True, f"Status updated para {novo_status.value}."

    def calcular_total(self, order_id):
        comanda = self.get_order_by_id(order_id)
        if not comanda:
            return 0.0
        return round(float(sum(i.product.preco * i.quantidade for i in comanda.itens if i.product)), 2)
    
    def gerar_conta(self, comanda):
        if not comanda:
            return None, OrderErrorMessages.COMANDA_NAO_ENCONTRADA

        if comanda.status != OrderStatus.ENTREGUE:
            return None, "A comanda ainda não foi totalmente entregue."

        itens_detalhados = []
        subtotal = 0.0
        
        for item in comanda.itens:
            valor_item = float(item.preco_vendido) * item.quantidade 
            subtotal += valor_item
            itens_detalhados.append({
                'produto': item.product.nome if item.product else 'Produto Removido',
                'quantidade': item.quantidade,
                'preco_unitario': float(item.preco_vendido), 
                'subtotal_item': round(valor_item, 2),
                'observacao': item.observacao or ''
            })
        conta = {
            'comanda_id': comanda.id,
            'mesa': comanda.numero_mesa,
            'itens': itens_detalhados,
            'total': round(subtotal, 2)
        }
        return conta, OrderSuccessMessages.CONTA_GERADA

    def fechar_comanda(self, order_id, user):
        if user.cargo != Role.GARCOM:
            return False, OrderErrorMessages.SEM_PERMISSAO
            
        comanda = self.get_order_by_id(order_id)
        if not comanda:
            return False, OrderErrorMessages.COMANDA_NAO_ENCONTRADA

        if comanda.status not in [OrderStatus.ENTREGUE, OrderStatus.CANCELADO]:
            return False, OrderErrorMessages.COMANDA_NAO_PODE_SER_FECHADA

        conta, mensagem_conta = self.gerar_conta(comanda)
        if conta is None and comanda.status != OrderStatus.CANCELADO:
            return False, mensagem_conta

        if comanda.status == OrderStatus.CANCELADO:
            conta = {'mesa': comanda.numero_mesa, 'itens': [], 'total': 0.0}
        
        comanda.status = OrderStatus.FINALIZADO
        db.session.commit()

        mesa = self.table_service.get_table_by_number(comanda.numero_mesa)
        if mesa:
            comandas_ativas = Order.query.filter(
                Order.numero_mesa == mesa.numero,
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
        
        return True, {"mensagem": OrderSuccessMessages.COMANDA_FECHADA, "conta": conta}
        
    def estatisticas_diarias(self):
        hoje = datetime.now(timezone.utc).replace(tzinfo=None).date()
        inicio_do_dia = datetime.combine(hoje, time.min)
        fim_do_dia = datetime.combine(hoje, time.max)
        
        comandas = Order.query.filter(
            Order.data_criacao >= inicio_do_dia,
            Order.data_criacao <= fim_do_dia
        ).all()
        
        comandas_canceladas = [c for c in comandas if c.status == OrderStatus.CANCELADO]
        comandas_validas = [c for c in comandas if c.status != OrderStatus.CANCELADO]
        
        total_comandas = len(comandas)
        
        # CORREÇÃO: Conta itens apenas se foram efetivamente enviados para a cozinha (não PENDENTE)
        total_itens = sum(
            1 for c in comandas_validas for i in c.itens if i.cozinha_status != 'PENDENTE'
        )
        
        # CORREÇÃO: Faturamento soma apenas de comandas que já foram FINALIZADAS (Pagas)
        total_faturamento = round(
            float(sum(i.preco_vendido * i.quantidade for c in comandas if c.status == OrderStatus.FINALIZADO for i in c.itens if i.product)), 
            2
        )
        
        return {
            "total_comandas": total_comandas,
            "total_comandas_canceladas": len(comandas_canceladas),
            "total_itens": total_itens,
            "total_faturamento": total_faturamento
        }
    
    def tempo_decorrido(self, comanda):
        if not comanda.entrada_cozinha:
            return "Não iniciado"
        
        fim = comanda.saida_cozinha if comanda.status == OrderStatus.PRONTO else datetime.now(timezone.utc).replace(tzinfo=None)
        diferenca = fim - comanda.entrada_cozinha
        total_segundos = int(diferenca.total_seconds())
        
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        return f"{minutos}m {segundos}s"
    
    def get_order_by_id(self, order_id):
        return db.session.get(Order, order_id)

    def open_order_counter(self, numero_mesa=None):
        query = Order.query.filter(Order.status != OrderStatus.CANCELADO)
        if numero_mesa is not None:
            query = query.filter(Order.numero_mesa == numero_mesa)
        return query.count()

    def order_per_table(self):
        mesas = Table.query.all()
        return {mesa.numero: self.open_order_counter(mesa.numero) for mesa in mesas}

    