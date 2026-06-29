from models.enums import Role
from models.models import User, db
from models.error_message import UserErrorMessages
from werkzeug.security import generate_password_hash

# ===================================
# CRIAÇÃO DO ADMINISTRADOR PADRÃO
# ===================================
def criar_admin_teste(user_service):
    admin = User(
        nome = "Admin",
        cpf = "27791093197",
        senha = generate_password_hash("Xpto!4321"),
        cargo = Role.ADMINISTRADOR,
        foto_usuario = "caminho/para/foto_admin.jpg"
    )
    db.session.add(admin)
    db.session.commit()
    return admin

# ========================
# TESTES DE CADASTRO
# ========================
def test_cadastrar_usuario_com_sucesso(app, user_service):
    admin = criar_admin_teste(user_service)

    usuario, mensagem = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome = "João Garçom",
        cpf_cadastrado = "54445540110",
        senha_cadastrada = "Senha@2026",
        cargo = Role.GARCOM.value,
        foto_usuario = "caminho/para/foto.jpg"
    )
    assert usuario is not False
    assert usuario.nome == "João Garçom"
    assert usuario.cpf == "54445540110"
    assert usuario.cargo == Role.GARCOM
    assert usuario.foto_usuario == "caminho/para/foto.jpg"
    assert mensagem == "Usuário cadastrado com sucesso."

def test_cadastrar_usuario_campos_invalidos(app, user_service):
    admin = criar_admin_teste(user_service)

    # 1. Teste com cpf inválido
    usuario, mensagem = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        
        nome="João Garçom",
        cpf_cadastrado = "48273948015",  # CPF inválido
        senha_cadastrada = "Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )
    assert usuario is False
    assert mensagem == UserErrorMessages.CPF_INVALIDO
    
    usuario, mensagem = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome="João Garçom",
        cpf_cadastrado="123",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )
    assert usuario is False
    assert mensagem == UserErrorMessages.CPF_INVALIDO

    # 2. Teste com nome inválido
    usuario, mensagem = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome=" ", 
        cpf_cadastrado="54445540110",
        senha_cadastrada="123", 
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )
    assert usuario is False
    assert mensagem == UserErrorMessages.NOME_OBRIGATORIO

    usuario, mensagem = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome="Jo",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )
    assert usuario is False
    assert mensagem == UserErrorMessages.NOME_TAMANHO

    # 3. Teste com senha inválida
    usuario, mensagem = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="123", 
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )
    assert usuario is False
    assert mensagem == UserErrorMessages.SENHA_TAMANHO

    # 4. Teste com cargo inválido
    usuario, mensagem = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome="João", 
        cpf_cadastrado="54445540110", 
        senha_cadastrada="Senha@2026", 
        cargo=" ",
        foto_usuario = "caminho/para/foto.jpg"
    )
    assert usuario is False
    assert mensagem == UserErrorMessages.CARGO_OBRIGATORIO

    # 5. Teste com foto inválida
    usuario, mensagem = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value, 
        foto_usuario= "foto_invalida.txt" * 100  
    )
    assert usuario is False
    assert mensagem == UserErrorMessages.FOTO_INVALIDA

def test_cadastrar_segundo_administrador_nao_permitido(app, user_service):
    admin = criar_admin_teste(user_service)

    # Tenta cadastrar um usuário com cargo de ADMINISTRADOR
    usuario, mensagem = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        nome="Segundo Admin",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.ADMINISTRADOR.value, 
        foto_usuario="caminho/para/foto.jpg"
    )
    assert usuario is False
    assert mensagem == UserErrorMessages.ADMIN_JA_EXISTENTE

def test_usuario_comum_nao_pode_cadastrar_usuario(app, user_service):
    admin = criar_admin_teste(user_service)
    
    garcom, _ = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )

    sucesso, mensagem = user_service.cadastrar_usuario(
        cpf_usuario_logado=garcom.cpf, 
        senha_admin="Senha@2026",
        nome="Invasor",
        cpf_cadastrado="34857493022",
        senha_cadastrada="Senha@2026",
        cargo=Role.COZINHEIRO.value
    )
    assert sucesso is False
    assert mensagem == UserErrorMessages.ACESSO_NEGADO

