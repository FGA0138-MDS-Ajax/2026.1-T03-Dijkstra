from flask import session
from backend.models.models import db, User
from backend.models.enums import Role
from werkzeug.security import generate_password_hash, check_password_hash
 
class UserService:
    def autenticar(self, id, senha):
        usuario = self.get_user_by_id(id)
        if not usuario:
            return False, "Usuário não encontrado.", None
        
        if not check_password_hash(usuario.senha, senha):
            return False, "Senha incorreta.", None
        
        return True, "Login bem-sucedido.", usuario
    
    def logout(self, id):
        usuario = self.get_user_by_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        
        return True, "Logout bem-sucedido."
    
    def listar_usuarios(self):
        return User.query.all()
    
    def cadastrar_usuario(self, nome, senha, cargo):
        
        novo_id = 1
        while self.get_user_by_id(novo_id) is not None:
            novo_id += 1

        if self.get_user_by_id(novo_id):
            return False, "ID de usuário já existe."
        
        try:
            cargo = Role(cargo)
        except ValueError:
            return False, f"Cargo inválido: {cargo}."
        
        senha_hash = generate_password_hash(senha)
        novo_usuario = User(id=novo_id, nome=nome, senha=senha_hash, cargo=cargo)
        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario, "Usuário cadastrado com sucesso."
    
    def visualizar_usuario(self, id):
        usuario = self.get_user_by_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        return True, usuario
 
    def editar_usuario(self, id_usuario_logado, id, nome=None, cargo=None, senha=None):
        usuario_logado = self.get_user_by_id(id_usuario_logado)
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return False, "Acesso negado. Apenas administradores podem editar usuários."
        
        usuario = self.get_user_by_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        
        if nome:
            usuario.nome = nome

        if cargo:
            try:
                cargo_role = Role(cargo)
            except ValueError:
                return False, f"Cargo inválido: {cargo}."
            
            # Se alterando para ADMINISTRADOR, transferir posse
            if cargo_role == Role.ADMINISTRADOR and usuario.cargo != Role.ADMINISTRADOR:
                usuario_logado.cargo = Role.USUARIO
            
            usuario.cargo = cargo_role
        
        if senha:
            try:
                usuario.senha = generate_password_hash(senha)
            except Exception as e:
                return False, f"Erro ao alterar senha: {str(e)}"
        
        db.session.commit()
        return True, "Usuário editado com sucesso."

    def deletar_usuario(self, id):
        usuario = self.get_user_by_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        db.session.delete(usuario)
        db.session.commit()
        return True, "Usuário excluído com sucesso."
    
    def get_user_by_id(self, id):
        return User.query.get(id)