import pytest
from models.models import db, User, Table, Product, Order, ProductOrdered
from models.enums import Role, OrderStatus, TableStatus, ProductCategory

# --- FUNÇÕES DE AJUDA PARA PREPARAR A BASE DE DADOS ---
def criar_dados_iniciais():
    """Cria um utilizador (Garçom), um Cozinheiro, uma Mesa e um Produto para os testes"""
    garcom = User(id=1, nome="João Garçom", senha="123", cargo=Role.GARCOM)
    cozinheiro = User(id=2, nome="Maria Chef", senha="123", cargo=Role.COZINHEIRO)
    mesa = Table(numero=5, capacidade=4, status=TableStatus.LIVRE)
    produto = Product(id=1, nome="Hambúrguer", preco=20.50, categoria=ProductCategory.PRATO)
    
    db.session.add_all([garcom, cozinheiro, mesa, produto])
    db.session.commit()
    return garcom, cozinheiro, mesa, produto

# --- INÍCIO DOS TESTES ---

def test_abrir_comanda_com_sucesso(app, order_service):
    garcom, _, _, _ = criar_dados_iniciais()
    
    comanda_id, mensagem = order_service.abrir_comanda(numero_mesa=5, user_id=garcom.id)
    
    assert comanda_id is not None
    assert mensagem == "Comanda aberta com sucesso."
    
    # Verifica se o status da mesa mudou para OCUPADA
    mesa = Table.query.filter_by(numero=5).first()
    assert mesa.status == TableStatus.OCUPADA

def test_abrir_comanda_falha_mesa_nao_livre(app, order_service):
    garcom, _, mesa, _ = criar_dados_iniciais()
    mesa.status = TableStatus.OCUPADA # Forçamos a mesa a estar ocupada
    db.session.commit()
    
    comanda_id, mensagem = order_service.abrir_comanda(numero_mesa=5, user_id=garcom.id)
    
    assert comanda_id is None
    assert "não está livre" in mensagem

def test_adicionar_item_com_sucesso(app, order_service):
    garcom, _, _, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(5, garcom.id)
    
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
    garcom, _, _, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(5, garcom.id)
    
    # Tenta adicionar quantidade 0
    sucesso, mensagem = order_service.adicionar_item(order_id, produto.id, 0, "", garcom)
    
    assert sucesso is False
    assert mensagem == "Quantidade deve ser maior que zero."

def test_calcular_total(app, order_service):
    garcom, _, _, produto1 = criar_dados_iniciais()
    
    # Adicionamos uma bebida para testar a soma
    produto2 = Product(id=2, nome="Suco", preco=10.00, categoria=ProductCategory.BEBIDA)
    db.session.add(produto2)
    db.session.commit()
    
    order_id, _ = order_service.abrir_comanda(5, garcom.id)
    
    # Adiciona 1 Hambúrguer (20.50) e 2 Sucos (20.00)
    order_service.adicionar_item(order_id, produto1.id, 1, "", garcom)
    order_service.adicionar_item(order_id, produto2.id, 2, "", garcom)
    
    total = order_service.calcular_total(order_id)
    
    # Total esperado = 40.50
    assert total == 40.50

def test_enviar_comanda_sem_itens_falha(app, order_service):
    garcom, _, _, _ = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(5, garcom.id)
    
    sucesso, mensagem = order_service.enviar_comanda(order_id, garcom)
    
    assert sucesso is False
    assert mensagem == "Não é possível enviar um pedido sem itens."

def test_fechar_comanda_sucesso(app, order_service):
    garcom, cozinheiro, _, produto = criar_dados_iniciais()
    order_id, _ = order_service.abrir_comanda(5, garcom.id)
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
    mesa = Table.query.filter_by(numero=5).first()
    assert mesa.status == TableStatus.LIVRE