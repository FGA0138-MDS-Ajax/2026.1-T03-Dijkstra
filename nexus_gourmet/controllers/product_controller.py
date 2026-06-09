from flask import request, redirect, session
from .base_controller import BaseController
from models import Usuario, Product
from enums import PerfilUsuario

class ProductController(BaseController):
    def __init__(self, app, product_service):
        super().__init__(app)
        self.product_service = product_service
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/produtos', view_func=self.listar_produtos, methods=['GET'])
        self.app.add_url_rule('/produtos/cadastrar', view_func=self.cadastrar_produto, methods=['POST'])
        self.app.add_url_rule('/produtos/editar/<int:produto_id>', view_func=self.editar_produto, methods=['POST'])
        self.app.add_url_rule('/produtos/deletar/<int:produto_id>', view_func=self.deletar_produto, methods=['POST'])

    def _get_usuario_logado(self):
        user_id = session.get('user_id')
        if not user_id:
            return None
        return self.user_service.get_user_by_id(user_id)

    def listar_produtos(self):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.perfil != PerfilUsuario.ADMINISTRADOR:
            return "Acesso negado", 403
        
        produtos = self.product_service.listar_produtos()
        return self.render('produtos.html', produtos=produtos)

    def cadastrar_produto(self):
        if session.get('user_perfil') != PerfilUsuario.ADMINISTRADOR.name:
            return "Acesso negado", 403
        
        id = request.form.get('id')
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        preco = request.form.get('preco')
        
        success, message = self.product_service.cadastrar_produto(id, nome, categoria, preco)
        if not success:
            return self.render('produtos.html', error=message)
        
        return redirect('/produtos')

    def editar_produto(self):
        if session.get('user_perfil') != PerfilUsuario.ADMINISTRADOR.name:
            return "Acesso negado", 403
        
        id = request.form.get('id')
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        preco = request.form.get('preco')

        success, message = self.product_service.editar_produto(id, nome, categoria, preco)
        if not success:
            return self.render('produtos.html', error=message)
        
        return redirect('/produtos')

    def deletar_produto(self, produto_id):
        if session.get('user_perfil') != PerfilUsuario.ADMINISTRADOR.name:
            return "Acesso negado", 403
        
        success, message = self.product_service.deletar_produto(produto_id)
        if not success:
            return self.render('produtos.html', error=message)
        
        return redirect('/produtos')