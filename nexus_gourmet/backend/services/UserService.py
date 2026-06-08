from enums import PerfilUsuario
from werkzeug.security import generate_password_hash, check_password_hash


def autenticar(usuario, senha):
    if usuario and check_password_hash(usuario.senha, senha):
        return usuario
    return None

def criar_usuario(usuario, solicitante):
    if solicitante.perfil != PerfilUsuario.ADMINISTRADOR:
        return None, "Apenas administradores podem criar usuários."
    usuario.senha = generate_password_hash(usuario.senha)
    return usuario, "Usuário criado."

def editar_usuario(usuario, nome, login, perfil, solicitante):
    if solicitante.perfil != PerfilUsuario.ADMINISTRADOR:
        return None, "Apenas administradores podem editar usuários."
    usuario.nome = nome
    usuario.login = login
    usuario.perfil = perfil
    return usuario, "Usuário atualizado."

def deletar_usuario(usuario, solicitante):
    if solicitante.perfil != PerfilUsuario.ADMINISTRADOR:
        return False, "Apenas administradores podem excluir usuários."
    return True, "Usuário excluído."