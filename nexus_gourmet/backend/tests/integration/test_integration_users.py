import pytest

def simular_sessao(client, cpf):
    with client.session_transaction() as sess:
        sess['user_cpf'] = cpf

def test_login_sucesso_retorna_dados_usuario(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    
    response = client.post('/api/login', json={
        "cpf": garcom.cpf,
        "senha": "Senha123!" 
    })
    
    assert response.status_code == 200
    dados = response.get_json()
    assert dados["success"] is True
    assert dados["data"]["cpf"] == garcom.cpf
    assert dados["data"]["cargo"] == "Garçom"

def test_acesso_negado_sem_login(client):
    response = client.get('/api/meu_perfil')
    
    assert response.status_code == 401
    dados = response.get_json()
    assert dados["success"] is False

def test_logout_limpa_sessao(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    
    client.post('/api/login', json={"cpf": garcom.cpf, "senha": "Senha123!"})
    
    response_logout = client.post('/api/logout')
    assert response_logout.status_code == 200
    
    response_perfil = client.get('/api/meu_perfil')
    assert response_perfil.status_code == 401

def test_listar_usuarios_admin_sucesso(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    simular_sessao(client, admin.cpf)
    
    response = client.get('/api/usuarios')
    
    assert response.status_code == 200
    dados = response.get_json()
    assert dados["success"] is True
    assert len(dados["data"]) == 3 

def test_listar_usuarios_garcom_acesso_negado(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    simular_sessao(client, garcom.cpf)
    
    response = client.get('/api/usuarios')
    
    assert response.status_code == 403
    assert response.get_json()["success"] is False

def test_cadastrar_usuario_sucesso(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    simular_sessao(client, admin.cpf)

    payload = {
        "senha_admin": "SenhaAdmin!", 
        "nome": "Novo Funcionario",
        "cpf_cadastrado": "98765432100",
        "senha_cadastrada": "SenhaForte1@", # Alterado para passar na validação!
        "cargo": "Garçom" # Alterado de "GARCOM" para respeitar o Enum
    }    
    response = client.post('/api/usuarios/cadastrar', json=payload)
    
    assert response.status_code == 200
    assert response.get_json()["success"] is True

def test_editar_usuario_admin_sucesso(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    garcom = dados_iniciais["garcom"]
    simular_sessao(client, admin.cpf)
    
    payload = {
        "senha_admin": "SenhaAdmin!",
        "nome": "João Alterado",
        "cargo": "Cozinheiro"
    }
    response = client.put(f'/api/usuarios/editar_usuario/{garcom.cpf}', json=payload)
    assert response.status_code == 200
    assert response.get_json()["success"] is True

def test_deletar_usuario_proprio_admin_bloqueado(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    simular_sessao(client, admin.cpf)
    
    payload = {"senha_admin": "SenhaAdmin!"}
    response = client.delete(f'/api/usuarios/deletar_usuario/{admin.cpf}', json=payload)
    
    assert response.status_code == 400
    assert response.get_json()["success"] is False

def test_finalizar_dia_admin_sucesso(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    simular_sessao(client, admin.cpf)
    
    response = client.get('/api/usuarios/finalizar_dia')
    assert response.status_code == 200
    dados = response.get_json()
    assert dados["success"] is True
    assert "total_comandas" in dados["data"]

def test_fantasma_banco_dados_usuario_inexistente(client, dados_iniciais):
    admin = dados_iniciais["admin"]
    simular_sessao(client, admin.cpf)
    
    # Tenta deletar um CPF que não existe no banco
    payload = {"senha_admin": "SenhaAdmin!"}
    response = client.delete('/api/usuarios/deletar_usuario/99999999999', json=payload)
    
    assert response.status_code == 400
    dados = response.get_json()
    assert dados["success"] is False
    assert "não encontrado" in dados["message"].lower()