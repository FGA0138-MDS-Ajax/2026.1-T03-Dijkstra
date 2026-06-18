from models.enums import ProductCategory
from models.models import Product
from services.product_service import ProductService

def product_service():
    return ProductService()

# ==========================================
# TESTES DE CADASTRO
# ==========================================
def test_cadastrar_produto_com_sucesso(app, product_service):
    # Usamos .value para passar a string exata que o banco espera (ex: "Bebida")
    sucesso, mensagem = product_service.cadastrar_produto(
        id=1, 
        nome="Refrigerante", 
        categoria=ProductCategory.BEBIDA.value, 
        preco=5.50
    )
    
    assert sucesso is True
    assert mensagem == "Produto cadastrado com sucesso."

    produto = product_service.get_product_by_id(1)
    assert produto.nome == "Refrigerante"
    assert float(produto.preco) == 5.50

def test_cadastrar_produto_preco_invalido(app, product_service):
    # Preço negativo deve ser bloqueado
    sucesso, mensagem = product_service.cadastrar_produto(
        id=1, 
        nome="Refrigerante", 
        categoria=ProductCategory.BEBIDA.value, 
        preco=-5.00
    )
    
    assert sucesso is False
    assert mensagem == "Preço deve ser maior que zero."

def test_cadastrar_produto_nome_vazio(app, product_service):
    # Tenta cadastrar sem nome
    sucesso, mensagem = product_service.cadastrar_produto(
        id=1, 
        nome="", 
        categoria=ProductCategory.BEBIDA.value, 
        preco=5.00
    )
    
    assert sucesso is False
    assert mensagem == "Nome do produto é obrigatório."

def test_cadastrar_produto_categoria_invalida(app, product_service):
    # Envia uma string que não existe no Enum ProductCategory
    sucesso, mensagem = product_service.cadastrar_produto(
        id=1, 
        nome="Refrigerante", 
        categoria="CategoriaInventada", 
        preco=5.00
    )
    
    assert sucesso is False
    assert "Categoria inválida" in mensagem

# ==========================================
# TESTES DE EDIÇÃO E DELEÇÃO
# ==========================================
def test_editar_produto_com_sucesso(app, product_service):
    product_service.cadastrar_produto(1, "Suco", ProductCategory.BEBIDA.value, 5.00)

    sucesso, mensagem = product_service.editar_produto(
        product_id=1, 
        nome="Suco de Laranja", 
        categoria=ProductCategory.BEBIDA.value, 
        preco=7.00
    )
    
    assert sucesso is True
    produto = product_service.get_product_by_id(1)
    assert produto.nome == "Suco de Laranja"
    assert float(produto.preco) == 7.00

def test_deletar_produto_com_sucesso(app, product_service):
    product_service.cadastrar_produto(1, "Suco", ProductCategory.BEBIDA.value, 5.00)

    sucesso, mensagem = product_service.deletar_produto(product_id=1)
    assert sucesso is True

    produto = product_service.get_product_by_id(1)
    assert produto is None

# ==========================================
# TESTES DE LISTAGEM
# ==========================================
def test_listar_produtos(app, product_service):
    product_service.cadastrar_produto(1, "Suco", ProductCategory.BEBIDA.value, 5.00)
    product_service.cadastrar_produto(2, "Bolo", ProductCategory.SOBREMESA.value, 10.00)

    produtos = product_service.listar_produtos()
    assert len(produtos) == 2

def test_listar_por_categoria(app, product_service):
    product_service.cadastrar_produto(1, "Suco", ProductCategory.BEBIDA.value, 5.00)
    product_service.cadastrar_produto(2, "Água", ProductCategory.BEBIDA.value, 3.00)
    product_service.cadastrar_produto(3, "Bolo", ProductCategory.SOBREMESA.value, 10.00)

    # Busca apenas as bebidas
    bebidas = product_service.listar_por_categoria(ProductCategory.BEBIDA.value)
    
    assert len(bebidas) == 2
    assert bebidas[0].nome == "Suco"
    assert bebidas[1].nome == "Água"