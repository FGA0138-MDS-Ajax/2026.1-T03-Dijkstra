from flask import request, session
from .base_controller import BaseController
from models.enums import Role

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
        user_cpf = session.get('user_cpf')
        if not user_cpf: 
            return None
        return self.user_service.get_user_by_cpf(user_cpf)

    def listar_produtos(self):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo not in [Role.ADMINISTRADOR, Role.GARCOM]:
            return self.json_response(False, "Acesso negado", status=403)
        
        produtos = self.product_service.listar_produtos()
        dados_produtos = [
            {
                "id": p.id, 
                "nome": p.nome, 
                "categoria": p.categoria.value, 
                "preco": p.preco, 
                "tempo_preparacao": p.tempo_preparacao,
                "foto_produto": p.foto_prato
            } for p in produtos
        ]
        return self.json_response(True, data=dados_produtos)
    
    def listar_por_categoria(self, categoria):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo not in [Role.ADMINISTRADOR, Role.GARCOM]:
            return self.json_response(False, "Acesso negado", status=403)
        
        produtos = self.product_service.listar_por_categoria(categoria)
        dados_produtos = [
            {
                "id": p.id, 
                "nome": p.nome, 
                "categoria": p.categoria.value, 
                "preco": p.preco, 
                "tempo_preparacao": p.tempo_preparacao,
                "foto_produto": p.foto_prato
            } for p in produtos
        ]
        return self.json_response(True, data=dados_produtos)

    def cadastrar_produto(self):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)
        
        foto = None
        if request.files or request.form:
            dados = request.form
            foto = request.files.get('foto_produto')
        else:
            dados = request.json or {}

        success, message = self.product_service.cadastrar_produto(
            dados.get('nome'), 
            dados.get('categoria'), 
            dados.get('preco'),
            dados.get('tempo_preparacao', 15),
            foto_produto=foto or dados.get('foto_produto'),
            user_role=usuario.cargo
        )
        return self.json_response(success, message, status=200 if success else 400)

    def editar_produto(self, product_id):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)
        
        foto = None
        if request.files or request.form:
            dados = request.form
            foto = request.files.get('foto_produto')
        else:
            dados = request.json or {}

        success, message = self.product_service.editar_produto(
            product_id, 
            dados.get('nome'), 
            dados.get('categoria'), 
            dados.get('preco'),
            dados.get('tempo_preparacao', 15),
            foto_produto=foto or dados.get('foto_produto'),
            user_role=usuario.cargo
        )
        return self.json_response(success, message, status=200 if success else 400)

    def deletar_produto(self, product_id):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)
        
        success, message = self.product_service.deletar_produto(product_id, user_role=usuario.cargo)
        return self.json_response(success, message, status=200 if success else 400)
