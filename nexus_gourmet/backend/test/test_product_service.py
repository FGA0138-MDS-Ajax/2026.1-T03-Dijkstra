from models.enums import ProductCategory
from models.models import Product
from services.product_service import ProductService

def product_service():
    return ProductService()

# ==========================================
# TESTES DE CADASTRO
# ==========================================
def test_cadastrar_produto_com_sucesso(app, product_service):
    # Não passamos mais o ID, o backend gera um aleatório!
    sucesso, mensagem = product_service.cadastrar_produto(
        nome="Refrigerante", 
        categoria=ProductCategory.BEBIDA.value, 
        preco=5.50
    )
    
    assert sucesso is True
    assert mensagem == "Produto cadastrado com sucesso."

    # Buscamos pelo nome para descobrir qual ID foi gerado
    produto = Product.query.filter_by(nome="Refrigerante").first()
    assert produto is not None
    assert produto.nome == "Refrigerante"
    assert float(produto.preco) == 5.50


def test_cadastrar_produto_campos_faltando(app, product_service):
    # 1. Teste faltando o nome
    sucesso, msg = product_service.cadastrar_produto(nome="", categoria=ProductCategory.BEBIDA.value, preco=5.50)
    assert sucesso is False
    assert "Nome" in msg

    # 2. Teste faltando preço (preço inválido)
    sucesso, msg = product_service.cadastrar_produto(nome="Coca", categoria=ProductCategory.BEBIDA.value, preco=0)
    assert sucesso is False
    assert "Preço" in msg

    # 3. Teste faltando categoria (categoria inválida)
    sucesso, msg = product_service.cadastrar_produto(nome="Coca", categoria="Inexistente", preco=5.50)
    assert sucesso is False
    assert "Categoria" in msg
    
# ==========================================
# TESTES DE EDIÇÃO E DELEÇÃO
# ==========================================
def test_editar_produto_com_sucesso(app, product_service):
    product_service.cadastrar_produto("Suco", ProductCategory.BEBIDA.value, 5.00)
    
    # Precisamos pegar o produto no banco para saber qual ID ele recebeu
    produto_criado = Product.query.filter_by(nome="Suco").first()

    sucesso, mensagem = product_service.editar_produto(
        product_id=produto_criado.id, 
        nome="Suco de Laranja", 
        categoria=ProductCategory.BEBIDA.value, 
        preco=7.00
    )
    
    assert sucesso is True
    produto_editado = product_service.get_product_by_id(produto_criado.id)
    assert produto_editado.nome == "Suco de Laranja"
    assert float(produto_editado.preco) == 7.00

def test_deletar_produto_com_sucesso(app, product_service):
    product_service.cadastrar_produto("Suco", ProductCategory.BEBIDA.value, 5.00)
    
    # Pega o produto recém-criado para saber o ID
    produto_criado = Product.query.filter_by(nome="Suco").first()

    sucesso, mensagem = product_service.deletar_produto(product_id=produto_criado.id)
    assert sucesso is True

    # Verifica se realmente sumiu do banco
    produto_apagado = product_service.get_product_by_id(produto_criado.id)
    assert produto_apagado is None

# ==========================================
# TESTES DE LISTAGEM
# ==========================================
def test_listar_produtos(app, product_service):
    # Cria os produtos sem forçar o ID
    product_service.cadastrar_produto("Suco", ProductCategory.BEBIDA.value, 5.00)
    product_service.cadastrar_produto("Bolo", ProductCategory.SOBREMESA.value, 10.00)

    produtos = product_service.listar_produtos()
    assert len(produtos) == 2

def test_listar_por_categoria(app, product_service):
    # Cria os produtos sem forçar o ID
    product_service.cadastrar_produto("Suco", ProductCategory.BEBIDA.value, 5.00)
    product_service.cadastrar_produto("Água", ProductCategory.BEBIDA.value, 3.00)
    product_service.cadastrar_produto("Bolo", ProductCategory.SOBREMESA.value, 10.00)

    # Busca apenas as bebidas
    bebidas = product_service.listar_por_categoria(ProductCategory.BEBIDA.value)
    
    assert len(bebidas) == 2
    # Como a ordem não é garantida pelo ID aleatório, podemos verificar se os nomes estão na lista
    nomes_bebidas = [b.nome for b in bebidas]
    assert "Suco" in nomes_bebidas
    assert "Água" in nomes_bebidas