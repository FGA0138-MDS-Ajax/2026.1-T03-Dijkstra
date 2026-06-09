from flask import request, redirect, session
from .base_controller import BaseController
from models import Usuario
from enums import StatusPedido, PerfilUsuario
from services.user_service import UserService
from services.order_service import OrderService

class OrderController(BaseController):
    def __init__(self, app, order_service):
        super().__init__(app)
        self.order_service = order_service
        self.setup_routes()

    def setup_routes(self):
        #Rota para a fila de pedidos na cozinha
        self.app.add_url_rule('/cozinha/fila',view_func=self.listar_itens_pedidos, methods=['GET'])

        #Rota para gerenciamento dos pedidos
        self.app.add_url_rule('/mesas/<int:mesa_id>/abrir_comanda', view_func=self.abrir_comanda, methods=['POST'])
        self.app.add_url_rule('/mesas/<int:mesa_id>/comandas/<int:comanda_id>/adicionar_item', view_func=self.adicionar_item, methods=['POST'])
        self.app.add_url_rule('/mesas/<int:mesa_id>/editar_comanda/<int:comanda_id>', view_func=self.editar_comanda, methods=['POST'])
        self.app.add_url_rule('/mesas/<int:mesa_id>/comandas/<int:comanda_id>/enviar', view_func=self.enviar_comanda, methods=['POST'])
        self.app.add_url_rule('/mesas/<int:mesa_id>/comandas/<int:comanda_id>/status:<string:status>', view_func=self.alterar_status, methods=['POST']) #Única rota que o cozinheiro terá acesso
        self.app.add_url_rule('/mesas/<int:mesa_id>/comandas/<int:comanda_id>/fechar', view_func=self.fechar_comanda, methods=['GET'])

    def _get_usuario_logado(self):
        user_id = session.get('user_id')
        if not user_id:
            return None
        return self.user_service.get_user_by_id(user_id)

    def listar_itens_pedidos(self):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        pedidos = self.order_service.get_fila_cozinha(usuario.id)
        return self.render('pedidos.html', pedidos=pedidos)
    
    def abrir_comanda(self):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.perfil != PerfilUsuario.GARCOM:
            return "Acesso negado", 403
        
        mesa_id = request.form.get('mesa_id')
        success, message = self.order_service.abrir_comanda(mesa_id, usuario.id)
        if not success:
            return self.render('mesas.html', error=message)
        return redirect(f'/mesas/{mesa_id}/comandas/<int:comanda_id>/adicionar_item')
    
    def adicionar_item(self, mesa_id, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.perfil != PerfilUsuario.GARCOM:
            return "Acesso negado", 403
        
        item_id = request.form.get('item_id')
        quantidade = request.form.get('quantidade')
        observacao = request.form.get('observacao')

        success, message = self.order_service.adicionar_item(comanda_id, item_id, quantidade, observacao)
        if not success:
            return self.render('comanda.html', error=message)
        return redirect(f'/mesas/{mesa_id}/comandas/{comanda_id}/')
    
    def editar_comanda(self, mesa_id, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.perfil != PerfilUsuario.GARCOM:
            return "Acesso negado", 403
        
        item_id = request.form.get('item_id')
        nova_quantidade = request.form.get('nova_quantidade')
        if not nova_quantidade or int(nova_quantidade) <= 0:
            success, message = self.order_service.remover_item(comanda_id, item_id)
        else:
            success, message = self.order_service.editar_comanda(comanda_id, item_id, nova_quantidade)
        if not success:
            return self.render('comanda.html', error=message)
        return redirect(f'/mesas/{mesa_id}/comandas/{comanda_id}/')
        
    def enviar_comanda(self, mesa_id, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.perfil != PerfilUsuario.GARCOM:
            return "Acesso negado", 403

        success, message = self.order_service.enviar_comanda(comanda_id)
        if not success:
            return self.render('comanda.html', error=message)
        return redirect('/mesas')
    
    def alterar_status(self, mesa_id, comanda_id, status):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        try:
            novo_status_enum = StatusPedido[status.upper()]
            success, message = self.order_service.alterar_status(comanda_id, novo_status_enum)
            if not success:
                return self.render('pedidos.html', error=message)
            return redirect('/cozinha/fila')
        except KeyError:
            return "Status inválido", 400
        
    def fechar_comanda(self, mesa_id, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')        
    
        if usuario.perfil != PerfilUsuario.GARCOM:
            return "Acesso negado", 403
        
        try:
            quantity = int(self.order_service.count_open_comandas(mesa_id))
        except Exception:
            quantity = None

        success, message = self.order_service.fechar_comanda(comanda_id)
        if not success:
            return self.render('comanda.html', error=message)
        
        elif quantity is not None and quantity > 0:
            return redirect(f'/mesas/{mesa_id}/comandas')
        
        return redirect('/mesas')