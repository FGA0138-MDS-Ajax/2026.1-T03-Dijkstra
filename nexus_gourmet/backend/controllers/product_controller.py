from flask import request, session
from .base_controller import BaseController
from backend.models.enums import Role

class ProductController(BaseController):
    def __init__(self, app, user_service, product_service):
        super().__init__(app)
        self.user_service = user_service
        self.product_service = product_service
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/api/produtos', view_func=self.listar_produtos, methods=['GET'])
        self.app.add_url_rule('/api/produtos/categoria/<categoria>', view_func=self.listar_por_categoria, methods=['GET'])
        self.app.add_url_rule('/api/produtos/cadastrar', view_func=self.cadastrar_produto, methods=['POST'])
        self.app.add_url_rule('/api/produtos/editar/<int:product_id>', view_func=self.editar_produto, methods=['PUT'])
        self.app.add_url_rule('/api/produtos/deletar/<int:product_id>', view_func=self.deletar_produto, methods=['DELETE'])

    def _get_usuario_logado(self):
        user_id = session.get('user_id')
        if not user_id: return None
        return self.user_service.get_user_by_id(user_id)

    def listar_produtos(self):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo not in [Role.ADMINISTRADOR, Role.GARCOM]:
            return self.json_response(False, "Acesso negado", status=403)
        
        produtos = self.product_service.listar_produtos()
        return self.json_response(True, data=[p.to_dict() for p in produtos])
    
    def listar_por_categoria(self, categoria):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)
        
        produtos = self.product_service.listar_por_categoria(categoria)
        return self.json_response(True, data=[p.to_dict() for p in produtos])

    def cadastrar_produto(self):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)
        
        dados = request.json or {}
        success, message = self.product_service.cadastrar_produto(
            dados.get('nome'), dados.get('categoria'), dados.get('preco')
        )
        return self.json_response(success, message, status=200 if success else 400)

    def editar_produto(self, product_id):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)
        
        dados = request.json or {}
        success, message = self.product_service.editar_produto(
            product_id, dados.get('nome'), dados.get('categoria'), dados.get('preco')
        )
        return self.json_response(success, message, status=200 if success else 400)

    def deletar_produto(self, product_id):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)
        
        success, message = self.product_service.deletar_produto(product_id)
        return self.json_response(success, message, status=200 if success else 400)