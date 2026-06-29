import pytest

def simular_sessao(client, cpf):
    with client.session_transaction() as sess:
        sess['user_cpf'] = cpf

def test_listar_produtos_com_sucesso(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    simular_sessao(client, garcom.cpf)
    
    response = client.get('/api/produtos')
    
    assert response.status_code == 200
    dados = response.get_json()
    assert dados["success"] is True
    assert dados["data"][0]["nome"] == "Hambúrguer"
    assert float(dados["data"][0]["preco"]) == 20.5

def test_cadastrar_produto_admin(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    simular_sessao(client, admin.cpf)
    
    payload = {
        "nome": "Pizza Margherita",
        "categoria": "Prato",
        "preco": 45.00,
        "tempo_preparacao": 20
    }
    
    response = client.post('/api/produtos/cadastrar', json=payload)
    
    assert response.status_code == 200
    assert response.get_json()["success"] is True

def test_deletar_produto_garcom_acesso_negado(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    produto = dados_iniciais["produto"]
    simular_sessao(client, garcom.cpf)
    
    response = client.delete(f'/api/produtos/deletar/{produto.id}')
    
    assert response.status_code == 403
    assert response.get_json()["success"] is False

def test_listar_produtos_por_categoria_sucesso(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    simular_sessao(client, garcom.cpf)
    
    response = client.get('/api/produtos/categoria/Prato')
    assert response.status_code == 200
    dados = response.get_json()
    assert dados["success"] is True
    assert len(dados["data"]) == 1

def test_editar_produto_admin_sucesso(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    produto = dados_iniciais["produto"]
    simular_sessao(client, admin.cpf)
    
    payload = {
        "nome": "Hambúrguer Gourmet",
        "categoria": "Prato",
        "preco": 28.90
    }
    response = client.put(f'/api/produtos/editar/{produto.id}', json=payload)
    assert response.status_code == 200
    assert response.get_json()["success"] is True

def test_deletar_produto_admin_sucesso(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    produto = dados_iniciais["produto"]
    simular_sessao(client, admin.cpf)
    
    response = client.delete(f'/api/produtos/deletar/{produto.id}')
    assert response.status_code == 200
    assert response.get_json()["success"] is True