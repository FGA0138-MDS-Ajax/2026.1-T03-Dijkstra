from datetime import datetime, timedelta, timezone
from models.models import db, User, Table, Product, Order, ProductOrdered
from models.enums import Role, OrderStatus, TableStatus, ProductCategory
from models.error_message import OrderErrorMessages, UserErrorMessages, TableErrorMessages
from models.sucess_message import TableSuccessMessages, OrderSuccessMessages, UserSuccessMessages
from werkzeug.security import generate_password_hash

# ==================================================
# FUNÇÕES DE AUXÍLIO PARA PREPARAR A BASE DE DADOS
# ==================================================
def criar_dados_iniciais():
    garcom = User(
        nome = "Garçom",
        cpf = "12345678901",
        senha = generate_password_hash("Senha123!"),
        cargo = Role.GARCOM,
        foto_usuario = "caminho/para/foto_garcom.jpg"
    )
    cozinheiro = User(
        nome="Maria Chef",
        cpf="11144477735",
        senha=generate_password_hash("Senha1234!"), 
        cargo=Role.COZINHEIRO,
        foto_usuario="caminho/para/foto_cozinheiro.jpg"
    )    
    mesa = Table(numero=5, capacidade=4, status=TableStatus.LIVRE)
    produto = Product(nome="Hambúrguer", preco=20.50, categoria=ProductCategory.PRATO, tempo_preparacao=20)
    
    db.session.add_all([garcom, cozinheiro, mesa, produto])
    db.session.commit()
    return garcom, cozinheiro, mesa, produto

# ===================================================
# TESTES DE FUNCIONALIDADES DO SERVIÇO DE COMANDAS
# ===================================================
def test_abrir_comanda_com_sucesso(app, order_service):
    garcom, _, mesa, _ = criar_dados_iniciais()
    
    comanda_id, mensagem = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=garcom.cpf)
    
    assert comanda_id is not None
    assert mensagem == OrderSuccessMessages.COMANDA_ABERTA

    mesa_atualizada = Table.query.filter_by(numero=mesa.numero).first()
    assert mesa_atualizada.status == TableStatus.OCUPADA

def test_abrir_multiplas_comandas_mesma_mesa(app, order_service):
    garcom, _, mesa, _ = criar_dados_iniciais()
    
    comanda1_id, mensagem1 = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=garcom.cpf)
    comanda2_id, mensagem2 = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=garcom.cpf)
    
    assert comanda1_id is not None
    assert comanda2_id is not None
    assert comanda1_id != comanda2_id 

def test_listar_todas_comandas(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    
    order_id, _ = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=garcom.cpf)
    order_service.adicionar_item(order_id, produto.id, 1, "", garcom)
    
    listagem = order_service.listar_todas_comandas()
    
    assert len(listagem) == 1
    assert listagem[0]['id'] == order_id
    assert listagem[0]['itens'][0]['produto'] == "Hambúrguer"

def test_listar_todas_comandas_independente_de_status(app, order_service):
    garcom, cozinheiro, mesa, produto = criar_dados_iniciais()
    
    # Cria uma comanda PENDENTE
    id_pendente, _ = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=garcom.cpf)
    order_service.adicionar_item(id_pendente, produto.id, 1, "", garcom)
    
    # Cria outra comanda e cancela ela (Status: CANCELADO)
    id_cancelada, _ = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=garcom.cpf)
    order_service.editar_comanda(id_cancelada, [], garcom, cancelar=True)
    
    # O listar_todas deve trazer AMBAS
    listagem = order_service.listar_todas_comandas()
    assert len(listagem) == 2
    
    ids_retornados = [c['id'] for c in listagem]
    assert id_pendente in ids_retornados
    assert id_cancelada in ids_retornados

def test_listar_comandas_por_status_especifico(app, order_service):
    garcom, cozinheiro, mesa, produto = criar_dados_iniciais()
    
    # 1. Cria comanda PENDENTE
    id_pendente, _ = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=garcom.cpf)
    order_service.adicionar_item(id_pendente, produto.id, 1, "Pendente", garcom)
    
    # 2. Cria comanda em EM_PREPARO
    id_preparo, _ = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=garcom.cpf)
    order_service.adicionar_item(id_preparo, produto.id, 1, "Em preparo", garcom)
    order_service.enviar_comanda(id_preparo, garcom)
    
    # Testando filtro de status ÚNICO (Apenas Pendentes)
    comandas_pendentes = order_service.listar_comandas_por_status(OrderStatus.PENDENTE)
    assert len(comandas_pendentes) == 1
    assert comandas_pendentes[0]['id'] == id_pendente
    
    # Testando filtro com uma LISTA de status (Pendentes + Em Preparo)
    comandas_filtradas = order_service.listar_comandas_por_status([OrderStatus.PENDENTE, OrderStatus.EM_PREPARO])
    assert len(comandas_filtradas) == 2

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
    assert mensagem == OrderSuccessMessages.ITEM_ADICIONADO
    
    pedido = order_service.get_order_by_id(order_id)
    assert len(pedido.itens) == 1
    assert pedido.itens[0].quantidade == 2
    assert pedido.itens[0].observacao == "Sem cebola"

