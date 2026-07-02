from flask import request, session
from .base_controller import BaseController
from backend.models.enums import Role

class OrderController(BaseController):
    def __init__(self, app, user_service, order_service, table_service):
        super().__init__(app)
        self.user_service = user_service
        self.order_service = order_service
        self.table_service = table_service
        self.setup_routes()

    def setup_routes(self):
        #Rota para visualizar todas as comandas (cozinha)
        self.app.add_url_rule('/api/cozinha/fila', view_func=self.listar_todas_comandas, methods=['GET'])
        self.app.add_url_rule('/api/cozinha/<int:comanda_id>/alterar_status', view_func=self.alterar_status, methods=['PUT']) 

        #Rotas para gerenciamento de comandas (garçom)
        self.app.add_url_rule('/api/salao/<int:numero_mesa>/comandas', view_func=self.listar_comandas_mesa, methods=['GET'])
        self.app.add_url_rule('/api/salao/<int:numero_mesa>/comandas/abrir_comanda', view_func=self.abrir_comanda, methods=['POST'])
        self.app.add_url_rule('/api/salao/<int:numero_mesa>/comandas/<int:comanda_id>', view_func=self.visualizar_comanda, methods=['GET'])
        self.app.add_url_rule('/api/salao/<int:numero_mesa>/comandas/<int:comanda_id>/adicionar_item', view_func=self.adicionar_item, methods=['POST'])
        self.app.add_url_rule('/api/salao/<int:numero_mesa>/comandas/<int:comanda_id>/editar_comanda', view_func=self.editar_comanda, methods=['PUT'])
        self.app.add_url_rule('/api/salao/<int:numero_mesa>/comandas/<int:comanda_id>/enviar_comanda', view_func=self.enviar_comanda, methods=['POST'])
        self.app.add_url_rule('/api/salao/<int:numero_mesa>/comandas/<int:comanda_id>/fechar_comanda', view_func=self.fechar_comanda, methods=['POST'])

    def _get_usuario_logado(self):
        user_cpf = session.get('user_cpf')
        if not user_cpf: 
            return None
        return self.user_service.get_user_by_cpf(user_cpf)
    
    def alterar_status(self, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario:
            return self.json_response(False, "Não autorizado", status=401)

        dados = request.json or {}
        status_input = dados.get('status')

        success, message = self.order_service.alterar_status(comanda_id, status_input, usuario)
        return self.json_response(success, message, status=200 if success else 400)

    def listar_todas_comandas(self):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo not in [Role.ADMINISTRADOR, Role.COZINHEIRO]:
            return self.json_response(False, "Acesso negado", status=403)
        
        if not usuario: 
            return self.json_response(False, "Não autorizado", status=401)
        
        pedidos = self.order_service.listar_todas_comandas()
        return self.json_response(True, data=pedidos)
    
    def listar_comandas_mesa(self, numero_mesa):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.GARCOM:
            return self.json_response(False, "Acesso negado", status=403)
        
        comandas, msg = self.table_service.listar_comandas_mesa(numero_mesa)
        if comandas is False:
            return self.json_response(False, msg, status=404)
        return self.json_response(True, data=comandas)

    def abrir_comanda(self, numero_mesa):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.GARCOM:
            return self.json_response(False, "Acesso negado", status=403)
        
        comanda_id, message = self.order_service.abrir_comanda(numero_mesa, usuario.cpf)
        if not comanda_id:
            return self.json_response(False, message, status=400)
        return self.json_response(True, message, data={"comanda_id": comanda_id})
    
    def visualizar_comanda(self, numero_mesa, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.GARCOM:
            return self.json_response(False, "Acesso negado", status=403)
        
        comanda = self.order_service.visualizar_comanda(comanda_id)
        if not comanda or comanda.numero_mesa != numero_mesa:
            return self.json_response(False, "Comanda não encontrada", status=404)
        
        dados_formatados = self.order_service._formatar_comanda(comanda)
        return self.json_response(True, data=dados_formatados)
    
    def adicionar_item(self, numero_mesa, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.GARCOM:
            return self.json_response(False, "Acesso negado", status=403)
        
        dados = request.json or {}
        success, message = self.order_service.adicionar_item(
            comanda_id, dados.get('product_id'), dados.get('quantidade'), dados.get('observacao'), usuario
        )
        return self.json_response(success, message, status=200 if success else 400)

    def editar_comanda(self, numero_mesa, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.GARCOM:
            return self.json_response(False, "Acesso negado", status=403)
        
        dados = request.json or {}
        itens_para_editar = dados.get('itens', [])
        cancelar = dados.get('cancelar', False)

        success, message = self.order_service.editar_comanda(comanda_id, itens_para_editar, usuario, cancelar=cancelar)
        return self.json_response(success, message, status=200 if success else 400)
        
    def enviar_comanda(self, numero_mesa, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.GARCOM:
            return self.json_response(False, "Acesso negado", status=403)

        success, message = self.order_service.enviar_comanda(comanda_id, usuario)
        return self.json_response(success, message, status=200 if success else 400)  
        
    def fechar_comanda(self, numero_mesa, comanda_id):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.GARCOM:
            return self.json_response(False, "Acesso negado", status=403)

        success, resultado = self.order_service.fechar_comanda(comanda_id, usuario)
        
        if success:
            return self.json_response(
                True, 
                message=resultado["mensagem"], 
                data={"conta": resultado["conta"]}
            )
        else:
            return self.json_response(False, message=resultado, status=400)
