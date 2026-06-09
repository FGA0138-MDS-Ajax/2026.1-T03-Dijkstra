from flask import request, redirect, session
from .base_controller import BaseController
from enums import PerfilUsuario
from services.user_service import UserService

class UserController(BaseController):
    def __init__(self, app, user_service: UserService):
        super().__init__(app)
        self.user_service = user_service
        self.setup_routes()

    def setup_routes(self):
        #Rotas de autenticação
        self.app.add_url_rule('/login', view_func=self.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/logout', view_func=self.logout, methods=['GET'])

        #Rotas de gerenciamento de usuários (para administradores)
        self.app.add_url_rule('/usuarios',   view_func=self.listar_usuarios, methods=['GET'])
        self.app.add_url_rule('/usuarios/cadastrar', view_func=self.cadastrar_usuario, methods=['POST'])
        self.app.add_url_rule('/usuarios/visualizar_perfil/<int:user_id>',  view_func=self.visualizar_perfil, methods=['GET'])
        self.app.add_url_rule('/usuarios/deletar_perfil/<int:user_id>', view_func=self.deletar_usuario, methods=['POST'])
        self.app.add_url_rule('/usuarios/mudar_cargo/<int:user_id>',       view_func=self.mudar_cargo,  methods=['POST'])
        self.app.add_url_rule('/usuarios/transferir_posse/<int:user_id>',    view_func=self.transferir_posse,methods=['POST'])

        #Rota para o perfil do usuário logado
        self.app.add_url_rule('/meu_perfil', view_func=self.meu_perfil,  methods=['GET', 'POST'])


    def login(self):
        if request.method == 'POST':
            login_input = request.form.get('login')
            senha_input = request.form.get('senha')
            
            usuario = self.user_service.autenticar(login_input, senha_input)
            if usuario:
                session['user_id'] = usuario.id
                session['user_name'] = usuario.nome
                session['user_perfil'] = usuario.perfil.name
                
                if usuario.perfil == PerfilUsuario.COZINHEIRO:
                    return redirect('/cozinha/fila')
                return redirect('/mesas')
            else:
                return self.render('login.html', error = 'Login ou senha inválidos')
        
        return self.render('login.html')

    def logout(self):
        session.clear()
        return redirect('/login')

    def cadastrar_usuario(self):
        if session.get('user_perfil') != PerfilUsuario.ADMINISTRADOR.name:
            return "Acesso negado", 403

        nome = request.form.get('nome')
        login = request.form.get('login')
        senha = request.form.get('senha')
        perfil_str = request.form.get('perfil') # Tipo do usuário (GARCOM, COZINHEIRO ou ADMINISTRADOR)
        
        try:
            perfil_enum = PerfilUsuario[perfil_str]
            usuario, message = self.user_service.criar_usuario(nome, login, senha, perfil_enum)
            if not usuario:
                return self.render('usuarios.html', error=message)
            return redirect('/usuarios')
        except KeyError:
            return "Perfil do usuário inválido", 400
        
    def listar_usuarios(self):
        if session.get('user_perfil') != PerfilUsuario.ADMINISTRADOR.name:
            return "Acesso negado", 403

        usuarios = self.user_service.listar_usuarios()
        return self.render('usuarios.html', usuarios=usuarios)
    
    def visualizar_perfil(self, user_id):
        if session.get('user_perfil') != PerfilUsuario.ADMINISTRADOR.name:
            return "Acesso negado", 403

        usuario = self.user_service.get_by_user_id(user_id)
        if not usuario:
            return "Usuário não encontrado", 404
        return self.render('perfil_usuario.html', usuario=usuario)
    
    def deletar_usuario(self, user_id):
        if session.get('user_perfil') != PerfilUsuario.ADMINISTRADOR.name:
            return "Acesso negado", 403

        success, message = self.user_service.deletar_usuario(user_id)
        if not success:
            return self.render('usuarios.html', error=message)
        return redirect('/usuarios')
    
    def mudar_cargo(self, user_id):
        if session.get('user_perfil') != PerfilUsuario.ADMINISTRADOR.name:
            return "Acesso negado", 403
        
        novo_cargo_str = request.form.get('novo_cargo')
        try: 
            novo_cargo_enum = PerfilUsuario[novo_cargo_str]
            success, message = self.user_service.mudar_cargo(user_id, novo_cargo_enum)
            
            if not success:
                return self.render('usuarios.html', error=message)
            return redirect('/usuarios')
        except KeyError:
            return "Cargo inválido", 400

    def transferir_posse(self, user_id):
        if session.get('user_perfil') != PerfilUsuario.ADMINISTRADOR.name:
            return "Acesso negado", 403
        
        success, message = self.user_service.transferir_posse(user_id)
        if not success:
            return self.render('usuarios.html', error=message)
        return redirect('/usuarios')
    
    def meu_perfil(self):
        user_id = session.get('user_id')
        if not user_id:
            return redirect('/login')

        usuario = self.user_service.get_by_user_id(user_id)

        if not usuario:
            return "Usuário não encontrado", 404
        return self.render('perfil_usuario.html', usuario=usuario)
    