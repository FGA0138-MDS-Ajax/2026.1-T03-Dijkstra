from models import db, Product
from models.enums import ProductCategory
  
class ProductService:     
    def listar_produtos(self):
        return Product.query.all()  
 
    def listar_por_categoria(self, categoria):
        try:
            categoria = ProductCategory(categoria)
        except ValueError:
            return []
        return Product.query.filter_by(categoria=categoria).all()
 
    def cadastrar_produto(self, id, nome, categoria, preco):
        if self.get_product_by_id(id):
            return False, "ID do produto já existe."
        if not nome or not nome.strip():
            return False, "Nome do produto é obrigatório."
        try:
            preco = float(preco)
        except (TypeError, ValueError):
            return False, "Preço inválido."
        if preco <= 0:
            return False, "Preço deve ser maior que zero."
        try:
            categoria = ProductCategory(categoria)
        except ValueError:
            return False, f"Categoria inválida: {categoria}."
 
        produto = Product(id=id, nome=nome.strip(), categoria=categoria, preco=preco)
        db.session.add(produto)
        db.session.commit()
        return True, "Produto cadastrado com sucesso."
 
    def editar_produto(self, product_id, nome, categoria, preco):
        produto = self.get_product_by_id(product_id)
        if not produto:
            return False, "Produto não encontrado."
        if not nome or not nome.strip():
            return False, "Nome do produto é obrigatório."
        try:
            preco = float(preco)
        except (TypeError, ValueError):
            return False, "Preço inválido."
        if preco <= 0:
            return False, "Preço deve ser maior que zero."
        try:
            categoria = ProductCategory(categoria)
        except ValueError:
            return False, f"Categoria inválida: {categoria}."
 
        produto.nome = nome.strip()
        produto.categoria = categoria
        produto.preco = preco
        db.session.commit()
        return True, "Produto atualizado com sucesso."
 
    def deletar_produto(self, product_id):
        produto = self.get_product_by_id(product_id)
        if not produto:
            return False, "Produto não encontrado."
        db.session.delete(produto)
        db.session.commit()
        return True, "Produto excluído com sucesso."

    def get_product_by_id(self, product_id):
        return Product.query.get(product_id)