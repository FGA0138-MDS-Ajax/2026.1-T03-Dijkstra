<<<<<<< HEAD

import re
from models.models import db, User
from models.enums import Role
from models.error_message import UserErrorMessages
from models.sucess_message import UserSuccessMessages
=======
from models import db, User
from enums import Role
>>>>>>> developer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
 
<<<<<<< HEAD
class UserService:
    def login(self, cpf, senha):
        usuario = self.get_user_by_cpf(cpf)

        if not usuario or not check_password_hash(usuario.senha, senha):
            return False, UserErrorMessages.DADOS_INCORRETOS, None
        
        return True, UserSuccessMessages.LOGIN_BEM_SUCEDIDO, usuario
    
    def logout(self, cpf):
        usuario = self.get_user_by_cpf(cpf)
        if not usuario:
            return False, UserErrorMessages.USUARIO_NAO_ENCONTRADO
        
        return True, UserSuccessMessages.LOGOUT_BEM_SUCEDIDO
=======
 
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
>>>>>>> developer
    
    def listar_usuarios(self):
        return User.query.all()
    
<<<<<<< HEAD
    def cadastrar_usuario(self, cpf_usuario_logado=None, senha_admin=None, nome=None, cpf_cadastrado=None, senha_cadastrada=None, cargo=None, foto_usuario=None):
        usuario_logado = self.get_user_by_cpf(cpf_usuario_logado)
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return False, UserErrorMessages.ACESSO_NEGADO
        
        if not senha_admin or not check_password_hash(usuario_logado.senha, senha_admin):
            return False, UserErrorMessages.ADMIN_SENHA_INCORRETA
        
        # Validações do Nome
        nome = nome.strip() if nome else ""

        if not nome:
            return False, UserErrorMessages.NOME_OBRIGATORIO

        if len(nome) < 3 or len(nome) > 50:
            return False, UserErrorMessages.NOME_TAMANHO
        
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome):
            return False, UserErrorMessages.NOME_INVALIDO
                
        # Validações do CPF
        cpf_cadastrado = str(cpf_cadastrado).strip() if cpf_cadastrado else ""
        cpf_limpo = re.sub(r'[^0-9]', '', str(cpf_cadastrado)) if cpf_cadastrado else ""

        if not cpf_limpo:
            return False, UserErrorMessages.CPF_OBRIGATORIO
        
        if not self.validar_cpf(cpf_limpo):
            return False, UserErrorMessages.CPF_INVALIDO
            
        if User.query.filter_by(cpf=cpf_limpo).first():
            return False, UserErrorMessages.CPF_DUPLICADO
        
        # Validações da senha
        senha_cadastrada = senha_cadastrada.strip() if senha_cadastrada else ""

        if not senha_cadastrada:
            return False, UserErrorMessages.SENHA_OBRIGATORIA
        
        if len(senha_cadastrada) < 6 or len(senha_cadastrada) > 20:
            return False, UserErrorMessages.SENHA_TAMANHO

        if not re.search(r'[A-Z]', senha_cadastrada):
            return False, UserErrorMessages.SENHA_LETRA_MAISCUULA
        
        if not re.search(r'[a-z]', senha_cadastrada):
            return False, UserErrorMessages.SENHA_LETRA_MINUSCULA
        
        if not re.search(r'[0-9]', senha_cadastrada):
            return False, UserErrorMessages.SENHA_NUMERO
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_cadastrada):
            return False, UserErrorMessages.SENHA_CARACTERE_ESPECIAL
        
        # Validações do cargo
        cargo = cargo.strip() if cargo else ""

        if not cargo:
            return False, UserErrorMessages.CARGO_OBRIGATORIO
        try:
            cargo = Role(cargo)
        except ValueError:
            return False, UserErrorMessages.CARGO_INVALIDO
        
        if cargo == Role.ADMINISTRADOR:
            return False, UserErrorMessages.ADMIN_JA_EXISTENTE
        
        # Validações da foto do usuário
        foto_usuario = foto_usuario.strip() if isinstance(foto_usuario, str) else foto_usuario
        
        if foto_usuario:
            if hasattr(foto_usuario, 'filename') and foto_usuario.filename != '':
                nome_arquivo = foto_usuario.filename
                
                if '.' in nome_arquivo:
                    extensao = nome_arquivo.rsplit('.', 1)[1].lower()
                    extensoes_permitidas = {'png', 'jpg', 'jpeg'}
                    
                    if extensao not in extensoes_permitidas:
                        return False, UserErrorMessages.FOTO_FORMATO_INVALIDO
                else:
                    return False, UserErrorMessages.FOTO_FORMATO_INVALIDO
            
            elif isinstance(foto_usuario, str):
                if len(foto_usuario) > 255:
                    return False, UserErrorMessages.FOTO_INVALIDA

  
        senha_hash = generate_password_hash(senha_cadastrada)
        novo_usuario = User(nome=nome, cpf=cpf_limpo, senha=senha_hash, cargo=cargo, foto_usuario=foto_usuario)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao salvar no banco de dados: {str(e)}"
        
        return novo_usuario, UserSuccessMessages.USUARIO_CADASTRADO        
    
    def visualizar_usuario(self, cpf):
        usuario = self.get_user_by_cpf(cpf)
