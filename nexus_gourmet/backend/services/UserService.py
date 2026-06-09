from models import db, Usuario
from enums import PerfilUsuario
from werkzeug.security import generate_password_hash, check_password_hash
 
 
class UsuarioService:
 
    def get_usuario_by_id(self, usuario_id):
        return Usuario.query.get(usuario_id)
 
    def get_usuario_by_login(self, login):
        return Usuario.query.filter_by(login=login).first()
 
    def listar_usuarios(self):
        return Usuario.query.all()
 
    def autenticar(self, login, senha):
        usuario = self.get_usuario_by_login(login)
        if not usuario or not check_password_hash(usuario.senha, senha):
            return None, "Login ou senha incorretos."
        return usuario, "Login realizado com sucesso."
 
    def cadastrar_usuario(self, nome, login, senha, perfil_str):
        if self.get_usuario_by_login(login):
            return False, "Login já está em uso."
        try:
            perfil = PerfilUsuario(perfil_str)
        except ValueError:
            return False, f"Perfil inválido: {perfil_str}."
 
        usuario = Usuario(
            nome=nome,
            login=login,
            senha=generate_password_hash(senha),
            perfil=perfil
        )
        db.session.add(usuario)
        db.session.commit()
        return True, "Usuário cadastrado com sucesso."
 
    def editar_usuario(self, usuario_id, nome, login, perfil_str):
        usuario = self.get_usuario_by_id(usuario_id)
        if not usuario:
            return False, "Usuário não encontrado."
        try:
            perfil = PerfilUsuario(perfil_str)
        except ValueError:
            return False, f"Perfil inválido: {perfil_str}."
 
        usuario.nome = nome
        usuario.login = login
        usuario.perfil = perfil
        db.session.commit()
        return True, "Usuário atualizado com sucesso."
 
    def deletar_usuario(self, usuario_id):
        usuario = self.get_usuario_by_id(usuario_id)
        if not usuario:
            return False, "Usuário não encontrado."
        db.session.delete(usuario)
        db.session.commit()
        return True, "Usuário excluído com sucesso."
 
    def alterar_senha(self, usuario_id, senha_atual, nova_senha):
        usuario = self.get_usuario_by_id(usuario_id)
        if not usuario:
            return False, "Usuário não encontrado."
        if not check_password_hash(usuario.senha, senha_atual):
            return False, "Senha atual incorreta."
        usuario.senha = generate_password_hash(nova_senha)
        db.session.commit()
        return True, "Senha alterada com sucesso."
 
