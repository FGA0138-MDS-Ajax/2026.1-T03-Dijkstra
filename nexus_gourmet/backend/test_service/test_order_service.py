from datetime import datetime, timedelta, time, timezone
from models.models import db, User, Table, Product, Order, ProductOrdered
from models.enums import Role, OrderStatus, TableStatus, ProductCategory


# --- FUNÇÕES DE AJUDA PARA PREPARAR A BASE DE DADOS ---
def criar_dados_iniciais():
    """Cria um utilizador (Garçom), um Cozinheiro, uma Mesa e um Produto para os testes, utilizando CPF como chave."""
    # Usando CPF pois abrir_comanda agora espera user_cpf
    garcom = User(cpf=11122233344, nome="João Garçom", senha="123", cargo=Role.GARCOM)
    cozinheiro = User(cpf=99988877766, nome="Maria Chef", senha="123", cargo=Role.COZINHEIRO)
    
    # Mantemos o número 5 apenas como ponto de partida da mesa no banco falso
    mesa = Table(numero=5, capacidade=4, status=TableStatus.LIVRE)
    produto = Product(nome="Hambúrguer", preco=20.50, categoria=ProductCategory.PRATO)
    
    db.session.add_all([garcom, cozinheiro, mesa, produto])
    db.session.commit()
    return garcom, cozinheiro, mesa, produto

# --- INÍCIO DOS TESTES ---

def test_abrir_comanda_com_sucesso(app, order_service):
    garcom, _, mesa, _ = criar_dados_iniciais()
    comanda_id, mensagem = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=garcom.cpf)
    
    assert comanda_id is not None
    assert mensagem == "Comanda aberta com sucesso."
    
    # Verifica se o status da mesa mudou para OCUPADA
    mesa_atualizada = Table.query.filter_by(numero=mesa.numero).first()
    assert mesa_atualizada.status == TableStatus.OCUPADA

def test_abrir_multiplas_comandas_mesma_mesa(app, order_service):
    garcom, _, mesa, _ = criar_dados_iniciais()
    
    comanda1_id, mensagem1 = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=garcom.cpf)
    comanda2_id, mensagem2 = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=garcom.cpf)
    
    assert comanda1_id is not None
    assert comanda2_id is not None
    assert comanda1_id != comanda2_id # IDs diferentes para comandas diferentes

def test_listar_todas_comandas(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    
    for _ in range(3):
        order_id, _ = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=garcom.cpf)
        order_service.adicionar_item(order_id, produto.id, 1, "", garcom)
        order_service.enviar_comanda(order_id, garcom) # Altera para EM_PREPARO e itens para PREPARANDO
    
    todas_comandas = order_service.listar_todas_comandas()
    
    assert len(todas_comandas) == 3
    for comanda in todas_comandas:
        assert comanda['mesa']['numero'] == mesa.numero