# ===========================
# TESTES DE AUTENTICAÇÃO
# ===========================
def test_autenticar_login_com_sucesso(app, user_service):
    admin = criar_admin_teste(user_service) 
    
    # Cadastra usando o admin e os parâmetros nomeados corretos
    user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )
    sucesso, mensagem, usuario = user_service.login(cpf="54445540110", senha="Senha@2026")
    
    assert sucesso is True
    assert mensagem == "Login bem-sucedido."
    assert usuario.cpf == "54445540110"

def test_autenticar_login_dados_incorretos(app, user_service):
    admin = criar_admin_teste(user_service)
    user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )
    # Teste com cpf inexistente
    sucesso, mensagem, usuario = user_service.login(cpf="99999999999", senha="Senha@2026")

    assert sucesso is False
    assert mensagem == UserErrorMessages.DADOS_INCORRETOS
    assert usuario is None
        
    # Teste com senha incorreta
    sucesso, mensagem, usuario = user_service.login(cpf="54445540110", senha="senha_errada")

    assert sucesso is False
    assert mensagem == UserErrorMessages.DADOS_INCORRETOS
    assert usuario is None
    
def test_logout_com_sucesso(app, user_service):
    admin = criar_admin_teste(user_service)
    user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )

    sucesso, mensagem = user_service.logout(cpf="54445540110")
    assert sucesso is True
    assert mensagem == "Logout bem-sucedido."

# ====================
# TESTES DE EDIÇÃO
# ====================
def test_editar_usuario_com_sucesso(app, user_service):
    admin = criar_admin_teste(user_service)
    user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )

    # Edita o usuário com sucesso
    sucesso, mensagem = user_service.editar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome="João Editado",
        cpf_atual="54445540110",
        senha="Senha@2027", 
        cargo=Role.COZINHEIRO.value,
        foto_usuario="caminho/para/nova_foto.jpg"
    )    
    usuario_editado = user_service.get_user_by_cpf("54445540110")
    
    assert sucesso is True
    assert mensagem == "Usuário editado com sucesso."
    assert usuario_editado.nome == "João Editado"
    assert usuario_editado.cargo == Role.COZINHEIRO

def test_editar_usuario_campos_invalidos(app, user_service):
    admin = criar_admin_teste(user_service)
    user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )
    
    # Tentar editar com nome 
    sucesso, mensagem = user_service.editar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        cpf_atual="54445540110",
        nome=" ",
    )
    assert sucesso is False
    assert mensagem == UserErrorMessages.NOME_OBRIGATORIO

    # Tentar editar com cpf inválido
    sucesso, mensagem = user_service.editar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        cpf_atual="54445540110",
        novo_cpf="123"  # CPF inválido
    )
    assert sucesso is False
    assert mensagem == UserErrorMessages.CPF_INVALIDO

    #Tentar editar com senha inválida
    sucesso, mensagem = user_service.editar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        cpf_atual="54445540110",
        senha="123"
    )
    assert sucesso is False
    assert mensagem == UserErrorMessages.SENHA_TAMANHO

    # Tentar editar com cargo inválido
    sucesso, mensagem = user_service.editar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        cpf_atual="54445540110",
        cargo=" "
    )
    assert sucesso is False
    assert mensagem == UserErrorMessages.CARGO_OBRIGATORIO

    # Tentar editar com foto inválida
    sucesso, mensagem = user_service.editar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        cpf_atual="54445540110",
        foto_usuario="foto_invalida.txt" * 100
    )
    assert sucesso is False
    assert mensagem == UserErrorMessages.FOTO_INVALIDA

def test_editar_usuario_senha_admin_incorreta(app, user_service):
    admin = criar_admin_teste(user_service)

    user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )

    sucesso, mensagem = user_service.editar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="senha_errada",

        cpf_atual="54445540110",
        nome="João Editado"
    )    
    assert sucesso is False
    assert mensagem == UserErrorMessages.ADMIN_SENHA_INCORRETA

def test_usuario_comum_nao_pode_editar_usuario(app, user_service):
    admin = criar_admin_teste(user_service)
    
    garcom_a, _ = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto1.jpg"
    )

    garcom_b, _ = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome="João Garçom",
        cpf_cadastrado="09427827122",
        senha_cadastrada="Senha@2027",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto2.jpg"
    )
    
    sucesso, mensagem = user_service.editar_usuario(
        cpf_usuario_logado=garcom_a.cpf,
        senha_admin="Senha@2026",

        cpf_atual=garcom_b.cpf,
        nome="Invasor"
    )
    assert sucesso is False
    assert mensagem == UserErrorMessages.ACESSO_NEGADO