def test_adicionar_item_quantidade_invalida(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    sucesso, mensagem = order_service.adicionar_item(order_id, produto.id, 0, "", garcom)
    
    assert sucesso is False
    assert mensagem == OrderErrorMessages.QUANTIDADE_MINIMA

def test_editar_comanda_remover_e_adicionar_itens(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    order_service.adicionar_item(order_id, produto.id, 2, "Original", garcom)
    pedido = order_service.get_order_by_id(order_id)
    item_id = pedido.itens[0].id
    
    novo_produto = Product(nome="Refrigerante", preco=6.00, categoria=ProductCategory.BEBIDA, tempo_preparacao=0)
    db.session.add(novo_produto)
    db.session.commit()
    
    payload_itens = [
        {"id": item_id, "quantidade": 0},
        {"product_id": novo_produto.id, "quantidade": 3, "observacao": "Gelado"}
    ]
    
    sucesso, msg = order_service.editar_comanda(order_id, payload_itens, garcom)
    assert sucesso is True
    
    db.session.refresh(pedido)
    assert len(pedido.itens) == 1
    assert pedido.itens[0].product_id == novo_produto.id
    assert pedido.itens[0].quantidade == 3

def test_cancelar_comanda_via_edicao_sucesso(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(order_id, produto.id, 1, "", garcom)
    
    sucesso, mensagem = order_service.editar_comanda(order_id, itens=[], user=garcom, cancelar=True)
    
    assert sucesso is True
    assert mensagem == OrderSuccessMessages.COMANDA_CANCELADA
    
    pedido = order_service.get_order_by_id(order_id)
    assert pedido.status == OrderStatus.CANCELADO

# ================================================
# TESTES DE FUNCIONALIDADES DE CÁLCULO E STATUS
# ================================================
def test_calcular_total(app, order_service):
    garcom, _, mesa, produto1 = criar_dados_iniciais()
    
    produto2 = Product(nome="Suco", preco=10.00, categoria=ProductCategory.BEBIDA, tempo_preparacao=2)
    db.session.add(produto2)
    db.session.commit()
    
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    order_service.adicionar_item(order_id, produto1.id, 1, "", garcom)
    order_service.adicionar_item(order_id, produto2.id, 2, "", garcom)
    
    total = order_service.calcular_total(order_id)
    assert total == 40.50

def test_enviar_comanda_com_sucesso(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(order_id, produto.id, 1, "", garcom)
    
    sucesso, mensagem = order_service.enviar_comanda(order_id, garcom)
    
    assert sucesso is True
    assert mensagem == OrderSuccessMessages.COMANDA_ENVIADA
    
    pedido = order_service.get_order_by_id(order_id)
    assert pedido.status == OrderStatus.EM_PREPARO
    assert pedido.entrada_cozinha is not None  

def test_enviar_comanda_sem_itens_falha(app, order_service):
    garcom, _, mesa, _ = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    sucesso, mensagem = order_service.enviar_comanda(order_id, garcom)
    
    assert sucesso is False
    assert mensagem == OrderErrorMessages.COMANDA_SEM_ITENS

def test_fechar_comanda_sucesso(app, order_service):
    garcom, cozinheiro, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(order_id, produto.id, 1, "", garcom)
    
    order_service.alterar_status(order_id, OrderStatus.EM_PREPARO, garcom)
    order_service.alterar_status(order_id, OrderStatus.PRONTO, cozinheiro)
    order_service.alterar_status(order_id, OrderStatus.ENTREGUE, garcom)
    
    sucesso, resposta = order_service.fechar_comanda(order_id, user=garcom)
    
    assert sucesso is True
    assert resposta["mensagem"] == OrderSuccessMessages.COMANDA_FECHADA
    assert resposta["conta"]["total"] == 20.50
    
    mesa_atualizada = Table.query.filter_by(numero=mesa.numero).first()
    assert mesa_atualizada.status == TableStatus.LIVRE

def test_fechar_comanda_cancelada_faturamento_zero(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(order_id, produto.id, 5, "", garcom)
    
    order_service.editar_comanda(order_id, [], garcom, cancelar=True)
    
    sucesso, resposta = order_service.fechar_comanda(order_id, user=garcom)
    assert sucesso is True
    assert resposta["conta"]["total"] == 0.0 
    assert resposta["mensagem"] == OrderSuccessMessages.COMANDA_FECHADA

    mesa_atualizada = Table.query.filter_by(numero=mesa.numero).first()
    assert mesa_atualizada.status == TableStatus.LIVRE

def test_fechamento_multiplas_comandas_na_mesma_mesa(order_service, table_service, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    mesa = dados_iniciais["mesa"]
    
    # 1. Garçom abre DUAS comandas para a mesma mesa
    comanda1_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    comanda2_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    # Adiciona itens e entrega ambas
    produto_id = dados_iniciais["produto"].id
    order_service.adicionar_item(comanda1_id, produto_id, 1, "", garcom)
    order_service.adicionar_item(comanda2_id, produto_id, 1, "", garcom)
    
    # (Pula direto pro final simulando entrega)
    order_service.alterar_status(comanda1_id, "Em Preparo", garcom)
    order_service.alterar_status(comanda1_id, "Pronto", dados_iniciais["cozinheiro"])
    order_service.alterar_status(comanda1_id, "Entregue", garcom)
    
    order_service.alterar_status(comanda2_id, "Em Preparo", garcom)
    order_service.alterar_status(comanda2_id, "Pronto", dados_iniciais["cozinheiro"])
    order_service.alterar_status(comanda2_id, "Entregue", garcom)
    
    # 2. Fecha a PRIMEIRA comanda
    order_service.fechar_comanda(comanda1_id, garcom)
    
    # A mesa deve CONTINUAR OCUPADA, pois a comanda 2 ainda está lá!
    mesa_atualizada = table_service.get_table_by_number(mesa.numero)
    assert mesa_atualizada.status.value == "Ocupada"
    
    # 3. Fecha a SEGUNDA comanda
    order_service.fechar_comanda(comanda2_id, garcom)
    
    # Agora sim, a mesa deve ficar LIVRE!
    assert mesa_atualizada.status.value == "Livre"

def test_comanda_fantasma_fechamento_zerado(order_service, table_service, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    mesa = dados_iniciais["mesa"]
    
    # 1. Garçom abre a comanda (cliente sentou, mesa fica ocupada)
    comanda_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    # 2. Tenta enviar pra cozinha sem itens (Deve ser bloqueado)
    sucesso_enviar, msg_enviar = order_service.enviar_comanda(comanda_id, garcom)
    assert sucesso_enviar is False
    
    # 3. Cliente desiste e vai embora. Garçom cancela a comanda.
    sucesso_cancelar, _ = order_service.editar_comanda(comanda_id, [], garcom, cancelar=True)
    assert sucesso_cancelar is True
    
    # 4. Garçom fecha a comanda cancelada para liberar a mesa no sistema
    sucesso_fechar, dados_fechar = order_service.fechar_comanda(comanda_id, garcom)
    assert sucesso_fechar is True
    assert dados_fechar["conta"]["total"] == 0.0 # Conta tem que vir zerada
    
    # 5. Garante que a mesa foi liberada com sucesso
    mesa_atualizada = table_service.get_table_by_number(mesa.numero)
    assert mesa_atualizada.status.value == "Livre"

def test_alterar_status_permissoes(app, order_service):
    garcom, cozinheiro, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(order_id, produto.id, 1, "", garcom)
    
    order_service.alterar_status(order_id, OrderStatus.EM_PREPARO, garcom)

    sucesso_garcom, mensagem_garcom = order_service.alterar_status(order_id, OrderStatus.PRONTO, garcom)
    assert sucesso_garcom is True
    
    sucesso_cozinheiro, _ = order_service.alterar_status(order_id, OrderStatus.ENTREGUE, cozinheiro)
    assert sucesso_cozinheiro is False
    
    pedido_atualizado = order_service.get_order_by_id(order_id)
    assert pedido_atualizado.status == OrderStatus.PRONTO

def test_tempo_decorrido_fluxo_completo(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(order_id, produto.id, 1, "", garcom)
    
    pedido = order_service.get_order_by_id(order_id)
    assert order_service.tempo_decorrido(pedido) == "Não iniciado"
    
    order_service.alterar_status(order_id, OrderStatus.EM_PREPARO, garcom)
    assert "0m" in order_service.tempo_decorrido(pedido)

def test_estatisticas_diarias_filtra_apenas_hoje(app, order_service):
    garcom, _, mesa, produto = criar_dados_iniciais()
    
    id_hoje, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)    
    order_service.adicionar_item(id_hoje, produto.id, 1, "", garcom)
    order_service.enviar_comanda(id_hoje, garcom)
    
    ontem = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=1)
    comanda_antiga = Order(
        numero_diario=99,
        numero_mesa=mesa.numero, 
        user_cpf=garcom.cpf,
        status=OrderStatus.EM_PREPARO, 
        entrada_cozinha=ontem,
        data_criacao=ontem 
    )
    db.session.add(comanda_antiga)
    db.session.commit()
    
    stats = order_service.estatisticas_diarias()
    assert stats["total_comandas"] == 1
    assert stats["total_faturamento"] == 20.50
    
# ======================================
# VALIDAÇÃO DE RESTRIÇÕES DE CARGO
# ======================================
def test_abrir_comanda_por_cozinheiro_deve_falhar(app, order_service):
    _, cozinheiro, mesa, _ = criar_dados_iniciais()
    comanda_id, mensagem = order_service.abrir_comanda(numero_mesa=mesa.numero, user_cpf=cozinheiro.cpf)
    
    assert comanda_id is None
    assert mensagem == OrderErrorMessages.SEM_PERMISSAO

def test_adicionar_item_por_cozinheiro_deve_falhar(app, order_service):
    garcom, cozinheiro, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    sucesso, mensagem = order_service.adicionar_item(order_id, produto.id, 1, "", cozinheiro)
    assert sucesso is False
    assert mensagem == OrderErrorMessages.SEM_PERMISSAO

def test_editar_comanda_por_cozinheiro_deve_falhar(app, order_service):
    garcom, cozinheiro, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    sucesso, mensagem = order_service.editar_comanda(order_id, itens=[], user=cozinheiro)
    assert sucesso is False
    assert mensagem == OrderErrorMessages.SEM_PERMISSAO

def test_enviar_comanda_por_cozinheiro_deve_falhar(app, order_service):
    garcom, cozinheiro, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(order_id, produto.id, 1, "", garcom)
    
    sucesso, mensagem = order_service.enviar_comanda(order_id, user=cozinheiro)
    assert sucesso is False
    assert mensagem == OrderErrorMessages.SEM_PERMISSAO

def test_fechar_comanda_por_cozinheiro_deve_falhar(app, order_service):
    garcom, cozinheiro, mesa, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(order_id, produto.id, 1, "", garcom)
    
    order_service.alterar_status(order_id, OrderStatus.EM_PREPARO, garcom)
    order_service.alterar_status(order_id, OrderStatus.PRONTO, cozinheiro)
    order_service.alterar_status(order_id, OrderStatus.ENTREGUE, garcom)
    
    sucesso, mensagem = order_service.fechar_comanda(order_id, user=cozinheiro)
    assert sucesso is False
    assert mensagem == OrderErrorMessages.SEM_PERMISSAO

def test_contra_fluxo_status_comanda(order_service, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    cozinheiro = dados_iniciais["cozinheiro"]
    mesa = dados_iniciais["mesa"]
    produto = dados_iniciais["produto"] 

    comanda_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    
    order_service.adicionar_item(comanda_id, produto.id, 1, "Sem cebola", garcom)
    
    order_service.alterar_status(comanda_id, "Em Preparo", garcom)
    order_service.alterar_status(comanda_id, "Pronto", cozinheiro)
    order_service.alterar_status(comanda_id, "Entregue", garcom)
    
    # === TESTANDO O CONTRA-FLUXO DIRETO NO SERVICE ===
    # 1. Garçom volta para PRONTO
    sucesso, msg = order_service.alterar_status(comanda_id, "Pronto", garcom)
    assert sucesso is True
    
    # 2. Cozinheiro volta para EM_PREPARO
    sucesso, msg = order_service.alterar_status(comanda_id, "Em Preparo", cozinheiro)
    assert sucesso is True
    
    # 3. Garçom volta para PENDENTE
    sucesso, msg = order_service.alterar_status(comanda_id, "Pendente", garcom)
    assert sucesso is True

def test_status_finalizado_bloqueia_alteracao(order_service, dados_iniciais):
    garcom = dados_iniciais["garcom"]
    cozinheiro = dados_iniciais["cozinheiro"]
    mesa = dados_iniciais["mesa"]
    produto = dados_iniciais["produto"]
    
    comanda_id, _ = order_service.abrir_comanda(mesa.numero, garcom.cpf)
    order_service.adicionar_item(comanda_id, produto.id, 1, "Sem cebola", garcom)
    order_service.alterar_status(comanda_id, "Em Preparo", garcom)
    order_service.alterar_status(comanda_id, "Pronto", cozinheiro)
    order_service.alterar_status(comanda_id, "Entregue", garcom)
    
    # Garçom fecha a comanda (status FINALIZADO)
    sucesso_fechar, _ = order_service.fechar_comanda(comanda_id, garcom)
    assert sucesso_fechar is True
    
    # === TESTANDO O BLOQUEIO ===
    # Tenta tirar do finalizado e voltar para Entregue
    sucesso, msg = order_service.alterar_status(comanda_id, "Entregue", garcom)
    
    assert sucesso is False
    assert "Transição inválida" in msg