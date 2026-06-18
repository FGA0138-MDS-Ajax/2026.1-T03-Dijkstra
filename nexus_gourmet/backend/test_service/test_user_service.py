from models.enums import Role
from models.models import User, db

# ==========================================
# TESTES DE CADASTRO
# ==========================================
def test_cadastrar_usuario_com_sucesso(app, user_service):
    # Não enviamos mais o ID nem o usuario_logado!
    usuario, mensagem = user_service.cadastrar_usuario(
        nome="João Garçom", 
        senha="123", 
        cargo=Role.GARCOM.value
    )
    
    assert usuario is not False 
    assert usuario.nome == "João Garçom"
    assert usuario.cargo == Role.GARCOM
    assert mensagem == "Usuário cadastrado com sucesso."
    assert usuario.id == 1 # O banco gerou o 1 automaticamente!

def test_cadastrar_usuario_campos_invalidos(app, user_service):
    # 1. Teste com nome vazio
    usuario, mensagem = user_service.cadastrar_usuario(
        nome="   ", 
        senha="123", 
        cargo=Role.GARCOM.value
    )
    assert usuario is False
    assert "Nome" in mensagem

    # 2. Teste com cargo inválido
    usuario, mensagem = user_service.cadastrar_usuario(
        nome="João", 
        senha="123", 
        cargo="Cargo Inexistente"
    )
    assert usuario is False
    assert "Cargo inválido" in mensagem

# ==========================================
# TESTES DE AUTENTICAÇÃO
# ==========================================
def test_autenticar_login_com_sucesso(app, user_service):
    user_service.cadastrar_usuario("João Garçom", "123", Role.GARCOM.value)
    
    sucesso, mensagem, usuario = user_service.autenticar(id=1, senha="123")
    
    assert sucesso is True
    assert mensagem == "Login bem-sucedido."
    assert usuario.id == 1

def test_autenticar_login_dados_incorretos(app, user_service):
    user_service.cadastrar_usuario("João Garçom", "123", Role.GARCOM.value)
    
    # Teste com senha incorreta
    sucesso, mensagem, usuario = user_service.autenticar(id=1, senha="senha_errada")
    assert sucesso is False
    assert mensagem == "Senha incorreta."
    assert usuario is None

    # Teste com ID inexistente
    sucesso, mensagem, usuario = user_service.autenticar(id=99, senha="123")
    assert sucesso is False
    assert mensagem == "Usuário não encontrado."
    assert usuario is None
    
def test_logout_com_sucesso(app, user_service):
    user_service.cadastrar_usuario("João Garçom", "123", Role.GARCOM.value)
    
    sucesso, mensagem = user_service.logout(id=1)
    assert sucesso is True
    assert mensagem == "Logout bem-sucedido."

# ==========================================
# TESTES DE EDIÇÃO E DELEÇÃO
# ==========================================
def test_editar_usuario_com_sucesso(app, user_service):
    admin = user_service.cadastrar_usuario("Admin", "123", Role.ADMINISTRADOR.value)[0]
    user_service.cadastrar_usuario("João", "123", Role.GARCOM.value)
    
    # Edita o João (que recebeu o ID 1 automaticamente)
    sucesso, mensagem = user_service.editar_usuario(
        admin, id=1, 

        nome="João Editado", 
        cargo=Role.COZINHEIRO.value
    )
    
    usuario_editado = user_service.get_user_by_id(1)
    
    assert sucesso is True
    assert mensagem == "Usuário editado com sucesso."
    assert usuario_editado.nome == "João Editado"
    assert usuario_editado.cargo == Role.COZINHEIRO

def test_editar_usuario_campos_invalidos(app, user_service):
    admin = user_service.cadastrar_usuario("Admin", "123", Role.ADMINISTRADOR.value)[0]
    user_service.cadastrar_usuario("João", "123", Role.GARCOM.value)
    
    # Tenta editar com nome vazio
    sucesso, mensagem = user_service.editar_usuario(
        admin, id=1, nome="   "
    )
    assert sucesso is False
    assert "Nome" in mensagem

    # Tenta editar com cargo inválido
    sucesso, mensagem = user_service.editar_usuario(
        admin, id=1, cargo="Cargo Inexistente"
    )
    assert sucesso is False
    assert "Cargo inválido" in mensagem

def test_deletar_usuario_com_sucesso(app, user_service):
    admin = user_service.cadastrar_usuario("Admin", "123", Role.ADMINISTRADOR.value)[0]
    user_service.cadastrar_usuario("João", "123", Role.GARCOM.value)
    
    sucesso, mensagem = user_service.deletar_usuario(admin, id=1)
    usuario_apagado = user_service.get_user_by_id(1)
    
    assert sucesso is True
    assert usuario_apagado is None 

# ==========================================
# TESTES DE OUTRAS FUNCIONALIDADES
# ==========================================
def test_listar_usuarios(app, user_service):
    user_service.cadastrar_usuario("Admin", "123", Role.ADMINISTRADOR.value) # Recebe ID 1
    user_service.cadastrar_usuario("João", "123", Role.GARCOM.value)         # Recebe ID 2
    
    usuarios = user_service.listar_usuarios()
    assert len(usuarios) == 2

def test_alterar_senha_com_sucesso(app, user_service):
    user_service.cadastrar_usuario("João", "senha_velha", Role.GARCOM.value)
    
    sucesso, mensagem = user_service.alterar_senha(id=1, senha="senha_velha", nova_senha="senha_nova")
    assert sucesso is True
    
    login_sucesso, _, _ = user_service.autenticar(id=1, senha="senha_nova")
    assert login_sucesso is True