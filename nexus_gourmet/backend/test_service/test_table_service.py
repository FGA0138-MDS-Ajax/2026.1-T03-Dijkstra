from models.enums import TableStatus
from models.models import Table, db

# ==========================================
# TESTES DE CRIAÇÃO
# ==========================================
def test_criar_mesa_com_sucesso(app, table_service):
    # Agora passamos a 'capacidade' conforme o seu novo service
    sucesso, mensagem = table_service.criar_mesa(numero=1, capacidade=4)
    
    assert sucesso is True
    assert mensagem == "Mesa criada com sucesso."
    
    mesa = table_service.get_table_by_number(1)
    assert mesa is not None
    assert mesa.numero == 1
    assert mesa.capacidade == 4
    assert mesa.status == TableStatus.LIVRE

def test_criar_mesa_numero_duplicado(app, table_service):
    table_service.criar_mesa(numero=1, capacidade=4)
    
    sucesso, mensagem = table_service.criar_mesa(numero=1, capacidade=6)
    
    assert sucesso is False
    assert mensagem == "Número de mesa já existe."

# ==========================================
# TESTES DE EDIÇÃO
# ==========================================
def test_editar_mesa_com_sucesso(app, table_service):
    table_service.criar_mesa(numero=1, capacidade=4)
    
    sucesso, mensagem = table_service.editar_mesa(numero_mesa=1, numero=2, capacidade=6)
    
    assert sucesso is True
    assert mensagem == "Mesa editada com sucesso."
    
    mesa_editada = table_service.get_table_by_number(2)
    assert mesa_editada.numero == 2
    assert mesa_editada.capacidade == 6

def test_editar_mesa_inexistente(app, table_service):
    sucesso, mensagem = table_service.editar_mesa(numero_mesa=99, capacidade=4)
    
    assert sucesso is False
    assert mensagem == "Mesa não encontrada."

def test_editar_mesa_para_numero_existente(app, table_service):
    table_service.criar_mesa(numero=1, capacidade=4)
    table_service.criar_mesa(numero=2, capacidade=4)
    
    # Tenta mudar a mesa 1 para o número 2, que já existe
    sucesso, mensagem = table_service.editar_mesa(numero_mesa=1, numero=2)
    
    assert sucesso is False
    assert mensagem == "Número de mesa já existe."

# ==========================================
# TESTES DE DELEÇÃO
# ==========================================
def test_deletar_mesa_com_sucesso(app, table_service):
    table_service.criar_mesa(numero=1, capacidade=4)
    
    sucesso, mensagem = table_service.deletar_mesa(numero_mesa=1)
    
    assert sucesso is True
    assert mensagem == "Mesa deletada com sucesso."
    assert table_service.get_table_by_number(1) is None

def test_deletar_mesa_inexistente(app, table_service):
    sucesso, mensagem = table_service.deletar_mesa(numero_mesa=99)
    
    assert sucesso is False
    assert mensagem == "Mesa não encontrada."

# ==========================================
# TESTES DE LISTAGEM E LIBERAÇÃO
# ==========================================
def test_listar_mesas(app, table_service):
    table_service.criar_mesa(numero=1, capacidade=4)
    table_service.criar_mesa(numero=2, capacidade=6)
    
    mesas = table_service.listar_mesas()
    
    assert len(mesas) == 2
    assert mesas[0]['numero'] == 1
    # O seu service formata a capacidade como "{len(comandas)}/{capacidade}"
    assert mesas[0]['capacidade'] == "0/4" 

def test_listar_comandas_mesa_sem_comandas(app, table_service):
    table_service.criar_mesa(numero=1, capacidade=4)
    
    comandas, mensagem = table_service.listar_comandas_mesa(mesa_numero=1)
    
    assert comandas == []
    assert mensagem == "Comandas listadas com sucesso."

def test_listar_comandas_mesa_inexistente(app, table_service):
    comandas, mensagem = table_service.listar_comandas_mesa(mesa_numero=99)
    
    assert comandas is None
    assert mensagem == "Mesa não encontrada."

def test_liberar_mesa_com_sucesso(app, table_service):
    table_service.criar_mesa(numero=1, capacidade=4)
    
    # Vamos forçar a mesa a ficar ocupada para testar a liberação
    mesa = table_service.get_table_by_number(1)
    mesa.status = TableStatus.OCUPADA
    db.session.commit()
    
    sucesso, mensagem = table_service.liberar_mesa(mesa_numero=1)
    
    assert sucesso is True
    assert mensagem == "Mesa 1 liberada."
    assert mesa.status == TableStatus.LIVRE