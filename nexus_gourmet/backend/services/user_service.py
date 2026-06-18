from models.models import db, User
from models.enums import Role
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
        if not nome or not nome.strip():
            return False, "Nome do usuário é obrigatório."
        
        if not senha:
            return False, "Senha do usuário é obrigatória."
        
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
 
    def editar_usuario(self, usuario_logado, id, nome=None, cargo=None):
        if usuario_logado.cargo != Role.ADMINISTRADOR:
            return False, "Apenas administradores podem editar usuários."
        
        usuario = self.get_user_by_id(id)

        if not usuario:
            return False, "Usuário não encontrado."
        
        if not nome and not cargo:
            return False, "Nenhum campo fornecido para edição."
        
        if nome:
            if not nome or not nome.strip():
                return False, "Nome do usuário é obrigatório."
            usuario.nome = nome

        if cargo:
            try:
                cargo_role = Role(cargo)
            except ValueError:
                return False, f"Cargo inválido: {cargo}."
            usuario.cargo = cargo_role
            
        db.session.commit()
        return True, "Usuário editado com sucesso."    
        
    def deletar_usuario(self, usuario_logado, id):
        if usuario_logado.cargo != Role.ADMINISTRADOR:
            return False, "Apenas administradores podem excluir usuários."
        
        usuario = self.get_user_by_id(id)

        if not usuario:
            return False, "Usuário não encontrado."
        db.session.delete(usuario)
        db.session.commit()
        return True, "Usuário excluído com sucesso."
 
    def alterar_senha(self, id, senha, nova_senha):
        usuario = self.get_user_by_id(id)
        if not usuario:
            return False, "Usuário não encontrado."
        
        if not check_password_hash(usuario.senha, senha):
            return False, "Senha atual incorreta."
        
        usuario.senha = generate_password_hash(nova_senha)
        db.session.commit()
        return True, "Senha alterada com sucesso."
    
    def get_user_by_id(self, id):
        return db.session.get(User, id)