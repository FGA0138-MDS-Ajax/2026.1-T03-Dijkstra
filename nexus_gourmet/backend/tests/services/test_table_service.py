from models.enums import Role, TableStatus, OrderStatus
from models.models import User, db, Order, Table
from models.error_message import UserErrorMessages, TableErrorMessages
from models.sucess_message import TableSuccessMessages
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

# =========================================
# CRIAÇÃO DE USUÁRIOS PADRÃO PARA TESTES
# =========================================
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

def criar_garcom_teste():
    garcom = User(
        nome = "Garçom",
        cpf = "12345678901",
        senha = generate_password_hash("Senha123!"),
        cargo = Role.GARCOM,
        foto_usuario = "caminho/para/foto_garcom.jpg"
    )
    db.session.add(garcom)
    db.session.commit()
    return garcom

# ===================================
# TESTES DE CRIAÇÃO
# ===================================
def test_criar_mesa_com_sucesso(app, user_service, table_service):
    admin = criar_admin_teste(user_service)

    sucesso, mensagem = table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=4)
    assert sucesso is True
    assert mensagem == TableSuccessMessages.MESA_CRIADA

def test_criar_mesa_com_capacidade_invalida(app, user_service, table_service):
    admin = criar_admin_teste(user_service)

    # Testando capacidade menor que 1
    sucesso, message = table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=0)
    assert sucesso is False
    assert message == TableErrorMessages.CAPACIDADE_INVALIDA
    
    # Testando capacidade maior que 20
    sucesso, message = table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=21)
    assert sucesso is False
    assert message == TableErrorMessages.CAPACIDADE_EXCEDIDA

def test_usuario_comum_nao_pode_criar_mesa(app, user_service, table_service):
    criar_admin_teste(user_service)
    garcom = criar_garcom_teste()

    sucesso, mensagem = table_service.criar_mesa(cpf_usuario_logado=garcom.cpf, capacidade=4)
    assert sucesso is False
    assert mensagem == UserErrorMessages.ACESSO_NEGADO

# ===================================
# TESTES DE EDIÇÃO
# ===================================
def test_editar_mesa_com_sucesso(app, user_service, table_service):
    admin = criar_admin_teste(user_service)
    table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=4)
    
    sucesso, mensagem = table_service.editar_mesa(cpf_usuario_logado=admin.cpf, numero_mesa=1, capacidade=6)
    
    assert sucesso is True
    assert mensagem == TableSuccessMessages.MESA_EDITADA

def test_editar_mesa_com_capacidade_invalida(app, user_service, table_service):
    admin = criar_admin_teste(user_service)
    table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=4)
    
    # Testando capacidade menor que 1
    sucesso, mensagem = table_service.editar_mesa(cpf_usuario_logado=admin.cpf, numero_mesa=1, capacidade=0)
    assert sucesso is False
    assert mensagem == TableErrorMessages.CAPACIDADE_INVALIDA
    
    # Testando capacidade maior que 20
    sucesso, mensagem = table_service.editar_mesa(cpf_usuario_logado=admin.cpf, numero_mesa=1, capacidade=21)
    assert sucesso is False
    assert mensagem == TableErrorMessages.CAPACIDADE_EXCEDIDA

def test_usuario_comum_nao_pode_editar_mesa(app, user_service, table_service):
    admin = criar_admin_teste(user_service)
    garcom = criar_garcom_teste()
    table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=4)

    sucesso, mensagem = table_service.editar_mesa(cpf_usuario_logado=garcom.cpf, numero_mesa=1, capacidade=6)
    assert sucesso is False
    assert mensagem == UserErrorMessages.ACESSO_NEGADO

# ===================================
# TESTES DE DELEÇÃO
# ===================================
def test_deletar_mesa_com_sucesso(app, user_service, table_service):
    admin = criar_admin_teste(user_service)
    table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=4)
    
    sucesso, mensagem = table_service.deletar_mesa(cpf_usuario_logado=admin.cpf, numero_mesa=1)
    
    assert sucesso is True
    assert mensagem == TableSuccessMessages.MESA_DELETADA

def test_usuario_comum_nao_pode_deletar_mesa(app, user_service, table_service):
    admin = criar_admin_teste(user_service)
    garcom = criar_garcom_teste()
    table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=4)

    sucesso, mensagem = table_service.deletar_mesa(cpf_usuario_logado=garcom.cpf, numero_mesa=1)
    assert sucesso is False
    assert mensagem == UserErrorMessages.ACESSO_NEGADO

# ===================================
# TESTES DE LISTAGEM E LIBERAÇÃO
# ===================================
def test_listar_mesas(app, user_service, table_service):
    admin = criar_admin_teste(user_service)
    table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=4) 
    table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=6) 
    
    mesas = table_service.listar_mesas()
    
    assert len(mesas) == 2
    assert mesas[0]['numero'] == 1
    assert mesas[0]['capacidade'] == 4 

def test_listar_comandas_mesa_com_comandas(app, user_service, table_service, order_service):
    admin = criar_admin_teste(user_service)
    table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=4)
    garcom = criar_garcom_teste()
    
    comanda = Order(
        id=1,
        numero_diario=1,
        status=OrderStatus.EM_PREPARO,
        user_cpf=garcom.cpf,
        numero_mesa=1
    )
    db.session.add(comanda)
    db.session.commit()
    
    comandas, _ = table_service.listar_comandas_mesa(mesa_numero=1)
    
    assert len(comandas) == 1
    assert comandas[0]['id'] == 1

def test_listar_comandas_mesa_sem_comandas(app, user_service, table_service):
    admin = criar_admin_teste(user_service)
    table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=4) 
    
    comandas, _ = table_service.listar_comandas_mesa(mesa_numero=1)
    assert comandas == []

def test_liberar_mesa_com_sucesso(app, user_service, table_service):
    admin = criar_admin_teste(user_service)
    table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=4) 
    
    mesa = table_service.get_table_by_number(1)
    mesa.status = TableStatus.OCUPADA
    db.session.commit()
    
    sucesso, mensagem = table_service.liberar_mesa(mesa_numero=1)
    
    assert sucesso is True
    assert mensagem == TableSuccessMessages.MESA_LIBERADA
    assert mesa.status == TableStatus.LIVRE

def test_liberar_mesa_comandas_abertas(app, user_service, table_service):
    admin = criar_admin_teste(user_service)
    table_service.criar_mesa(cpf_usuario_logado=admin.cpf, capacidade=4) 

    mesa = table_service.get_table_by_number(1)
    mesa.status = TableStatus.OCUPADA
    
    comanda_aberta = Order(
        id=1,
        numero_diario=1,
        entrada_cozinha=datetime.now(timezone.utc).replace(tzinfo=None),
        status=OrderStatus.EM_PREPARO,
        user_cpf="12345678901",
        numero_mesa=mesa.numero
    )
    db.session.add(comanda_aberta)
    db.session.commit()
    
    sucesso, mensagem = table_service.liberar_mesa(mesa_numero=1)
    
    assert sucesso is False
    assert mensagem == f"Mesa {mesa.numero} ainda tem comandas em aberto."