def test_adicionar_item_com_sucesso(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    sucesso, mensagem = order_service.adicionar_item(
        order_id=order_id, 
        product_id=produto.id, 
        quantidade=2, 
        observacao="Sem cebola", 
        user=garcom
    )
    
    assert sucesso is True
    assert mensagem == "Item adicionado."
    
    # Verifica se os itens foram guardados
    pedido = order_service.get_order_by_id(order_id)
    assert len(pedido.itens) == 1
    assert pedido.itens[0].quantidade == 2
    assert pedido.itens[0].observacao == "Sem cebola"

def test_adicionar_item_quantidade_invalida(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    # Tenta adicionar quantidade 0
    sucesso, mensagem = order_service.adicionar_item(order_id, produto.id, 0, "", garcom)
    
    assert sucesso is False
    assert mensagem == "Quantidade deve ser maior que zero."

def test_calcular_total(app, order_service):
    garcom, _, mesa, produto1 = criar_dados_iniciais()
    
    # Adicionamos uma bebida para testar a soma (sem forçar o ID)
    produto2 = Product(nome="Suco", preco=10.00, categoria=ProductCategory.BEBIDA)
    db.session.add(produto2)
    db.session.commit()
    
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    # Adiciona 1 Hambúrguer (20.50) e 2 Sucos (20.00)
    order_service.adicionar_item(order_id, produto1.id, 1, "", garcom)
    order_service.adicionar_item(order_id, produto2.id, 2, "", garcom)
    
    total = order_service.calcular_total(order_id)
    
    # Total esperado = 40.50
    assert total == 40.50

def test_enviar_comanda_com_sucesso(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(order_id, produto.id, 1, "", garcom)
    
    sucesso, mensagem = order_service.enviar_comanda(order_id, garcom)
    
    assert sucesso is True
    assert mensagem == "Comanda enviada para a cozinha."
    
    pedido = order_service.get_order_by_id(order_id)
    assert pedido.status == OrderStatus.EM_PREPARO

def test_enviar_comanda_sem_itens_falha(app, order_service):
    garcom, _, mesa, _ = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    sucesso, mensagem = order_service.enviar_comanda(order_id, garcom)
    
    assert sucesso is False
    assert mensagem == "Não é possível enviar um pedido sem itens."
    
def test_fechar_comanda_sucesso(app, order_service):
    garcom, cozinheiro, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(order_id, produto.id, 1, "", garcom)
    
    # Temos de forçar o pedido a chegar ao status 'ENTREGUE' para poder fechar
    pedido = order_service.get_order_by_id(order_id)
    pedido.status = OrderStatus.ENTREGUE
    db.session.commit()
    
    sucesso, resposta = order_service.fechar_comanda(order_id)
    
    assert sucesso is True
    assert "mensagem" in resposta
    assert resposta["conta"]["total"] == 20.50
    
    # A mesa deve ter ficado livre de novo
    mesa_atualizada = Table.query.filter_by(numero=mesa.numero).first()
    assert mesa_atualizada.status == TableStatus.LIVRE

def test_alterar_status(app, order_service):
    garcom, cozinheiro, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(order_id, produto.id, 1, "", garcom)
    order_service.alterar_status(order_id, OrderStatus.EM_PREPARO, garcom)

    # Garçom tenta mudar para PRONTO (deve falhar)
    sucesso_garcom, mensagem_garcom = order_service.alterar_status(order_id, OrderStatus.PRONTO, garcom)
    
    assert sucesso_garcom is False
    assert "perfil" in mensagem_garcom.lower()
    
    # Cozinheiro muda para PRONTO (deve funcionar)
    sucesso_cozinheiro, mensagem_cozinheiro = order_service.alterar_status(order_id, OrderStatus.PRONTO, cozinheiro)
    
    assert sucesso_cozinheiro is True
    assert mensagem_cozinheiro == "Status atualizado para Pronto."
    
    pedido_atualizado = order_service.get_order_by_id(order_id)
    assert pedido_atualizado.status == OrderStatus.PRONTO

def test_daily_statistics_filtra_apenas_hoje(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    
    # 1. Cria uma comanda de HOJE
    id_hoje, _ = order_service.abrir_comanda(mesa.numero, garcom.id)
    
    # A MÁGICA ESTÁ AQUI: Forçamos a data exata de hoje na hora local,
    # ignorando o que o banco de dados colocou como padrão.
    comanda_hoje = order_service.get_order_by_id(id_hoje)
    comanda_hoje.data_abertura = datetime.now()
    db.session.commit()
def test_tempo_decorrido(app, order_service):
    agora_sem_fuso = datetime.now(timezone.utc).replace(tzinfo=None)  

    # classe Mock para simular uma comanda do banco
    class MockComanda:
        def __init__(self):
            self.entrada_cozinha = agora_sem_fuso - timedelta(minutes=5, seconds=30)
            self.status = OrderStatus.EM_PREPARO
            self.saida_cozinha = None

    comanda_simulada = MockComanda()
    
    tempo_formatado = order_service.tempo_decorrido(comanda_simulada)
    
    assert tempo_formatado == "5m 30s"
def test_daily_statistics(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    
    agora_local = datetime.now()
    
    # comanda para HOJE
    id_hoje, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    pedido_hoje = order_service.get_order_by_id(id_hoje)
    pedido_hoje.entrada_cozinha = agora_local # Força a data local!
    
    order_service.adicionar_item(id_hoje, produto.id, 1, "", garcom)
    
    # comanda CANCELADA HOJE
    id_cancelada, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(id_cancelada, produto.id, 2, "", garcom)
    pedido_cancelado = order_service.get_order_by_id(id_cancelada)
    pedido_cancelado.entrada_cozinha = agora_local # Força a data local!
    pedido_cancelado.status = OrderStatus.CANCELADO
    
    # comanda de ONTEM (deve ser ignorada)
    ontem = agora_local - timedelta(days=1)
    comanda_antiga = Order(
        numero_diario=99,
        numero_mesa=mesa.numero,
        user_id=garcom.cpf,
        status=OrderStatus.ENTREGUE,
        entrada_cozinha=ontem
    )
    db.session.add(comanda_antiga)
    db.session.commit()
    
    stats = order_service.daily_statistics()
    
    assert stats["total_comandas"] == 2 # Conta as duas de hoje (1 normal, 1 cancelada)
    assert stats["total_comandas_canceladas"] == 1
    assert stats["total_itens"] == 2 # 1 item na normal + 1 itens na cancelada
    assert stats["total_faturamento"] == 61.50