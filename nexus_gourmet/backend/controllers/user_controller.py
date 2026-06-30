from flask import request, session
from .base_controller import BaseController
from backend.models.enums import Role

class UserController(BaseController):
    def __init__(self, app, user_service, order_service):
        super().__init__(app)
        self.user_service = user_service
        self.order_service = order_service
        self.setup_routes()

    def setup_routes(self):
        #Gerenciamento de usuários (administrador)
        self.app.add_url_rule('/api/login', view_func=self.login, methods=['POST'])
        self.app.add_url_rule('/api/logout', view_func=self.logout, methods=['POST'])

        self.app.add_url_rule('/api/usuarios', view_func=self.listar_usuarios, methods=['GET'])
        self.app.add_url_rule('/api/usuarios/cadastrar', view_func=self.cadastrar_usuario, methods=['POST'])
        self.app.add_url_rule('/api/usuarios/editar_usuario/<cpf_atual>', view_func=self.editar_usuario, methods=['PUT'])
        self.app.add_url_rule('/api/usuarios/deletar_usuario/<cpf_alvo>', view_func=self.deletar_usuario, methods=['DELETE'])
        self.app.add_url_rule('/api/usuarios/visualizar_perfil/<cpf>', view_func=self.visualizar_perfil, methods=['GET'])
        
        #Rota para finalizar o dia e gerar estatísticas
        self.app.add_url_rule('/api/usuarios/finalizar_dia', view_func=self.finalizar_dia, methods=['GET'])

        #Visualizar o próprio perfil
        self.app.add_url_rule('/api/meu_perfil', view_func=self.meu_perfil, methods=['GET'])

    def _get_usuario_logado(self):
        user_cpf = session.get('user_cpf')
        if not user_cpf: 
            return None
        return self.user_service.get_user_by_cpf(user_cpf)

    def login(self):
        dados = request.json or {}
        cpf_input = dados.get('cpf')
        senha_input = dados.get('senha')
        
        success, message, usuario = self.user_service.login(cpf_input, senha_input)
        if success:
            session['user_cpf'] = usuario.cpf
            session['user_nome'] = usuario.nome
            session['user_cargo'] = usuario.cargo.name
            return self.json_response(success=True, message=message, data={
                "nome": usuario.nome, 
                "cpf": usuario.cpf, 
                "cargo": usuario.cargo.value
            })
        return self.json_response(success=False, message=message, status=401)
        
    def logout(self):
        session.clear()
        return self.json_response(success=True, message="Deslogado com sucesso")

    def cadastrar_usuario(self):
        usuario_logado = self._get_usuario_logado()
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)
        
        foto = None
        if request.files or request.form:
            dados = request.form
            foto = request.files.get('foto')
        else:
            dados = request.json or {}

        success, message = self.user_service.cadastrar_usuario(
            cpf_usuario_logado=usuario_logado.cpf,
            senha_admin=dados.get('senha_admin'),
            nome=dados.get('nome'),
            cpf_cadastrado=dados.get('cpf_cadastrado'),
            senha_cadastrada=dados.get('senha_cadastrada'),
            cargo=dados.get('cargo'),
            foto_usuario=foto or dados.get('foto_usuario')
        )
        if not success:
            return self.json_response(False, message, status=400)
        return self.json_response(True, message)
        
    def listar_usuarios(self):
        usuario_logado = self._get_usuario_logado()
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)

        usuarios = self.user_service.listar_usuarios()
        return self.json_response(True, data=[
            {
                "nome": u.nome, 
                "cpf": u.cpf, 
                "cargo": u.cargo.value, 
                "foto_usuario": u.foto_usuario
            } for u in usuarios
        ])
    
    def visualizar_perfil(self, cpf):
        usuario_logado = self._get_usuario_logado()
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)

        dados_user, message = self.user_service.visualizar_usuario(cpf)
        if not dados_user:
            return self.json_response(False, message, status=404)
        return self.json_response(True, message=message, data=dados_user)
    
    def deletar_usuario(self, cpf_alvo):
        usuario_logado = self._get_usuario_logado()
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)

        dados = request.json or {}
        success, message = self.user_service.deletar_usuario(
            cpf_usuario_logado=usuario_logado.cpf,
            senha_admin=dados.get('senha_admin'),
            cpf_alvo=cpf_alvo
        )
        return self.json_response(success, message, status=200 if success else 400)
    
    def editar_usuario(self, cpf_atual):
        usuario_logado = self._get_usuario_logado()
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)

        dados = request.json or {}
        success, message = self.user_service.editar_usuario(
            cpf_usuario_logado=usuario_logado.cpf,
            senha_admin=dados.get('senha_admin'),
            nome=dados.get('nome'),
            cpf_atual=cpf_atual,
            cargo=dados.get('cargo'),
            senha=dados.get('senha'),
            novo_cpf=dados.get('novo_cpf'),
            foto_usuario=dados.get('foto_usuario')
        )
        return self.json_response(success, message, status=200 if success else 400)
            
    def finalizar_dia(self):
        usuario = self._get_usuario_logado()
        if not usuario or usuario.cargo != Role.ADMINISTRADOR:
            return self.json_response(False, "Acesso negado", status=403)
        
        # O método estatisticas_diarias do service calcula os dados do dia corrente globalmente.
        estatisticas = self.order_service.estatisticas_diarias()
        return self.json_response(True, message="Estatísticas diárias geradas com sucesso", data=estatisticas)
    
    def meu_perfil(self):
        usuario = self._get_usuario_logado()
        if not usuario:
            return self.json_response(False, "Usuário não encontrado ou não autenticado", status=401)
        
        dados_user, message = self.user_service.visualizar_usuario(usuario.cpf)
        return self.json_response(True, data=dados_user)