def test_editar_usuario_promover_para_admin_nao_permitido(app, user_service):
    admin = criar_admin_teste(user_service)
    
    user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )
    # Tenta promover o garçom a ADMINISTRADOR
    sucesso, mensagem = user_service.editar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        cpf_atual="54445540110",
        cargo=Role.ADMINISTRADOR.value 
    )
    assert sucesso is False
    assert mensagem == UserErrorMessages.ADMIN_JA_EXISTENTE 

def test_editar_proprio_admin_rebaixar_cargo_nao_permitido(app, user_service):
    admin = criar_admin_teste(user_service)

    sucesso, mensagem = user_service.editar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        cpf_atual=admin.cpf,
        cargo=Role.GARCOM.value 
    )
    assert sucesso is False
    assert mensagem == UserErrorMessages.ACESSO_NEGADO

# =====================
# TESTES DE DELEÇÃO
# =====================

def test_deletar_usuario_com_sucesso(app, user_service):
    admin = criar_admin_teste(user_service)

    user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )

    sucesso, mensagem = user_service.deletar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        cpf_alvo="54445540110"
        )
    usuario_apagado = user_service.get_user_by_cpf("54445540110")
    
    assert sucesso is True
    assert usuario_apagado is None 

def test_deletar_usuario_senha_admin_incorreta(app, user_service):
    admin = criar_admin_teste(user_service)
    user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )

    sucesso, mensagem = user_service.deletar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="senha_errada",

        cpf_alvo="54445540110"
    )

    assert sucesso is False
    assert mensagem == UserErrorMessages.ADMIN_SENHA_INCORRETA

def test_usuario_comum_nao_pode_deletar_usuario(app, user_service):
    admin = criar_admin_teste(user_service)
    
    garcom_a, _ = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto1.jpg"
    )

    garcom_b, _ = user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",

        nome="João Garçom",
        cpf_cadastrado="09427827122",
        senha_cadastrada="Senha@2027",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto2.jpg"
    )
    sucesso, mensagem = user_service.deletar_usuario(
        cpf_usuario_logado=garcom_a.cpf,
        senha_admin="Senha@2026",
        cpf_alvo=garcom_b.cpf
    )
    assert sucesso is False
    assert mensagem == UserErrorMessages.ACESSO_NEGADO

def test_admin_tentar_se_autodeletar_nao_permitido(app, user_service):
    admin = criar_admin_teste(user_service)

    sucesso, mensagem = user_service.deletar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        cpf_alvo=admin.cpf 
    )
    assert sucesso is False
    assert mensagem == UserErrorMessages.ADMIN_AUTOEXCLUSAO_NAO_PERMITIDA

# ===================================
# TESTES DE OUTRAS FUNCIONALIDADES
# ===================================
def test_listar_usuarios(app, user_service):
    admin = criar_admin_teste(user_service)
    user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )

    usuarios = user_service.listar_usuarios()
    assert len(usuarios) == 2

def test_visualizar_usuario(app, user_service):
    admin = criar_admin_teste(user_service)
    user_service.cadastrar_usuario(
        cpf_usuario_logado=admin.cpf,
        senha_admin="Xpto!4321",
        nome="João Garçom",
        cpf_cadastrado="54445540110",
        senha_cadastrada="Senha@2026",
        cargo=Role.GARCOM.value,
        foto_usuario="caminho/para/foto.jpg"
    )

    usuario, mensagem = user_service.visualizar_usuario("54445540110")
    assert usuario is not None
    assert usuario["nome"] == "João Garçom"
    assert usuario["cpf"] == "54445540110"
    assert usuario["cargo"] == Role.GARCOM.value
    assert usuario["foto_usuario"] == "caminho/para/foto.jpg"
    assert mensagem == "Usuário encontrado com sucesso."

def test_validar_cpf(app, user_service):
    # Teste com CPF válido
    assert user_service.validar_cpf("54445540110") is True

    # Teste com CPF inválido
    assert user_service.validar_cpf("123") is False
    assert user_service.validar_cpf("4827394801") is False