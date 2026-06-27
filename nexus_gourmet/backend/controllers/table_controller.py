from flask import request, session
from .base_controller import BaseController
from backend.models.enums import Role

class TableController(BaseController):
    def __init__(self, app, user_service, table_service):
        super().__init__(app)
        self.user_service = user_service
        self.table_service = table_service
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/api/salao', view_func=self.listar_mesas, methods=['GET'])
        self.app.add_url_rule('/api/salao/criar_mesa', view_func=self.criar_mesa, methods=['POST'])
        self.app.add_url_rule('/api/salao/editar_mesa/<int:numero_mesa>', view_func=self.editar_mesa, methods=['PUT'])
        self.app.add_url_rule('/api/salao/deletar_mesa/<int:numero_mesa>', view_func=self.deletar_mesa, methods=['DELETE'])

    def _get_usuario_logado(self):
        user_cpf = session.get('user_cpf')
        if not user_cpf: return None
        return self.user_service.get_user_by_cpf(user_cpf)

    def listar_mesas(self):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo not in [Role.ADMINISTRADOR, Role.GARCOM]:
            return self.json_response(False, "Acesso negado", status=403)
        
        mesas = self.table_service.listar_mesas()
        return self.json_response(True, data=mesas)

    def criar_mesa(self):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)

        dados = request.json or {}
        success, message = self.table_service.criar_mesa(dados.get('capacidade'))
        return self.json_response(success, message, status=200 if success else 400)

    def editar_mesa(self, numero_mesa):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)

        dados = request.json or {}
        success, message = self.table_service.editar_mesa(numero_mesa, capacidade=dados.get('capacidade'))
        return self.json_response(success, message, status=200 if success else 400)

    def deletar_mesa(self, numero_mesa):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)

        success, message = self.table_service.deletar_mesa(numero_mesa)
        return self.json_response(success, message, status=200 if success else 400)