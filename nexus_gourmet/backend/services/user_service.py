from models import db, User
from enums import Role
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
 
 
class UsuarioService:

    def login(self, id, senha):
        usuario = self.get_by_user_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        if not check_password_hash(usuario.senha, senha):
            return False, "Senha incorreta."
        return True, "Login bem-sucedido.", usuario
    
    def logout(self, id):
        usuario = self.get_by_user_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        return True, "Logout bem-sucedido."
    
    def listar_usuarios(self):
        return User.query.all()
    
    def cadastrar_usuario(self, id, nome, senha, cargo):
        if self.get_by_user_id(id):
            return False, "ID de usuário já existe."
        try:
            cargo = Role(cargo)
        except ValueError:
            return False, f"Cargo inválido: {cargo}."
        senha_hash = generate_password_hash(senha)
        novo_usuario = User(id=id, nome=nome, senha=senha_hash, cargo=cargo)
        db.session.add(novo_usuario)
        db.session.commit()
        return True, "Usuário cadastrado com sucesso."
    
    def visualizar_usuario(self, id):
        usuario = self.get_by_user_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        return True, usuario
 
    def editar_usuario(self, id, nome=None, cargo=None):
        usuario = self.get_by_user_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        if nome:
            usuario.nome = nome
        if cargo:
            try:
                cargo = Role(cargo)
            except ValueError:
                return False, f"Cargo inválido: {cargo}."
            usuario.cargo = cargo
        db.session.commit()
        return True, "Usuário editado com sucesso."    
        
    def deletar_usuario(self, id):
        usuario = self.get_by_user_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        db.session.delete(usuario)
        db.session.commit()
        return True, "Usuário excluído com sucesso."
 
    def alterar_senha(self, id, senha, nova_senha):
        usuario = self.get_by_user_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        if not check_password_hash(usuario.senha, senha):
            return False, "Senha atual incorreta."
        usuario.senha = generate_password_hash(nova_senha)
        db.session.commit()
        return True, "Senha alterada com sucesso."
    
    def mudar_cargo(self, id, cargo):
        usuario = self.get_by_user_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        try:
            cargo = Role(cargo)
        except ValueError:
            return False, f"Cargo inválido: {cargo}."
        usuario.cargo = cargo
        db.session.commit()
        return True, "Cargo alterado com sucesso."
    
    def transferir_posse(self, id_atual, id_novo):
        usuario_atual = self.get_by_user_id(id_atual)
        usuario_novo = self.get_by_user_id(id_novo)
        if not usuario_atual or not usuario_novo:
            return False, "Usuário não encontrado."
        if usuario_atual.cargo != Role.ADMINISTRADOR:
            return False, "Apenas administradores podem transferir posse."
        usuario_atual.cargo = Role.USUARIO
        usuario_novo.cargo = Role.ADMINISTRADOR
        db.session.commit()
        return True, "Posse transferida com sucesso."
    
    def get_by_user_id(self, id):
        return User.query.get(id)