=======
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
>>>>>>> developer
        if not usuario:
            return None, UserErrorMessages.USUARIO_NAO_ENCONTRADO

        dados_usuario = {
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "cargo": usuario.cargo.value
        }        
        dados_usuario["foto_usuario"] = usuario.foto_usuario

        return dados_usuario, UserSuccessMessages.USUARIO_ENCONTRADO
 
<<<<<<< HEAD
    def editar_usuario(self, cpf_usuario_logado, senha_admin, nome=None, cpf_atual=None, cargo=None, senha=None, novo_cpf=None, foto_usuario=None):
        usuario_logado = self.get_user_by_cpf(cpf_usuario_logado)
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return False, UserErrorMessages.ACESSO_NEGADO
                
        # Validação da senha do Administrador logado
        if not senha_admin or not check_password_hash(usuario_logado.senha, senha_admin):
            return False, UserErrorMessages.ADMIN_SENHA_INCORRETA
            
        usuario = self.get_user_by_cpf(cpf_atual)
        if not usuario:
            return False, UserErrorMessages.USUARIO_NAO_ENCONTRADO
        
        # Validação e edição do Nome
        if nome is not None:
            nome = nome.strip()
            if not nome:
                return False, UserErrorMessages.NOME_OBRIGATORIO
            if len(nome) < 3 or len(nome) > 50:
                return False, UserErrorMessages.NOME_TAMANHO
            if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome):
                return False, UserErrorMessages.NOME_INVALIDO
            usuario.nome = nome

        # Validação e edição do CPF
        if novo_cpf is not None:
            cpf_limpo = re.sub(r'[^0-9]', '', str(novo_cpf))
            if not cpf_limpo:
                return False, UserErrorMessages.CPF_OBRIGATORIO
            if not self.validar_cpf(cpf_limpo):
                return False, UserErrorMessages.CPF_INVALIDO
            
            # Verifica se o novo CPF já pertence a OUTRO usuário no sistema
            usuario_existente = User.query.filter_by(cpf=cpf_limpo).first()
            if usuario_existente and usuario_existente.cpf != usuario.cpf:
                return False, UserErrorMessages.CPF_DUPLICADO
                
            usuario.cpf = cpf_limpo
        
        # Validação e edição da Senha do usuário que está sendo editado
        if senha is not None:
            senha = senha.strip()
            if not senha:
                return False, UserErrorMessages.SENHA_OBRIGATORIA
            if len(senha) < 6 or len(senha) > 20:
                return False, UserErrorMessages.SENHA_TAMANHO
            
            if not re.search(r'[A-Z]', senha):           
                return False, UserErrorMessages.SENHA_LETRA_MAISCUULA

            if not re.search(r'[a-z]', senha):           
                return False, UserErrorMessages.SENHA_LETRA_MINUSCULA

            if not re.search(r'[0-9]', senha):           
                return False, UserErrorMessages.SENHA_NUMERO

            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
                return False, UserErrorMessages.SENHA_CARACTERE_ESPECIAL

            usuario.senha = generate_password_hash(senha)

        # Validação e edição do Cargo (CORRIGIDO)
        if cargo is not None:
            cargo = cargo.strip() if isinstance(cargo, str) else cargo

            if not cargo:
                return False, UserErrorMessages.CARGO_OBRIGATORIO            
            try:
                novo_cargo = Role(cargo) 
            except ValueError:
                return False, UserErrorMessages.CARGO_INVALIDO
                
            if usuario.cargo == Role.ADMINISTRADOR and novo_cargo != Role.ADMINISTRADOR:
                return False, UserErrorMessages.ACESSO_NEGADO
            
            if usuario.cargo != Role.ADMINISTRADOR and novo_cargo == Role.ADMINISTRADOR:
                return False, UserErrorMessages.ADMIN_JA_EXISTENTE
            
            usuario.cargo = novo_cargo
            
        # Validação e edição da foto do usuário
        if foto_usuario is not None:
            foto_usuario = foto_usuario.strip() if isinstance(foto_usuario, str) else foto_usuario
            
            if foto_usuario:
                if hasattr(foto_usuario, 'filename') and foto_usuario.filename != '':
                    nome_arquivo = foto_usuario.filename
                    
                    if '.' in nome_arquivo:
                        extensao = nome_arquivo.rsplit('.', 1)[1].lower()
                        extensoes_permitidas = {'png', 'jpg', 'jpeg'}
                        
                        if extensao not in extensoes_permitidas:
                            return False, UserErrorMessages.FOTO_FORMATO_INVALIDO
                    else:
                        return False, UserErrorMessages.FOTO_FORMATO_INVALIDO
                
                elif isinstance(foto_usuario, str):
                    if len(foto_usuario) > 255:
                        return False, UserErrorMessages.FOTO_INVALIDA  
            usuario.foto_usuario = foto_usuario
        
        db.session.commit()
        return True, UserSuccessMessages.USUARIO_EDITADO

    def deletar_usuario(self, cpf_usuario_logado, senha_admin, cpf_alvo):
        usuario_logado = self.get_user_by_cpf(cpf_usuario_logado)
        if not usuario_logado or usuario_logado.cargo != Role.ADMINISTRADOR:
            return False, UserErrorMessages.ACESSO_NEGADO
            
        # Validação da senha do Administrador logado
        if not senha_admin or not check_password_hash(usuario_logado.senha, senha_admin):
            return False, UserErrorMessages.ADMIN_SENHA_INCORRETA

        usuario_alvo = self.get_user_by_cpf(cpf_alvo)
        if not usuario_alvo:
            return False, UserErrorMessages.USUARIO_NAO_ENCONTRADO
            
        # Evita que o admin delete a si próprio por engano através desta rota comum
        if usuario_logado.cpf == usuario_alvo.cpf:
            return False, UserErrorMessages.ADMIN_AUTOEXCLUSAO_NAO_PERMITIDA

        db.session.delete(usuario_alvo)
=======
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
>>>>>>> developer
        db.session.commit()
        return True, UserSuccessMessages.USUARIO_EXCLUIDO
    
<<<<<<< HEAD
    def validar_cpf(self, cpf: str) -> bool:
        cpf = re.sub(r'[^0-9]', '', cpf) 

        if len(cpf) != 11:
            return False
        
        if cpf == cpf[0] * 11:
            return False
        
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        return cpf[-2:] == f"{digito1}{digito2}"

    def get_user_by_cpf(self, cpf):
        cpf_limpo = re.sub(r'[^0-9]', '', str(cpf)) if cpf else ""

        return User.query.filter_by(cpf=cpf_limpo).first()
=======
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
>>>>>>> developer
