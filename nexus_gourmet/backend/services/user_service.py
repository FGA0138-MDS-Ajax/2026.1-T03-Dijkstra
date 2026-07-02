import os
import uuid
import re
from flask import current_app
from werkzeug.utils import secure_filename
from backend.models.models import db, User
from backend.models.enums import Role
from backend.models.error_message import UserErrorMessages
from backend.models.sucess_message import UserSuccessMessages
from werkzeug.security import generate_password_hash, check_password_hash
 
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
    
    def listar_usuarios(self):
        return User.query.all()
    
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
        
        # Validações e salvamento da foto do usuário
        foto_url = None
        if foto_usuario is not None:
            if hasattr(foto_usuario, 'filename') and foto_usuario.filename != '':
                extensao = foto_usuario.filename.rsplit('.', 1)[-1].lower()
                extensoes_permitidas = {'png', 'jpg', 'jpeg', 'webp'}
                
                if extensao not in extensoes_permitidas:
                    return False, UserErrorMessages.FOTO_FORMATO_INVALIDO
                
                novo_nome = f"{uuid.uuid4().hex}.{extensao}"
                caminho_pasta = os.path.join(current_app.config['UPLOAD_FOLDER'], 'usuarios')
                caminho = os.path.join(caminho_pasta, novo_nome)
                foto_usuario.save(caminho)
                foto_url = f"/static/uploads/usuarios/{novo_nome}"
            
            elif isinstance(foto_usuario, str) and foto_usuario.strip():
                if len(foto_usuario) > 255:
                    return False, UserErrorMessages.FOTO_INVALIDA
                foto_url = foto_usuario.strip()

        senha_hash = generate_password_hash(senha_cadastrada)
        novo_usuario = User(nome=nome, cpf=cpf_limpo, senha=senha_hash, cargo=cargo, foto_usuario=foto_url)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao salvar no banco de dados: {str(e)}"
        
        return novo_usuario, UserSuccessMessages.USUARIO_CADASTRADO        
    
    def visualizar_usuario(self, cpf):
        usuario = self.get_user_by_cpf(cpf)
        if not usuario:
            return None, UserErrorMessages.USUARIO_NAO_ENCONTRADO

        dados_usuario = {
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "cargo": usuario.cargo.value
        }        
        dados_usuario["foto_usuario"] = usuario.foto_usuario

        return dados_usuario, UserSuccessMessages.USUARIO_ENCONTRADO
 
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
            
            usuario_existente = User.query.filter_by(cpf=cpf_limpo).first()
            if usuario_existente and usuario_existente.cpf != usuario.cpf:
                return False, UserErrorMessages.CPF_DUPLICADO
                
            usuario.cpf = cpf_limpo
        
        # Validação e edição da Senha
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

        # Validação e edição do Cargo
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
            if hasattr(foto_usuario, 'filename') and foto_usuario.filename != '':
                extensao = foto_usuario.filename.rsplit('.', 1)[-1].lower()
                extensoes_permitidas = {'png', 'jpg', 'jpeg', 'webp'}
                
                if extensao not in extensoes_permitidas:
                    return False, UserErrorMessages.FOTO_FORMATO_INVALIDO
                
                novo_nome = f"{uuid.uuid4().hex}.{extensao}"
                caminho_pasta = os.path.join(current_app.config['UPLOAD_FOLDER'], 'usuarios')
                caminho = os.path.join(caminho_pasta, novo_nome)
                foto_usuario.save(caminho)
                usuario.foto_usuario = f"/static/uploads/usuarios/{novo_nome}"
            
            elif isinstance(foto_usuario, str) and foto_usuario.strip():
                if len(foto_usuario.strip()) > 255:
                    return False, UserErrorMessages.FOTO_INVALIDA  
                usuario.foto_usuario = foto_usuario.strip()
        
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
        db.session.commit()
        return True, UserSuccessMessages.USUARIO_EXCLUIDO
    
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