from models.enums import ProductCategory, Role
from models.models import Product
from services.product_service import ProductService

def product_service():
    return ProductService()

# ==========================================
# TESTES DE CADASTRO & PERMISSÕES
# ==========================================
def test_cadastrar_produto_com_sucesso(app, product_service):
    sucesso, mensagem = product_service.cadastrar_produto(
        nome="Refrigerante", 
        categoria=ProductCategory.BEBIDA.value, 
        preco=5.50,
        user_role=Role.ADMINISTRADOR
    )
    
    assert sucesso is True
    assert mensagem == "Produto cadastrado com sucesso."

    produto = Product.query.filter_by(nome="Refrigerante").first()
    assert produto is not None
    assert produto.nome == "Refrigerante"
    assert float(produto.preco) == 5.50


def test_cadastrar_produto_campos_faltando(app, product_service):
    # 1. Teste faltando o nome
    sucesso, msg = product_service.cadastrar_produto(
        nome="", categoria=ProductCategory.BEBIDA.value, preco=5.50, user_role=Role.ADMINISTRADOR
    )
    assert sucesso is False
    assert "Nome" in msg

    # 2. Teste faltando preço (preço inválido)
    sucesso, msg = product_service.cadastrar_produto(
        nome="Coca", categoria=ProductCategory.BEBIDA.value, preco=0, user_role=Role.ADMINISTRADOR
    )
    assert sucesso is False
    assert "Preço" in msg

    # 3. Teste faltando categoria (categoria inválida)
    sucesso, msg = product_service.cadastrar_produto(
        nome="Coca", categoria="Inexistente", preco=5.50, user_role=Role.ADMINISTRADOR
    )
    assert sucesso is False
    assert "Categoria" in msg


def test_cadastrar_produto_negado_para_garcom(app, product_service):
    sucesso, msg = product_service.cadastrar_produto(
        nome="Hambúrguer", 
        categoria=ProductCategory.PRATO.value, 
        preco=25.00,
        user_role=Role.GARCOM
    )
    assert sucesso is False
    assert "Acesso negado" in msg


def test_cadastrar_produto_negado_para_cozinheiro(app, product_service):
    sucesso, msg = product_service.cadastrar_produto(
        nome="Bolo de Rolo", 
        categoria=ProductCategory.SOBREMESA.value, 
        preco=12.00,
        user_role=Role.COZINHEIRO
    )
    assert sucesso is False
    assert "Acesso negado" in msg

    
# ==========================================
# TESTES DE EDIÇÃO E DELEÇÃO
# ==========================================
def test_editar_produto_com_sucesso(app, product_service):
    product_service.cadastrar_produto("Suco", ProductCategory.BEBIDA.value, 5.00, user_role=Role.ADMINISTRADOR)
    
    produto_criado = Product.query.filter_by(nome="Suco").first()

    sucesso, mensagem = product_service.editar_produto(
        product_id=produto_criado.id, 
        nome="Suco de Laranja", 
        categoria=ProductCategory.BEBIDA.value, 
        preco=7.00,
        user_role=Role.ADMINISTRADOR
    )
    
    assert sucesso is True
    produto_editado = product_service.get_product_by_id(produto_criado.id)
    assert produto_editado.nome == "Suco de Laranja"
    assert float(produto_editado.preco) == 7.00


def test_editar_produto_negado(app, product_service):
    product_service.cadastrar_produto("Suco", ProductCategory.BEBIDA.value, 5.00, user_role=Role.ADMINISTRADOR)
    produto_criado = Product.query.filter_by(nome="Suco").first()

    sucesso, mensagem = product_service.editar_produto(
        product_id=produto_criado.id, 
        nome="Suco Batizado", 
        categoria=ProductCategory.BEBIDA.value, 
        preco=15.00,
        user_role=Role.GARCOM
    )
    assert sucesso is False
    assert "Acesso negado" in mensagem


def test_deletar_produto_com_sucesso(app, product_service):
    product_service.cadastrar_produto("Suco", ProductCategory.BEBIDA.value, 5.00, user_role=Role.ADMINISTRADOR)
    
    produto_criado = Product.query.filter_by(nome="Suco").first()

    sucesso, mensagem = product_service.deletar_produto(product_id=produto_criado.id, user_role=Role.ADMINISTRADOR)
    assert sucesso is True

    produto_apagado = product_service.get_product_by_id(produto_criado.id)
    assert produto_apagado is None


def test_deletar_produto_negado(app, product_service):
    product_service.cadastrar_produto("Suco", ProductCategory.BEBIDA.value, 5.00, user_role=Role.ADMINISTRADOR)
    produto_criado = Product.query.filter_by(nome="Suco").first()

    # Tentativa de exclusão por um Cozinheiro
    sucesso, mensagem = product_service.deletar_produto(product_id=produto_criado.id, user_role=Role.COZINHEIRO)
    assert sucesso is False
    assert "Acesso negado" in mensagem


# ==========================================
# TESTES DE LISTAGEM
# ==========================================
def test_listar_produtos(app, product_service):
    product_service.cadastrar_produto("Suco", ProductCategory.BEBIDA.value, 5.00, user_role=Role.ADMINISTRADOR)
    product_service.cadastrar_produto("Bolo", ProductCategory.SOBREMESA.value, 10.00, user_role=Role.ADMINISTRADOR)

    produtos = product_service.listar_produtos()
    assert len(produtos) == 2


def test_listar_por_categoria(app, product_service):
    product_service.cadastrar_produto("Suco", ProductCategory.BEBIDA.value, 5.00, user_role=Role.ADMINISTRADOR)
    product_service.cadastrar_produto("Água", ProductCategory.BEBIDA.value, 3.00, user_role=Role.ADMINISTRADOR)
    product_service.cadastrar_produto("Bolo", ProductCategory.SOBREMESA.value, 10.00, user_role=Role.ADMINISTRADOR)

    bebidas = product_service.listar_por_categoria(ProductCategory.BEBIDA.value)
    
    assert len(bebidas) == 2
    nomes_bebidas = [b.nome for b in bebidas]
    assert "Suco" in nomes_bebidas
    assert "Água" in nomes_bebidas