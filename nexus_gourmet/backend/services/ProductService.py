from enums import PerfilUsuario


def criar_produto(produto, solicitante):
    if solicitante.perfil != PerfilUsuario.ADMINISTRADOR:
        return None, "Apenas administradores podem criar produtos."
    return produto, "Produto criado."

def editar_produto(produto, nome, categoria, preco, solicitante):
    if solicitante.perfil != PerfilUsuario.ADMINISTRADOR:
        return None, "Apenas administradores podem editar produtos."
    produto.nome = nome
    produto.categoria = categoria
    produto.preco = preco
    return produto, "Produto atualizado."

def deletar_produto(produto, solicitante):
    if solicitante.perfil != PerfilUsuario.ADMINISTRADOR:
        return False, "Apenas administradores podem excluir produtos."
    return True, "Produto excluído."
