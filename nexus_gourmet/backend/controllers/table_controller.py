from flask import request, redirect, session
from .base_controller import BaseController
from models.enums import Role

class TableController(BaseController):
    def __init__(self, app, user_service, table_service):
        super().__init__(app)
        self.user_service = user_service
        self.table_service = table_service
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/salão', view_func=self.listar_mesas, methods=['GET'])
        self.app.add_url_rule('/salão/criar', view_func=self.criar_mesa, methods=['POST'])
        self.app.add_url_rule('/salão/editar/<int:numero_mesa>', view_func=self.editar_mesa, methods=['POST'])
        self.app.add_url_rule('/salão/deletar/<int:numero_mesa>', view_func=self.deletar_mesa, methods=['POST'])

    def _get_usuario_logado(self):
        user_id = session.get('user_id')
        if not user_id:
            return None
        return self.user_service.get_user_by_id(user_id)

    def listar_mesas(self):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')
        
        if usuario.cargo != Role.ADMINISTRADOR:
            return "Acesso negado", 403
        
        mesas = self.table_service.listar_mesas()
        return self.render('mesas.html', mesas=mesas)

    def criar_mesa(self):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')

        if usuario.cargo != Role.ADMINISTRADOR:
            return "Acesso negado", 403

        numero = request.form.get('numero')
        capacidade = request.form.get('capacidade')
        success, message = self.table_service.criar_mesa(numero, capacidade)
        if not success:
            return self.render('mesas.html', error=message)

        return redirect('/salão')

    def editar_mesa(self, numero_mesa):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')

        if usuario.cargo != Role.ADMINISTRADOR:
            return "Acesso negado", 403

        numero = request.form.get('numero')
        capacidade = request.form.get('capacidade')
        success, message = self.table_service.editar_mesa(numero_mesa, numero, capacidade)
        if not success:
            return self.render('mesas.html', error=message)
        return redirect(f'/salão/{numero_mesa}')

    def deletar_mesa(self, numero_mesa):
        usuario = self._get_usuario_logado()
        if not usuario:
            return redirect('/login')

        if usuario.cargo != Role.ADMINISTRADOR:
            return "Acesso negado", 403

        success, message = self.table_service.deletar_mesa(numero_mesa)
        if not success:
            return self.render('mesas.html', error=message)

        return redirect('/salão')
