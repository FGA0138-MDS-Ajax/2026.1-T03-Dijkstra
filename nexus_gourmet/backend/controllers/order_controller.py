from flask import request, redirect, session
from .base_controller import BaseController
from models.enums import OrderStatus, Role

class OrderController(BaseController):
    def __init__(self, app, user_service, order_service, table_service):
        super().__init__(app)
        self.user_service = user_service
        self.order_service = order_service
        self.table_service = table_service
        self.setup_routes()

    def setup_routes(self):
        #Rota para a fila de pedidos na cozinha
        self.app.add_url_rule('/cozinha/fila',view_func=self.listar_todas_comandas, methods=['GET'])

        #Rota para visualizar mesas e comandas
        self.app.add_url_rule('/salão', view_func=self.listar_mesas, methods=['GET'])
        self.app.add_url_rule('/salão/<int:numero_mesa>/comandas', view_func=self.listar_comandas_mesa, methods=['GET'])
        self.app.add_url_rule('/salão/<int:numero_mesa>/comandas/abrir_comanda', view_func=self.abrir_comanda, methods=['POST'])
        self.app.add_url_rule('/salão/<int:numero_mesa>/comandas/<int:comanda_id>', view_func=self.visualizar_comanda, methods=['GET'])

        #Rota para gerenciamento de comandas de uma mesa específica
        self.app.add_url_rule('/salão/<int:numero_mesa>/comandas/<int:comanda_id>/adicionar_item', view_func=self.adicionar_item, methods=['POST'])
        self.app.add_url_rule('/salão/<int:numero_mesa>/comandas/<int:comanda_id>/editar_comanda', view_func=self.editar_comanda, methods=['POST'])
        self.app.add_url_rule('/salão/<int:numero_mesa>/comandas/<int:comanda_id>/enviar_comanda', view_func=self.enviar_comanda, methods=['POST'])
        self.app.add_url_rule('/salão/<int:numero_mesa>/comandas/<int:comanda_id>/alterar_status:<string:status>', view_func=self.alterar_status, methods=['POST']) #Única rota que o cozinheiro terá acesso
        self.app.add_url_rule('/salão/<int:numero_mesa>/comandas/<int:comanda_id>/fechar', view_func=self.fechar_comanda, methods=['GET'])

    def _get_usuario_logado(self):
        user_id = session.get('user_id')
        if not user_id:
            return None
        return self.user_service.get_user_by_id(user_id)
    
    def listar_todas_comandas(self):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        pedidos = self.order_service.listar_todas_comandas()
        return self.render('pedidos.html', pedidos=pedidos)
    
    def listar_mesas(self):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.cargo != Role.GARCOM:
            return "Acesso negado", 403
        
        mesas = self.table_service.listar_mesas()
        return self.render('mesas.html', mesas=mesas)
    
    def listar_comandas_mesa(self, numero_mesa):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.cargo != Role.GARCOM:
            return "Acesso negado", 403
        
        comandas = self.table_service.listar_comandas_mesa(numero_mesa)
        return self.render('comandas.html', comandas=comandas, numero_mesa=numero_mesa)

    def abrir_comanda(self, numero_mesa):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.cargo != Role.GARCOM:
            return "Acesso negado", 403
        
        comanda_id, message = self.order_service.abrir_comanda(numero_mesa, usuario.id)
        if not comanda_id:
            return self.render('mesas.html', error=message)
        return redirect(f'/salão/{numero_mesa}/comandas/{comanda_id}/adicionar_item')
    
    def visualizar_comanda(self, numero_mesa, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.cargo != Role.GARCOM:
            return "Acesso negado", 403
        
        comanda = self.order_service.get_order_by_id(comanda_id)
        if not comanda or comanda.numero_mesa != numero_mesa:
            return "Comanda não encontrada", 404
        
        return self.render('comanda.html', comanda=comanda)
    
    def adicionar_item(self, numero_mesa, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.cargo != Role.GARCOM:
            return "Acesso negado", 403
        
        product_id = request.form.get('product_id')
        quantidade = request.form.get('quantidade')
        observacao = request.form.get('observacao')

        success, message = self.order_service.adicionar_item(comanda_id, product_id, quantidade, observacao, usuario)
        if not success:
            return self.render('comanda.html', error=message)
        return redirect(f'/salão/{numero_mesa}/comandas/{comanda_id}/')

    def editar_comanda(self, numero_mesa, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.cargo != Role.GARCOM:
            return "Acesso negado", 403
        
        product_id = request.form.get('product_id')
        nova_quantidade = request.form.get('quantidade')
        observacao = request.form.get('observacao')

        itens_para_editar = [{
            'product_id': product_id,
            'quantidade': nova_quantidade,
            'observacao': observacao
        }]

        sucess, message = self.order_service.editar_comanda(comanda_id, itens_para_editar, usuario)
        if not sucess:
            return self.render('comanda.html', error=message)
        return redirect(f'/salão/{numero_mesa}/comandas/{comanda_id}/')
        
    def enviar_comanda(self, numero_mesa, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.cargo != Role.GARCOM:
            return "Acesso negado", 403

        success, message = self.order_service.enviar_comanda(comanda_id, usuario)
        if not success:
            return self.render('comanda.html', error=message)
        return redirect('/salão')
    
    def alterar_status(self, numero_mesa, comanda_id, status):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.cargo != Role.COZINHEIRO:
            return "Acesso negado", 403

        try:
            novo_status = OrderStatus(status)
        except ValueError:
            return "Status inválido", 400

        success, message = self.order_service.alterar_status(comanda_id, novo_status, usuario)
        if not success:
            return self.render('comanda.html', error=message)
        return redirect('/cozinha/fila')
        
    def fechar_comanda(self, numero_mesa, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')        
    
        if usuario.cargo != Role.GARCOM:
            return "Acesso negado", 403
        
        try:
            quantity = int(self.order_service.open_order_counter(numero_mesa))
        except Exception:
            quantity = None

        success, message = self.order_service.fechar_comanda(comanda_id)
        if not success:
            return self.render('comanda.html', error=message)
        
        elif quantity is not None and quantity > 0:
            return redirect(f'/salão/{numero_mesa}/comandas')
        
        return redirect('/salão')