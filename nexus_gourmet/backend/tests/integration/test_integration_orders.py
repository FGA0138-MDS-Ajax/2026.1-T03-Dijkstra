import pytest

def simular_sessao(client, cpf):
    with client.session_transaction() as sess:
        sess['user_cpf'] = cpf

def test_abrir_comanda_integra_banco(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    mesa = dados_iniciais["mesa"]
    simular_sessao(client, garcom.cpf)
    
    response = client.post(f'/api/salao/{mesa.numero}/comandas/abrir_comanda')
    
    assert response.status_code == 200
    dados = response.get_json()
    assert dados["success"] is True
    assert "comanda_id" in dados["data"]

def test_adicionar_item_na_comanda(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    mesa = dados_iniciais["mesa"]
    produto = dados_iniciais["produto"]
    simular_sessao(client, garcom.cpf)
    
    res_abrir = client.post(f'/api/salao/{mesa.numero}/comandas/abrir_comanda')
    comanda_id = res_abrir.get_json()["data"]["comanda_id"]
    
    payload = {
        "product_id": produto.id,
        "quantidade": 2,
        "observacao": "Sem cebola"
    }
    res_adicionar = client.post(
        f'/api/salao/{mesa.numero}/comandas/{comanda_id}/adicionar_item',
        json=payload
    )
    
    assert res_adicionar.status_code == 200
    assert res_adicionar.get_json()["success"] is True
    
    res_visualizar = client.get(f'/api/salao/{mesa.numero}/comandas/{comanda_id}')
    dados_comanda = res_visualizar.get_json()["data"]
    
    assert len(dados_comanda["itens"]) > 0
    assert dados_comanda["itens"][0]["quantidade"] == 2

def test_listar_fila_cozinha_com_cozinheiro(client, dados_iniciais):
    cozinheiro = dados_iniciais["cozinheiro"]
    simular_sessao(client, cozinheiro.cpf)
    
    response = client.get('/api/cozinha/fila')
    
    assert response.status_code == 200
    dados = response.get_json()
    assert dados["success"] is True
    assert isinstance(dados["data"], list)

def test_listar_fila_cozinha_garcom_bloqueado(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    simular_sessao(client, garcom.cpf)
    
    response = client.get('/api/cozinha/fila')
    
    assert response.status_code == 403
    dados = response.get_json()
    assert dados["success"] is False
    assert "Acesso negado" in dados["message"]

def test_fluxo_completo_comanda(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    cozinheiro = dados_iniciais["cozinheiro"]
    mesa = dados_iniciais["mesa"]
    produto = dados_iniciais["produto"]
    
    # === PASSO 1: Garçom abre a comanda ===
    simular_sessao(client, garcom.cpf)
    res_abrir = client.post(f'/api/salao/{mesa.numero}/comandas/abrir_comanda')
    comanda_id = res_abrir.get_json()["data"]["comanda_id"]
    
    # === PASSO 2: Garçom adiciona item ===
    client.post(
        f'/api/salao/{mesa.numero}/comandas/{comanda_id}/adicionar_item',
        json={"product_id": produto.id, "quantidade": 1}
    )
    
    # === PASSO 3: Garçom envia para a cozinha ===
    res_enviar = client.post(f'/api/salao/{mesa.numero}/comandas/{comanda_id}/enviar_comanda')
    assert res_enviar.status_code == 200
    assert res_enviar.get_json()["success"] is True
    
    # === PASSO 4: Cozinheiro vê o pedido e altera o status ===
    simular_sessao(client, cozinheiro.cpf)

    res_fila = client.get('/api/cozinha/fila')
    fila_dados = res_fila.get_json()["data"]
    assert len(fila_dados) > 0

    res_status = client.put(
        f'/api/cozinha/{comanda_id}/alterar_status',
        json={"status": "Pronto"} 
    )
    assert res_status.status_code == 200

    # === PASSO 4.5: Garçom entrega o pedido na mesa ===
    simular_sessao(client, garcom.cpf)
    res_entregue = client.put(
        f'/api/cozinha/{comanda_id}/alterar_status',
        json={"status": "Entregue"}
    )
    assert res_entregue.status_code == 200

    # === PASSO 5: Garçom fecha a comanda ===
    res_fechar = client.post(f'/api/salao/{mesa.numero}/comandas/{comanda_id}/fechar_comanda')

    assert res_fechar.status_code == 200
    assert res_fechar.get_json()["success"] is True
    
def test_contra_fluxo_status_comanda(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    cozinheiro = dados_iniciais["cozinheiro"]
    mesa = dados_iniciais["mesa"]
    produto = dados_iniciais["produto"]
    
    simular_sessao(client, garcom.cpf)
    res_abrir = client.post(f'/api/salao/{mesa.numero}/comandas/abrir_comanda')
    comanda_id = res_abrir.get_json()["data"]["comanda_id"]
    client.post(f'/api/salao/{mesa.numero}/comandas/{comanda_id}/adicionar_item', json={"product_id": produto.id, "quantidade": 1})
    client.post(f'/api/salao/{mesa.numero}/comandas/{comanda_id}/enviar_comanda') # Vai para EM_PREPARO
    
    simular_sessao(client, cozinheiro.cpf)
    client.put(f'/api/cozinha/{comanda_id}/alterar_status', json={"status": "Pronto"})
    
    simular_sessao(client, garcom.cpf)
    client.put(f'/api/cozinha/{comanda_id}/alterar_status', json={"status": "Entregue"})
    
    # === TESTANDO O CONTRA-FLUXO ===
    # 1. Garçom volta para PRONTO (errou a mesa)
    res_voltar_pronto = client.put(f'/api/cozinha/{comanda_id}/alterar_status', json={"status": "Pronto"})
    assert res_voltar_pronto.status_code == 200
    
    # 2. Cozinheiro volta para EM_PREPARO (viu que faltou um ingrediente)
    simular_sessao(client, cozinheiro.cpf)
    res_voltar_preparo = client.put(f'/api/cozinha/{comanda_id}/alterar_status', json={"status": "Em Preparo"})
    assert res_voltar_preparo.status_code == 200

def test_tentar_alterar_status_apos_finalizado_falha(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    cozinheiro = dados_iniciais["cozinheiro"]
    mesa = dados_iniciais["mesa"]
    produto = dados_iniciais["produto"]
    
    simular_sessao(client, garcom.cpf)
    res_abrir = client.post(f'/api/salao/{mesa.numero}/comandas/abrir_comanda')
    comanda_id = res_abrir.get_json()["data"]["comanda_id"]
    client.post(f'/api/salao/{mesa.numero}/comandas/{comanda_id}/adicionar_item', json={"product_id": produto.id, "quantidade": 1})
    client.post(f'/api/salao/{mesa.numero}/comandas/{comanda_id}/enviar_comanda')
    
    simular_sessao(client, cozinheiro.cpf)
    client.put(f'/api/cozinha/{comanda_id}/alterar_status', json={"status": "Pronto"})
    
    simular_sessao(client, garcom.cpf)
    client.put(f'/api/cozinha/{comanda_id}/alterar_status', json={"status": "Entregue"})
    
    # Garçom FECHA a conta (vai para FINALIZADO)
    client.post(f'/api/salao/{mesa.numero}/comandas/{comanda_id}/fechar_comanda')
    
    # === TESTANDO O MURO DO FINALIZADO ===
    # Cozinheiro tenta voltar para PRONTO
    simular_sessao(client, cozinheiro.cpf)
    res_erro1 = client.put(f'/api/cozinha/{comanda_id}/alterar_status', json={"status": "Pronto"})
    assert res_erro1.status_code == 400
    assert "Transição inválida" in res_erro1.get_json()["message"]
    
    # Garçom tenta voltar para ENTREGUE
    simular_sessao(client, garcom.cpf)
    res_erro2 = client.put(f'/api/cozinha/{comanda_id}/alterar_status', json={"status": "Entregue"})
    assert res_erro2.status_code == 400
    assert "Transição inválida" in res_erro2.get_json()["message"]

def test_fantasma_banco_dados_comanda_inexistente(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    mesa = dados_iniciais["mesa"]
    simular_sessao(client, garcom.cpf)
    
    response = client.post(f'/api/salao/{mesa.numero}/comandas/9999/adicionar_item', json={
        "product_id": 1,
        "quantidade": 1
    })
    
    assert response.status_code == 400
    dados = response.get_json()
    assert dados["success"] is False
    assert "não encontrada" in dados["message"].lower()

def test_alteracao_preco_produto_com_comanda_aberta_mantem_preco_antigo(client, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    admin = dados_iniciais["admin"]
    mesa = dados_iniciais["mesa"]
    produto = dados_iniciais["produto"] # Preço inicial: 20.50
    
    # 1. Garçom abre a comanda e o cliente pede 1 Hambúrguer
    simular_sessao(client, garcom.cpf)
    res_abrir = client.post(f'/api/salao/{mesa.numero}/comandas/abrir_comanda')
    comanda_id = res_abrir.get_json()["data"]["comanda_id"]
    
    # Neste momento, o sistema deve salvar o preco_vendido como 20.50
    client.post(f'/api/salao/{mesa.numero}/comandas/{comanda_id}/adicionar_item', json={"product_id": produto.id, "quantidade": 1})
    
    # 2. Administrador altera o preço do Hambúrguer no cardápio para R$ 30.00
    simular_sessao(client, admin.cpf)
    client.put(f'/api/produtos/editar/{produto.id}', json={
        "nome": "Hambúrguer", "categoria": "Prato", "preco": 30.00
    })
    
    # 3. Garçom avança os status da comanda e fecha a conta
    simular_sessao(client, garcom.cpf)
    client.post(f'/api/salao/{mesa.numero}/comandas/{comanda_id}/enviar_comanda')
    
    simular_sessao(client, dados_iniciais["cozinheiro"].cpf)
    client.put(f'/api/cozinha/{comanda_id}/alterar_status', json={"status": "Pronto"})
    
    simular_sessao(client, garcom.cpf)
    client.put(f'/api/cozinha/{comanda_id}/alterar_status', json={"status": "Entregue"})
    
    # FECHA A CONTA
    res_fechar = client.post(f'/api/salao/{mesa.numero}/comandas/{comanda_id}/fechar_comanda')
    conta = res_fechar.get_json()["data"]["conta"]
    
    # 4. A HORA DA VERDADE: O total cobrado tem que ser o antigo (20.50), ignorando a inflação!
    assert float(conta["total"]) == 20.50