from models import db, Produto
from enums import CategoriaProduto


def get_todos():
    return Produto.query.all()

def get_por_id(produto_id):
    return Produto.query.get(produto_id)

def get_por_categoria(categoria: CategoriaProduto):
    return Produto.query.filter_by(categoria=categoria).all()

def criar_produto(nome, categoria, preco):
    p = Produto(nome=nome, categoria=categoria, preco=preco)
    db.session.add(p)
    db.session.commit()
    return p, "Produto criado."

def editar_produto(produto_id, nome, categoria, preco):
    p = get_por_id(produto_id)
    if not p:
        return None, "Produto não encontrado."
    p.nome = nome
    p.categoria = categoria
    p.preco = preco
    db.session.commit()
    return p, "Produto atualizado."

def deletar_produto(produto_id):
    p = get_por_id(produto_id)
    if not p:
        return False, "Produto não encontrado."
    db.session.delete(p)
    db.session.commit()
    return True, "Produto excluído."
