from models import db, Produto
from enums import CategoriaProduto
 
 
class ProdutoService:
 
    def get_produto_by_id(self, produto_id):
        return Produto.query.get(produto_id)
 
    def listar_produtos(self):
        return Produto.query.all()
 
    def listar_por_categoria(self, categoria_str):
        try:
            categoria = CategoriaProduto(categoria_str)
        except ValueError:
            return []
        return Produto.query.filter_by(categoria=categoria).all()
 
    def cadastrar_produto(self, nome, categoria_str, preco_str):
        if not nome or not nome.strip():
            return False, "Nome do produto é obrigatório."
        try:
            preco = float(preco_str)
        except (TypeError, ValueError):
            return False, "Preço inválido."
        if preco <= 0:
            return False, "Preço deve ser maior que zero."
        try:
            categoria = CategoriaProduto(categoria_str)
        except ValueError:
            return False, f"Categoria inválida: {categoria_str}."
 
        produto = Produto(nome=nome.strip(), categoria=categoria, preco=preco)
        db.session.add(produto)
        db.session.commit()
        return True, "Produto cadastrado com sucesso."
 
    def editar_produto(self, produto_id, nome, categoria_str, preco_str):
        produto = self.get_produto_by_id(produto_id)
        if not produto:
            return False, "Produto não encontrado."
        if not nome or not nome.strip():
            return False, "Nome do produto é obrigatório."
        try:
            preco = float(preco_str)
        except (TypeError, ValueError):
            return False, "Preço inválido."
        if preco <= 0:
            return False, "Preço deve ser maior que zero."
        try:
            categoria = CategoriaProduto(categoria_str)
        except ValueError:
            return False, f"Categoria inválida: {categoria_str}."
 
        produto.nome = nome.strip()
        produto.categoria = categoria
        produto.preco = preco
        db.session.commit()
        return True, "Produto atualizado com sucesso."
 
    def deletar_produto(self, produto_id):
        produto = self.get_produto_by_id(produto_id)
        if not produto:
            return False, "Produto não encontrado."
        db.session.delete(produto)
        db.session.commit()
        return True, "Produto excluído com sucesso."
