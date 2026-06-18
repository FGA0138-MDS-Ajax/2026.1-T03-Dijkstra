from flask import request, redirect, session
from .base_controller import BaseController
from backend.models.enums import Role
from backend.services.user_service import UserService

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
        self.app.add_url_rule('/usuarios/visualizar_cargo/<int:user_id>',  view_func=self.visualizar_cargo, methods=['GET'])
        self.app.add_url_rule('/usuarios/deletar_cargo/<int:user_id>', view_func=self.deletar_usuario, methods=['POST'])
        self.app.add_url_rule('/usuarios/mudar_cargo/<int:user_id>',       view_func=self.mudar_cargo,  methods=['POST'])
        self.app.add_url_rule('/usuarios/transferir_posse',    view_func=self.transferir_posse,methods=['POST'])

        #Rota para o cargo do usuário logado
        self.app.add_url_rule('/meu_cargo', view_func=self.meu_cargo,  methods=['GET', 'POST'])

    def login(self):
        if request.method == 'POST':
            login_input = request.form.get('login')
            senha_input = request.form.get('senha')
            
            sucess, message, usuario = self.user_service.autenticar(login_input, senha_input)
            if sucess:
                session['user_id'] = usuario.id
                session['user_nome'] = usuario.nome
                session['user_cargo'] = usuario.cargo.name

                if usuario.cargo == Role.ADMINISTRADOR:
                    return redirect('/usuarios')
                elif usuario.cargo == Role.COZINHEIRO:
                    return redirect('/cozinha/fila')
                return redirect('/salão')
            else:
                return self.render('login.html', error=message)
        return self.render('login.html')
        
    def logout(self):
        session.clear()
        return redirect('/login')

    def cadastrar_usuario(self):
        if session.get('user_cargo') != Role.ADMINISTRADOR.name:
            return "Acesso negado", 403

        nome = request.form.get('nome')
        senha = request.form.get('senha')
        cargo = request.form.get('cargo') # Tipo do usuário (GARCOM, COZINHEIRO ou ADMINISTRADOR)
        
        try:
            cargo = Role[cargo]
            usuario, message = self.user_service.cadastrar_usuario(nome, senha, cargo)
            if not usuario:
                return self.render('usuarios.html', error=message)
            return redirect('/usuarios')
        except KeyError:
            return "cargo do usuário inválido", 400
        
    def listar_usuarios(self):
        if session.get('user_cargo') != Role.ADMINISTRADOR.name:
            return "Acesso negado", 403

        usuarios = self.user_service.listar_usuarios()
        return self.render('usuarios.html', usuarios=usuarios)
    
    def visualizar_cargo(self, user_id):
        if session.get('user_cargo') != Role.ADMINISTRADOR.name:
            return "Acesso negado", 403

        usuario = self.user_service.get_user_by_id(user_id)
        if not usuario:
            return "Usuário não encontrado", 404
        return self.render('cargo_usuario.html', usuario=usuario)
    
    def deletar_usuario(self, user_id):
        if session.get('user_cargo') != Role.ADMINISTRADOR.name:
            return "Acesso negado", 403

        success, message = self.user_service.deletar_usuario(user_id)
        if not success:
            return self.render('usuarios.html', error=message)
        return redirect('/usuarios')
    
    def mudar_cargo(self, user_id):
        if session.get('user_cargo') != Role.ADMINISTRADOR.name:
            return "Acesso negado", 403
        
        novo_cargo_str = request.form.get('novo_cargo')
        try: 
            novo_cargo_enum = Role[novo_cargo_str]
            success, message = self.user_service.mudar_cargo(user_id, novo_cargo_enum)
            
            if not success:
                return self.render('usuarios.html', error=message)
            return redirect('/usuarios')
        except KeyError:
            return "Cargo inválido", 400

    def transferir_posse(self):
        if session.get('user_cargo') != Role.ADMINISTRADOR.name:
            return "Acesso negado", 403

        id_atual = request.form.get('id_atual')
        id_novo = request.form.get('id_novo')
        success, message = self.user_service.transferir_posse(id_atual, id_novo)
        if not success:
            return self.render('usuarios.html', error=message)
        return redirect('/usuarios')
    
    def meu_cargo(self):
        user_id = session.get('user_id')
        if not user_id:
            return redirect('/login')

        usuario = self.user_service.get_user_by_id(user_id)

        if not usuario:
            return "Usuário não encontrado", 404
        return self.render('cargo_usuario.html', usuario=usuario)
    