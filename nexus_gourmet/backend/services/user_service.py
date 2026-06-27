import re
from models.models import db, User
from models.enums import Role
from werkzeug.security import generate_password_hash, check_password_hash
 
class UserService:
    def login(self, cpf, senha):
        usuario = self.get_user_by_cpf(cpf)
        if not usuario:
            return False, "Usuário não encontrado.", None
        
        if not check_password_hash(usuario.senha, senha):
            return False, "Senha incorreta.", None
        
        return True, "Login bem-sucedido.", usuario
    
    def logout(self, cpf):
        usuario = self.get_user_by_cpf(cpf)
        if not usuario:
            return False, "Usuário não encontrado."
        
        return True, "Logout bem-sucedido."
    
    def listar_usuarios(self):
        return User.query.all()
    
    def cadastrar_usuario(self, nome, senha, cargo, cpf=None, foto=None):
        nome = nome.strip() if nome else ""
        senha = senha.strip() if senha else ""
        
        cpf_limpo = re.sub(r'[^0-9]', '', str(cpf)) if cpf else ""

        if not nome:
            return False, "Nome do usuário é obrigatório."
        if not senha:
            return False, "Senha é obrigatória."
        if not cpf_limpo:
            return False, "CPF é obrigatório."
        if not cargo:
            return False, "Cargo é obrigatório."
            
        if not self.validar_cpf(cpf_limpo):
            return False, "O CPF informado é inválido."
            
        if User.query.filter_by(cpf=cpf_limpo).first():
            return False, "Este CPF já está cadastrado no sistema."

        if len(nome) < 3 or len(nome) > 50:
            return False, "O nome deve ter entre 3 e 50 caracteres."
        if len(senha) < 6 or len(senha) > 20:
            return False, "A senha deve ter entre 6 e 20 caracteres."
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome):
            return False, "O nome deve conter apenas letras.}"
        
        # Verifica se a senha tem pelo menos 6 e no máximo 20 caracteres
        if len(senha) < 6 or len(senha) > 20:
            return False, "A senha deve ter entre 6 e 20 caracteres."

        if not re.search(r'[A-Z]', senha):
            return False, "A senha deve conter pelo menos uma letra maiúscula."
        if not re.search(r'[a-z]', senha):
            return False, "A senha deve conter pelo menos uma letra minúscula."
        if not re.search(r'[0-9]', senha):
            return False, "A senha deve conter pelo menos um número."
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
            return False, "A senha deve conter pelo menos um caractere especial."
        
        if foto:
            if hasattr(foto, 'filename') and foto.filename != '':
                nome_arquivo = foto.filename
                
                if '.' in nome_arquivo:
                    extensao = nome_arquivo.rsplit('.', 1)[1].lower()
                    extensoes_permitidas = {'png', 'jpg', 'jpeg'}
                    
                    if extensao not in extensoes_permitidas:
                        return False, "Formato de foto inválido. Use PNG, JPG, JPEG ou WEBP."
                else:
                    return False, "Arquivo de foto sem extensão válida."
            elif isinstance(foto, str):
                if len(foto) > 255:
                    return False, "O caminho ou URL da foto é muito grande."

        try:
            cargo = Role(cargo)
        except ValueError:
            return False, f"Cargo inválido: {cargo}."
            
        senha_hash = generate_password_hash(senha)
        
        novo_usuario = User(cpf=cpf_limpo, nome=nome, senha=senha_hash, cargo=cargo, foto=foto)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return False, "Erro interno ao salvar no banco de dados."
        
        return novo_usuario, "Usuário cadastrado com sucesso."
    
    def visualizar_usuario(self, cpf):
        try:
            cpf = int(cpf)
            usuario = self.get_user_by_cpf(cpf)
        except ValueError:
            usuario = self.get_user_by_cpf(cpf)
            
        if not usuario:
            return None, "Usuário não encontrado."            

        dados_usuario = {
            "cpf": usuario.cpf,
            "nome": usuario.nome,
            "cargo": usuario.cargo.value if usuario.cargo else None
        }        
        dados_usuario["foto"] = usuario.foto

        return dados_usuario, "Usuário encontrado com sucesso."
 
    def editar_usuario(self, cpf_usuario_logado, cpf_atual, nome=None, cargo=None, senha=None, novo_cpf=None, foto=None):
        usuario_logado = self.get_user_by_cpf(cpf_usuario_logado)
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return False, "Acesso negado. Apenas administradores podem editar usuários."
        
        usuario = self.get_user_by_cpf(cpf_atual)
        if not usuario:
            return False, "Usuário não encontrado."
        
        # Validação e edição do Nome
        if nome is not None:
            nome = nome.strip()
            if not nome:
                return False, "O nome não pode ser vazio."
            if len(nome) < 3 or len(nome) > 50:
                return False, "O nome deve ter entre 3 e 50 caracteres."
            if not re.match(r'^[a-zA-Z0-9À-ÿ\s]+$', nome):
                return False, "O nome deve conter apenas letras e números."
            usuario.nome = nome

        # Validação e edição do CPF
        if novo_cpf is not None:
            cpf_limpo = re.sub(r'[^0-9]', '', str(novo_cpf))
            if not cpf_limpo:
                return False, "O CPF não pode ser vazio."
            if not self.validar_cpf(cpf_limpo):
                return False, "O CPF informado é inválido."
            
            # Verifica se o novo CPF já pertence a OUTRO usuário no sistema
            usuario_existente = User.query.filter_by(cpf=cpf_limpo).first()
            if usuario_existente and usuario_existente.cpf != usuario.cpf:
                return False, "Este CPF já está cadastrado para outro usuário."
                
            usuario.cpf = cpf_limpo

        # Validação e edição do Cargo
        if cargo:
            try:
                cargo_role = Role(cargo)
            except ValueError:
                return False, f"Cargo inválido: {cargo}."
            
            # Se alterando para ADMINISTRADOR, transferir posse
            if cargo_role == Role.ADMINISTRADOR and usuario.cargo != Role.ADMINISTRADOR:
                usuario_logado.cargo = Role.USUARIO
            
            usuario.cargo = cargo_role
        
        # Validação e edição da Senha
        if senha is not None:
            senha = senha.strip()
            if not senha:
                return False, "A senha não pode ser vazia."
            if len(senha) < 6 or len(senha) > 20:
                return False, "A senha deve ter entre 6 e 20 caracteres."
            try:
                usuario.senha = generate_password_hash(senha)
            except Exception as e:
                return False, f"Erro ao alterar senha: {str(e)}"
                
        # Edição da Foto
        if foto is not None:
            usuario.foto = foto
        
        db.session.commit()
        return True, "Usuário editado com sucesso."

    def deletar_usuario(self, cpf):
        usuario = self.get_user_by_cpf(cpf)
        if not usuario:
            return False, "Usuário não encontrado."
        db.session.delete(usuario)
        db.session.commit()
        return True, "Usuário excluído com sucesso."
    
    def validar_cpf(self, cpf: str) -> bool:
        cpf = re.sub(r'[^0-9]', '', cpf)  # Remove caracteres não numéricos

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        if cpf in [s * 11 for s in [str(n) for n in range(10)]]:
            return False
        
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10 % 11) % 10
        digito1 = 0 if digito1 == 10 else digito1

        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10
        digito2 = 0 if digito2 == 10 else digito2

        return cpf[-2:] == f"{digito1}{digito2}"

    def get_user_by_cpf(self, cpf):
        return User.query.get(cpf)
