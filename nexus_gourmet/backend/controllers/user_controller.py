from flask import request, session
from .base_controller import BaseController
from backend.models.enums import Role
from backend.services.user_service import UserService

class UserController(BaseController):
    def __init__(self, app, user_service: UserService):
        super().__init__(app)
        self.user_service = user_service
        self.setup_routes()

    def setup_routes(self):
        #Gerenciamento de usuários (administrador)
        self.app.add_url_rule('/api/login', view_func=self.login, methods=['POST'])
        self.app.add_url_rule('/api/logout', view_func=self.logout, methods=['POST'])

        self.app.add_url_rule('/api/usuarios', view_func=self.listar_usuarios, methods=['GET'])
        self.app.add_url_rule('/api/usuarios/cadastrar', view_func=self.cadastrar_usuario, methods=['POST'])
        self.app.add_url_rule('/api/usuarios/editar_usuario/<int:user_id>', view_func=self.editar_usuario, methods=['PUT'])
        self.app.add_url_rule('/api/usuarios/deletar_usuario/<int:user_id>', view_func=self.deletar_usuario, methods=['DELETE'])
        self.app.add_url_rule('/api/usuarios/visualizar_perfil/<int:user_id>', view_func=self.visualizar_perfil, methods=['GET'])
        
        #Rota para finalizar o dia e gerar estatísticas
        self.app.add_url_rule('/api/usuarios/finalizar_dia', view_func=self.finalizar_dia, methods=['PUT'])


        #Visualizar o próprio perfil
        self.app.add_url_rule('/api/meu_perfil', view_func=self.meu_perfil, methods=['GET'])

    def login(self):
        dados = request.json or {}
        login_input = dados.get('login')
        senha_input = dados.get('senha')
        
        sucess, message, usuario = self.user_service.autenticar(login_input, senha_input)
        if sucess:
            session['user_cpf'] = usuario.cpf
            session['user_nome'] = usuario.nome
            session['user_cargo'] = usuario.cargo.name
            return self.json_response(success=True, data=usuario.to_dict())
        return self.json_response(success=False, message=message, status=401)
        
    def logout(self):
        session.clear()
        return self.json_response(success=True, message="Deslogado com sucesso")

    def cadastrar_usuario(self):
        if session.get('user_cargo') != Role.ADMINISTRADOR.name:
            return self.json_response(False, "Acesso negado", status=403)
        
        foto = None
        if request.files or request.form:
            dados = request.form
            foto = request.files.get('foto')
        else:
            dados = request.json or {}

        try:
            cargo = Role[dados.get('cargo')]
            usuario, message = self.user_service.cadastrar_usuario(dados.get('nome'), dados.get('senha'), cargo, foto)
            if not usuario:
                return self.json_response(False, message, status=400)
            return self.json_response(True, message)
        except KeyError:
            return self.json_response(False, "Cargo inválido", status=400)
        
    def listar_usuarios(self):
        if session.get('user_cargo') != Role.ADMINISTRADOR.name:
            return self.json_response(False, "Acesso negado", status=403)

        usuarios = self.user_service.listar_usuarios()
        return self.json_response(True, data=[u.to_dict() for u in usuarios])
    
    def visualizar_perfil(self, user_id):
        if session.get('user_cargo') != Role.ADMINISTRADOR.name:
            return self.json_response(False, "Acesso negado", status=403)

        usuario = self.user_service.get_user_by_id(user_id)
        if not usuario:
            return self.json_response(False, "Usuário não encontrado", status=404)
        return self.json_response(True, data=usuario.to_dict())
    
    def deletar_usuario(self, user_id):
        if session.get('user_cargo') != Role.ADMINISTRADOR.name:
            return self.json_response(False, "Acesso negado", status=403)

        success, message = self.user_service.deletar_usuario(user_id)
        return self.json_response(success, message, status=200 if success else 400)
    
    def editar_usuario(self, user_id):
        if session.get('user_cargo') != Role.ADMINISTRADOR.name:
            return self.json_response(False, "Acesso negado", status=403)

        dados = request.json or {}
        try:
            cargo = Role[dados.get('cargo')] if dados.get('cargo') else None
            success, message = self.user_service.editar_usuario(Role[session.get('user_cargo')], user_id, dados.get('nome'), cargo)
            return self.json_response(success, message, status=200 if success else 400)
        except KeyError:
            return self.json_response(False, "Cargo inválido", status=400)
            
    def finalizar_dia(self, numero_mesa):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)
        
        estatisticas, message = self.order_service.estatisticas_diarias(numero_mesa)
        if not estatisticas:
            return self.json_response(False, message, status=400)
        return self.json_response(True, message, data=estatisticas)
    
    def meu_perfil(self):
        user_cpf = session.get('user_cpf')
        if not user_cpf:
            return self.json_response(False, "Usuário não autenticado", status=401)

        usuario = self.user_service.get_user_by_cpf(user_cpf)
        if not usuario:
            return self.json_response(False, "Usuário não encontrado", status=404)
        return self.json_response(True, data=usuario.to_dict())
    
    