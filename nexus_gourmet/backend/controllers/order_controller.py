from flask import request, redirect, session
from .base_controller import BaseController
from models import Usuario
from enums import StatusPedido, PerfilUsuario
from services.user_service import UserService
from services.order_service import OrderService
from services.table_service import TableService

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
        self.app.add_url_rule('/mesas', view_func=self.listar_mesas, methods=['GET'])
        self.app.add_url_rule('/mesas/<int:mesa_id>/comandas', view_func=self.listar_comandas_mesa, methods=['GET'])
        self.app.add_url_rule('/mesas/<int:mesa_id>/comandas/abrir_comanda', view_func=self.abrir_comanda, methods=['POST'])
        self.app.add_url_rule('/mesas/<int:mesa_id>/comandas/<int:comanda_id>/', view_func=self.visualizar_comanda, methods=['GET'])

        #Rota para gerenciamento de comandas de uma mesa específica
        self.app.add_url_rule('/mesas/<int:mesa_id>/comandas/<int:comanda_id>/adicionar_item', view_func=self.adicionar_item, methods=['POST'])
        self.app.add_url_rule('/mesas/<int:mesa_id>/comandas/<int:comanda_id>/editar', view_func=self.editar_comanda, methods=['POST'])
        self.app.add_url_rule('/mesas/<int:mesa_id>/comandas/<int:comanda_id>/enviar', view_func=self.enviar_comanda, methods=['POST'])
        self.app.add_url_rule('/mesas/<int:mesa_id>/comandas/<int:comanda_id>/status:<string:status>', view_func=self.alterar_status, methods=['POST']) #Única rota que o cozinheiro terá acesso
        self.app.add_url_rule('/mesas/<int:mesa_id>/comandas/<int:comanda_id>/fechar', view_func=self.fechar_comanda, methods=['GET'])

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
        
        if usuario.perfil != PerfilUsuario.GARCOM:
            return "Acesso negado", 403
        
        mesas = self.table_service.listar_mesas()
        return self.render('mesas.html', mesas=mesas)
    
    def listar_comandas_mesa(self, mesa_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.perfil != PerfilUsuario.GARCOM:
            return "Acesso negado", 403
        
        comandas = self.table_service.listar_comandas_mesa(mesa_id)
        return self.render('comandas.html', comandas=comandas, mesa_id=mesa_id)

    def abrir_comanda(self):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.perfil != PerfilUsuario.GARCOM:
            return "Acesso negado", 403
        
        mesa_id = request.form.get('mesa_id')
        success, message = self.order_service.abrir_comanda(mesa_id, user.cargo)
        if not success:
            return self.render('mesas.html', error=message)
        return redirect(f'/mesas/{mesa_id}/comandas/<int:comanda_id>/adicionar_item')
    
    def visualizar_comanda(self, mesa_id, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.perfil != PerfilUsuario.GARCOM:
            return "Acesso negado", 403
        
        comanda = self.order_service.get_comanda_by_id(comanda_id)
        if not comanda or comanda.mesa_id != mesa_id:
            return "Comanda não encontrada", 404
        
        return self.render('comanda.html', comanda=comanda)
    
    def adicionar_item(self, mesa_id, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.perfil != PerfilUsuario.GARCOM:
            return "Acesso negado", 403
        
        item_id = request.form.get('item_id')
        quantidade = request.form.get('quantidade')
        observacao = request.form.get('observacao')

        success, message = self.order_service.adicionar_item(comanda_id, item_id, quantidade, observacao, usuario)
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
            success, message = self.order_service.editar_comanda(comanda_id, item_id, nova_quantidade, usuario)
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
        
        success, message = self.order_service.alterar_status(comanda_id, status, usuario)        
        if not success:
            return self.render('pedidos.html', error=message)
        return redirect('/cozinha/fila')
        
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