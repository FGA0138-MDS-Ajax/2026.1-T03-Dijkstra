import pytest

def simular_sessao(client, cpf):
    with client.session_transaction() as sess:
        sess['user_cpf'] = cpf

def test_listar_mesas_garcom(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    mesa = dados_iniciais["mesa"]
    simular_sessao(client, garcom.cpf)
    
    response = client.get('/api/salao')
    
    assert response.status_code == 200
    dados = response.get_json()
    assert dados["success"] is True
    assert len(dados["data"]) >= 1
    assert dados["data"][0]["numero"] == mesa.numero

def test_criar_mesa_admin_sucesso(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    simular_sessao(client, admin.cpf)
    
    response = client.post('/api/salao/criar_mesa', json={
        "capacidade": 4
    })
    
    assert response.status_code == 200
    dados = response.get_json()
    assert dados["success"] is True

def test_criar_mesa_garcom_acesso_negado(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    simular_sessao(client, garcom.cpf)
    
    response = client.post('/api/salao/criar_mesa', json={
        "capacidade": 4
    })
    
    assert response.status_code == 403
    dados = response.get_json()
    assert dados["success"] is False
    assert "Acesso negado" in dados["message"]

def test_editar_mesa_admin_sucesso(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    mesa = dados_iniciais["mesa"]
    simular_sessao(client, admin.cpf)
    
    response = client.put(f'/api/salao/editar_mesa/{mesa.numero}', json={"capacidade": 6})
    assert response.status_code == 200
    assert response.get_json()["success"] is True

def test_deletar_mesa_com_comanda_ativa_deve_falhar(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    garcom = dados_iniciais["garcom"]
    mesa = dados_iniciais["mesa"]
    
    # 1. Abre uma comanda na mesa pelo garçom
    simular_sessao(client, garcom.cpf)
    client.post(f'/api/salao/{mesa.numero}/comandas/abrir_comanda')
    
    # 2. Admin tenta deletar a mesa ocupada
    simular_sessao(client, admin.cpf)
    response = client.delete(f'/api/salao/deletar_mesa/{mesa.numero}')
    
    assert response.status_code == 400
    assert response.get_json()["success"] is False

def test_tolerancia_dados_invalidos_capacidade_mesa(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    simular_sessao(client, admin.cpf)
    
    response = client.post('/api/salao/criar_mesa', json={
        "capacidade": "dez"
    })
    
    assert response.status_code == 400
    dados = response.get_json()
    assert dados["success"] is False