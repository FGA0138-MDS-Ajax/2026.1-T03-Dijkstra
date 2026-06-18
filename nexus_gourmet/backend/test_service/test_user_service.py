from models.enums import Role
from models.models import User, db

# ==========================================
# FUNÇÕES AUXILIARES PARA OS TESTES
# ==========================================
def criar_admin_direto():
    """Cria um administrador diretamente no banco, burlando o service."""
    admin = User(id=999, nome="Admin Supremo", senha="123", cargo=Role.ADMINISTRADOR)
    db.session.add(admin)
    db.session.commit()
    return admin

def criar_garcom_direto():
    """Cria um garçom diretamente no banco para testar bloqueios."""
    garcom = User(id=888, nome="Garçom Teste", senha="123", cargo=Role.GARCOM)
    db.session.add(garcom)
    db.session.commit()
    return garcom

# ==========================================
# TESTES DE CADASTRO
# ==========================================
def test_cadastrar_usuario_com_sucesso(app, user_service):
    admin = criar_admin_direto()
    
    usuario, mensagem = user_service.cadastrar_usuario(
        usuario_logado=admin, 
        id=1, 
        nome="João Garçom", 
        senha="123", 
        cargo=Role.GARCOM
    )
    
    assert usuario is not False 
    assert usuario.nome == "João Garçom"
    assert usuario.cargo == Role.GARCOM
    assert mensagem == "Usuário cadastrado com sucesso."

def test_cadastrar_usuario_sem_permissao(app, user_service):
    garcom = criar_garcom_direto()
    
    # Um garçom tenta cadastrar outro usuário
    sucesso, mensagem = user_service.cadastrar_usuario(
        usuario_logado=garcom, 
        id=2, 
        nome="Invasor", 
        senha="123", 
        cargo=Role.COZINHEIRO
    )
    
    assert sucesso is False
    assert mensagem == "Apenas administradores podem cadastrar usuários."

# ==========================================
# TESTES DE AUTENTICAÇÃO
# ==========================================
def test_autenticar_login_com_sucesso(app, user_service):
    admin = criar_admin_direto()
    user_service.cadastrar_usuario(admin, 1, "João Garçom", "123", Role.GARCOM)
    
    sucesso, mensagem, usuario = user_service.autenticar(id=1, senha="123")
    
    assert sucesso is True
    assert mensagem == "Login bem-sucedido."
    assert usuario.id == 1

def test_autenticar_login_senha_incorreta(app, user_service):
    admin = criar_admin_direto()
    user_service.cadastrar_usuario(admin, 1, "João Garçom", "senha_certa", Role.GARCOM)
    
    sucesso, mensagem, usuario = user_service.autenticar(id=1, senha="senha_errada")
    
    assert sucesso is False
    assert mensagem == "Senha incorreta."
    assert usuario is None

def test_logout_com_sucesso(app, user_service):
    admin = criar_admin_direto()
    user_service.cadastrar_usuario(admin, 1, "João Garçom", "123", Role.GARCOM)
    
    sucesso, mensagem = user_service.logout(1)
    assert sucesso is True
    assert mensagem == "Logout bem-sucedido."

# ==========================================
# TESTES DE EDIÇÃO E DELEÇÃO
# ==========================================
def test_editar_usuario_com_sucesso(app, user_service):
    admin = criar_admin_direto()
    user_service.cadastrar_usuario(admin, 1, "João", "123", Role.GARCOM)
    
    sucesso, mensagem = user_service.editar_usuario(
        usuario_logado=admin, 
        id=1, 
        nome="João Editado", 
        cargo=Role.COZINHEIRO
    )
    
    usuario_editado = user_service.get_user_by_id(1)
    
    assert sucesso is True
    assert usuario_editado.nome == "João Editado"
    assert usuario_editado.cargo == Role.COZINHEIRO

def test_editar_usuario_sem_permissao(app, user_service):
    admin = criar_admin_direto()
    garcom = criar_garcom_direto()
    user_service.cadastrar_usuario(admin, 1, "João", "123", Role.GARCOM)
    
    sucesso, mensagem = user_service.editar_usuario(
        usuario_logado=garcom, 
        id=1, 
        nome="Hackeado"
    )
    
    assert sucesso is False
    assert mensagem == "Apenas administradores podem editar usuários."

def test_deletar_usuario_com_sucesso(app, user_service):
    admin = criar_admin_direto()
    user_service.cadastrar_usuario(admin, 1, "João", "123", Role.GARCOM)
    
    sucesso, mensagem = user_service.deletar_usuario(usuario_logado=admin, id=1)
    usuario_apagado = user_service.get_user_by_id(1)
    
    assert sucesso is True
    assert usuario_apagado is None 

def test_deletar_usuario_sem_permissao(app, user_service):
    admin = criar_admin_direto()
    garcom = criar_garcom_direto()
    user_service.cadastrar_usuario(admin, 1, "João", "123", Role.GARCOM)
    
    sucesso, mensagem = user_service.deletar_usuario(usuario_logado=garcom, id=1)
    
    assert sucesso is False
    assert mensagem == "Apenas administradores podem excluir usuários."

# ==========================================
# TESTES DE OUTRAS FUNCIONALIDADES
# ==========================================
def test_listar_usuarios(app, user_service):
    admin = criar_admin_direto()
    user_service.cadastrar_usuario(admin, 1, "João", "123", Role.GARCOM)
    
    usuarios = user_service.listar_usuarios()
    
    assert len(usuarios) == 2 # O admin direto (1) + O João (1)

def test_alterar_senha_com_sucesso(app, user_service):
    admin = criar_admin_direto()
    user_service.cadastrar_usuario(admin, 1, "João", "senha_velha", Role.GARCOM)
    
    sucesso, mensagem = user_service.alterar_senha(1, "senha_velha", "senha_nova")
    assert sucesso is True
    
    login_sucesso, _, _ = user_service.autenticar(1, "senha_nova")
    assert login_sucesso is True

def test_mudar_cargo_com_sucesso(app, user_service):
    admin = criar_admin_direto()
    user_service.cadastrar_usuario(admin, 1, "João", "123", Role.GARCOM)
    
    sucesso, mensagem = user_service.mudar_cargo(usuario_logado=admin, id=1, cargo=Role.COZINHEIRO)
    usuario = user_service.get_user_by_id(1)
    
    assert sucesso is True
    assert usuario.cargo == Role.COZINHEIRO

def test_mudar_cargo_sem_permissao(app, user_service):
    admin = criar_admin_direto()
    garcom = criar_garcom_direto()
    user_service.cadastrar_usuario(admin, 1, "João", "123", Role.GARCOM)
    
    sucesso, mensagem = user_service.mudar_cargo(usuario_logado=garcom, id=1, cargo=Role.ADMINISTRADOR)
    
    assert sucesso is False
    assert mensagem == "Apenas administradores podem alterar cargos."