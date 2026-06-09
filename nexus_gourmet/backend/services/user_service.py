from models import db, User
from enums import Role
from werkzeug.security import generate_password_hash, check_password_hash
 
 
class UsuarioService:
 
    def get_usuario_by_id(self, id):
        return User.query.get(id)
 
    def listar_usuarios(self):
        return User.query.all()
 
    def autenticar(self, id, senha):
        usuario = self.get_usuario_by_id(id)
        if not usuario or not check_password_hash(usuario.senha, senha):
            return None, "Login ou senha incorretos."
        return usuario, "Login realizado com sucesso."
 
    def cadastrar_usuario(self, nome, id, senha, cargo):
        if self.get_usuario_by_id(id):
            return False, "Login já está em uso."
        try:
            cargo = Role(cargo)
        except ValueError:
            return False, f"Cargo inválido: {cargo}."
 
        usuario = User(
            nome=nome,
            id=id,
            senha=generate_password_hash(senha),
            cargo=cargo
        )
        db.session.add(usuario)
        db.session.commit()
        return True, "Usuário cadastrado com sucesso."
 
    def editar_usuario(self, nome, id, cargo):
        usuario = self.get_usuario_by_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        try:
            cargo = Role(cargo)
        except ValueError:
            return False, f"Cargo inválido: {cargo}."
 
        usuario.nome = nome
        usuario.id = id
        usuario.cargo = cargo
        db.session.commit()
        return True, "Usuário atualizado com sucesso."
 
    def deletar_usuario(self, id):
        usuario = self.get_usuario_by_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        db.session.delete(usuario)
        db.session.commit()
        return True, "Usuário excluído com sucesso."
 
    def alterar_senha(self, id, senha_atual, nova_senha):
        usuario = self.get_usuario_by_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        if not check_password_hash(usuario.senha, senha_atual):
            return False, "Senha atual incorreta."
        usuario.senha = generate_password_hash(nova_senha)
        db.session.commit()
        return True, "Senha alterada com sucesso."
 
