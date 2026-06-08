from models import db, Usuario
from enums import PerfilUsuario
from werkzeug.security import generate_password_hash, check_password_hash


def autenticar(login, senha):
    u = Usuario.query.filter_by(login=login).first()
    if u and check_password_hash(u.senha, senha):
        return u
    return None

def get_todos(solicitante):
    if solicitante.perfil != PerfilUsuario.ADMINISTRADOR:
        return None, "Apenas administradores podem listar usuários."
    return Usuario.query.all(), None

def get_por_id(usuario_id, solicitante):
    if solicitante.perfil != PerfilUsuario.ADMINISTRADOR:
        return None, "Apenas administradores podem consultar usuários."
    return Usuario.query.get(usuario_id), None

def criar_usuario(nome, login, senha, perfil, solicitante):
    if solicitante.perfil != PerfilUsuario.ADMINISTRADOR:
        return None, "Apenas administradores podem criar usuários."
    if Usuario.query.filter_by(login=login).first():
        return None, "Login já em uso."
    u = Usuario(nome=nome, login=login, senha=generate_password_hash(senha), perfil=perfil)
    db.session.add(u)
    db.session.commit()
    return u, "Usuário criado."

def editar_usuario(usuario_id, nome, login, perfil, solicitante):
    if solicitante.perfil != PerfilUsuario.ADMINISTRADOR:
        return None, "Apenas administradores podem editar usuários."
    u = Usuario.query.get(usuario_id)
    if not u:
        return None, "Usuário não encontrado."
    u.nome = nome
    u.login = login
    u.perfil = perfil
    db.session.commit()
    return u, "Usuário atualizado."

def deletar_usuario(usuario_id, solicitante):
    if solicitante.perfil != PerfilUsuario.ADMINISTRADOR:
        return False, "Apenas administradores podem excluir usuários."
    u = Usuario.query.get(usuario_id)
    if not u:
        return False, "Usuário não encontrado."
    db.session.delete(u)
    db.session.commit()
    return True, "Usuário excluído."