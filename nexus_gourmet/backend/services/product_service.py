<<<<<<< HEAD
from models.models import db, Product
from models.enums import ProductCategory, Role

class ProductService:     
=======
from models import db, Product
from enums import ProductCategory
 
 
class ProdutoService:
     
>>>>>>> developer
    def listar_produtos(self):
        return Product.query.all()  
 
    def listar_por_categoria(self, categoria):
        try:
            if isinstance(categoria, str):
                categoria = ProductCategory(categoria)
        except ValueError:
            return []
        return Product.query.filter_by(categoria=categoria).all()
 
<<<<<<< HEAD
    def cadastrar_produto(self, nome, categoria, preco, tempo_preparacao=15, user_role=None):
        if user_role and user_role != Role.ADMINISTRADOR:
            return False, "Acesso negado. Apenas administradores podem cadastrar produtos."

=======
    def cadastrar_produto(self, id, nome, categoria, preco):
        if self.get_by_product_id(id):
            return False, "ID do produto já existe."
>>>>>>> developer
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
 
<<<<<<< HEAD
        try:
            produto = Product(
                nome=nome.strip(), 
                categoria=categoria, 
                preco=preco, 
                tempo_preparacao=int(tempo_preparacao)
            )
            db.session.add(produto)
            db.session.commit()
            return True, "Produto cadastrado com sucesso."
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao salvar no banco de dados: {str(e)}"
 
    def editar_produto(self, product_id, nome, categoria, preco, tempo_preparacao=15, user_role=None):
        if user_role and user_role != Role.ADMINISTRADOR:
            return False, "Acesso negado. Apenas administradores podem editar produtos."

        produto = self.get_product_by_id(product_id)
=======
        produto = Product(id=id, nome=nome.strip(), categoria=categoria, preco=preco)
        db.session.add(produto)
        db.session.commit()
        return True, "Produto cadastrado com sucesso."
 
    def editar_produto(self, product_id, nome, categoria, preco):
        produto = self.get_by_product_id(product_id)
>>>>>>> developer
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
 
        try:
            produto.nome = nome.strip()
            produto.categoria = categoria
            produto.preco = preco
            produto.tempo_preparacao = int(tempo_preparacao)
            db.session.commit()
            return True, "Produto atualizado com sucesso."
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao atualizar no banco de dados: {str(e)}"
 
<<<<<<< HEAD
    def deletar_produto(self, product_id, user_role=None):
        if user_role and user_role != Role.ADMINISTRADOR:
            return False, "Acesso negado. Apenas administradores podem deletar produtos."

        produto = self.get_product_by_id(product_id)
=======
    def deletar_produto(self, product_id):
        produto = self.get_by_product_id(product_id)
>>>>>>> developer
        if not produto:
            return False, "Produto não encontrado."
            
        try:
            db.session.delete(produto)
            db.session.commit()
            return True, "Produto excluído com sucesso."
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao excluir do banco de dados: {str(e)}"

<<<<<<< HEAD
    def get_product_by_id(self, product_id):
        return db.session.get(Product, product_id)
=======
    def get_by_product_id(self, product_id):
        return Product.query.get(product_id)
>>>>>>> developer
